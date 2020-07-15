'''
Reference: https://github.com/ClearMacroIPD/MHF/blob/master/MTR/CYCLE/PHASES.py
'''

import pandas as pd


def get_cycle_phase(df, model, window, thresh='mean'):
    """

        Iterate through time series to identify rule-based cycle values. 

        Variables:
        ---------
            df:     pandas.DataFrame() or pandas.Series() object, time series.
            model:  str, 'EWM', 'MA' or 'Hist', signal to identify regime switches.
            window: int, applied to signal. Number of previous values to consider.  
            thresh: str or int, optional 'mean', 'median', int, set threshold in 
                    to identify expansion and contraction phases.

        Returns:
        --------
            pandas.DataFrame(), time series

    """

    def start_method(df):
        """
            Assign first cycle value using the first point outside the array.
            Variable: df: pd.DataFrame() or pd.Series() object, time series.
            Returns:  str, cycle value   
        """
        n_0, n_1 = df.iloc[1, 0], df.iloc[0, 0]
        thresh = df.iloc[1].loc['threshold']

        if n_0 == n_1:
            n_0, n_1 = df.iloc[2].loc['Model'], df.iloc[1].loc['Model']

        if (n_0 < thresh) and (n_0 > n_1):
            cycle_value = 'recovery'
        elif (n_0 > thresh) and (n_0 > n_1):
            cycle_value = 'expansion'
        elif (n_0 > thresh) and (n_0 < n_1):
            cycle_value = 'slowdown'
        elif (n_0 < thresh) and (n_0 < n_1):
            cycle_value = 'contraction'
        return cycle_value

    # set threshold
    if thresh == 'mean':
        df['threshold'] = df.iloc[:, 0].mean()
    elif thresh == 'median':
        df['threshold'] = df.iloc[:, 0].median()
    else:
        df['threshold'] = thresh

    # select type of model
    params = {
        'EWM':      df.iloc[:, 0].ewm(span=window).mean(),
        'MA':       df.iloc[:, 0].rolling(window).mean(),
        'Hist':     df.iloc[:, 0].shift(window)
    }
    df[model] = params[model]

    # drop nan to remove window length
    df = df.dropna()

    # start model with initial values
    cycle_value = start_method(df)

    # append first cycle value
    list_cycle_values = [cycle_value]

    # iterate through time series
    # Note: start at 1, as we have found the first cycle value\
    for i, v in enumerate(df.iloc[1:].T, start=1):
        # n_1: previous index value in time series
        # n_0: current index value in time series
        # thresh: time series average (note: potentially thresh=100 in OECD indicator...)
        # ma_1: previous index value in moving average
        # ma_0: current index value in moving average
        n_1 = df.iloc[i-1, 0]
        n_0 = df.iloc[i, 0]
        thresh = df.loc[v, 'threshold']
        ma_1 = df.iloc[i-1].loc[model]
        ma_0 = df.loc[v, model]

        if cycle_value in ['double_dip', 'contraction']:
            if (n_0 < thresh
                and n_0 > n_1
                and ma_0 > ma_1
                    and ma_0 < thresh):
                list_cycle_values.append('recovery')
                cycle_value = 'recovery'
            elif n_0 > thresh:
                list_cycle_values.append('recovery')
                cycle_value = 'recovery'
            else:
                list_cycle_values.append(cycle_value)

        elif cycle_value in ['recovery']:
            if (n_0 > thresh
                and n_0 > n_1
                and ma_0 > ma_1
                    and ma_0 > thresh):
                list_cycle_values.append('expansion')
                cycle_value = 'expansion'
            elif (n_0 < thresh
                  and n_0 < n_1
                  and ma_0 < ma_1
                  and ma_0 < thresh):
                list_cycle_values.append('double_dip')
                cycle_value = 'double_dip'
            else:
                list_cycle_values.append(cycle_value)

        elif cycle_value in ['expansion', 're-acceleration']:
            if (n_0 > thresh
                and n_0 < n_1
                and ma_0 < ma_1
                    and ma_0 > thresh):
                list_cycle_values.append('slowdown')
                cycle_value = 'slowdown'
            elif (n_0 < thresh):
                list_cycle_values.append('slowdown')
                cycle_value = 'slowdown'
            else:
                list_cycle_values.append(cycle_value)

        elif cycle_value in ['slowdown']:
            if (n_0 < thresh
                and n_0 < n_1
                and ma_0 < ma_1
                    and ma_0 < thresh):
                list_cycle_values.append('contraction')
                cycle_value = 'contraction'
            elif (n_0 > thresh
                  and n_0 > n_1
                  and ma_0 > ma_1
                  and ma_0 > thresh):
                list_cycle_values.append('re-acceleration')
                cycle_value = 're-acceleration'
            else:
                list_cycle_values.append(cycle_value)

    # gather results
    res = pd.DataFrame(list_cycle_values, columns=['phase'])
    output = pd.concat([df.reset_index(), res], axis=1)
    output = output.set_index(output.columns[0])
    return output


def get_cycle_duration(df_cycle):
    """

        Read growth cycle dates and phases. translate it to timedelta.

        Variable:
        --------

            df_cycle:   pd.DataFrame() object, output from get_cycle_phase 
                        function.

        Returns:
        -------

            pd.DataFrame object, time series, including timedeltas from each 
            phases.

    """
    # focus on dataframe phases
    df_cycle = df_cycle['phase'].reset_index()
    df_cycle.columns = ['date', 'phase']

    # identify start and end phases
    df_cycle['phase_start'] = df_cycle['phase'].loc[df_cycle['phase'].shift()
                                                    != df_cycle['phase']]
    df_cycle['phase_end'] = df_cycle['phase'].loc[df_cycle['phase']
                                                  .shift(-1) != df_cycle['phase']]

    # reshape dataframe: extract start and end phases
    start_phase = pd.DataFrame(df_cycle.dropna(subset=['phase_start']
                                               )[['date', 'phase_start']].reset_index(drop=True))
    end_phase = pd.DataFrame(df_cycle.dropna(subset=['phase_end']
                                             )[['date']].reset_index(drop=True))

    # gather phases
    df_duration = pd.merge(start_phase, end_phase,
                           left_index=True, right_index=True)
    df_duration.columns = ['start date', 'phase', 'end date']

    # calculate duration timedelta
    # timedeltas are differences in times, expressed in difference units
    df_duration['timedelta'] = df_duration['end date'] - \
        df_duration['start date']

    return df_duration



if __name__ == '__main__':

    from clearmacro.MHF.PIPELINE import PIPE
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    underlying = 'US'
    data = 'trailing'
    model = 'MA'
    window = 4
    thresh = 100  # optional 'mean', 'median'
    param = PIPE.param(underlying)
    df = param[underlying]['economics']['gdp']
    # identify cycle phases
    df_cycle = get_cycle_phase(df, model, window, thresh)
    print(df_cycle['phase'].tail(20))

    df_cycle['phase'].value_counts()
    df.head(20)
    # calculate duration and estimate average duration
    df_duration = get_cycle_duration(df_cycle)
    # print average timedelta
    # Note: In this example, we did not identify any re-acceleration phases...
    for phase in ['recovery', 'expansion', 'slowdown', 'contraction',
                  'double_dip', 're-acceleration']:
        print(
            phase, df_duration.loc[df_duration['phase'] == phase]['timedelta'].mean())
