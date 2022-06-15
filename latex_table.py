"""
AUTHOR : Khaled Al Moulla
DATE   : 2022-01-01

LaTeX Table.
"""

#%%
### MODULES

import numpy  as np
import pandas as pd

#%%
### FUNCTION

def latex_table(labels, values, caption='', sort_column=0, sort_type='increasing', nan_replace='-', error=None, error_suffix=None, align=True, two_column=True):

    # Function for jumping error columns
    def i_next(i):
        if error=='equal'  : return i+2
        if error=='unequal': return i+3

    # Nr. of rows and columns
    Nrow, Ncol = values.shape

    # NaN replacement
    nan_rep = '{'+nan_replace+'}'

    # Error suffix
    if (error == 'equal'  ) & (error_suffix is None):
        error_suffix =  ' err'
    if (error == 'unequal') & (error_suffix is None):
        error_suffix = [' err_u', ' err_l']

    # Index of string, variable and error columns
    str_idx = []
    var_idx = []
    err_idx = []
    for i in range(Ncol):
        try:
            float(values[0,i])
            var_idx.append(i)
        except:
            str_idx.append(i)
        if error=='equal':
            if (labels[i]+error_suffix in labels):
                err_idx.append(i)
        if error=='unequal':
            if (labels[i]+error_suffix[0] in labels) & (labels[i]+error_suffix[1] in labels):
                err_idx.append(i)

    # DataFrame: Input
    df0 = pd.DataFrame()
    for i in range(Ncol):
        df0[labels[i]] = values[:,i].astype(str)

    # DataFrame: Sort
    sort_idx = np.argsort(np.array(df0.iloc[:,sort_column]))
    if sort_type == 'increasing': sort_idx = sort_idx
    if sort_type == 'decreasing': sort_idx = sort_idx[::-1]
    df0 = df0.reindex(sort_idx).reset_index(drop=True)

    # DataFrame: Edit
    for i in range(Nrow):
        for j in range(Ncol):
            if df0.iloc[i,j] == 'nan':
                df0.iloc[i,j] = nan_rep

    # DataFrame: Output
    df = pd.DataFrame()
    i = 0
    while i < Ncol:
        if i not in err_idx:
            df[labels[i]] = df0[labels[i]]
            i += 1
        else:
            var_list = []
            sep_list = []
            err_list = []
            for j in range(Nrow):
                var = df0.iloc[j,i]
                if var == nan_rep:
                    var = ''
                    sep = nan_rep
                    err = ''
                elif error=='equal':
                    sep = '$\pm$'
                    err = df0.iloc[j,i+1]
                elif error=='unequal':
                    err_u = df0.iloc[j,i+1]
                    err_l = df0.iloc[j,i+2]
                    if err_u == err_l:
                        sep = '$\pm$'
                        err = err_u
                    if err_u != err_l:
                        sep = '$^{+}_{-}$'
                        err = '$^{'+err_u+'}_{'+err_l+'}$'
                var_list.append(var)
                sep_list.append(sep)
                err_list.append(err)
            df[labels[i]       ] = var_list
            df[labels[i]+' pm' ] = sep_list
            df[labels[i]+' err'] = err_list
            i = i_next(i)

    # Try to find column with References
    try:
        
        # References
        ref_idx  = labels.index('References')
        ref_list = df0.iloc[:,ref_idx]
        ref_list = [ref.split(',') for ref in ref_list]
        ref_uniq = np.concatenate(ref_list)[np.sort(np.unique(np.concatenate(ref_list), return_index=True)[1])]
        ref_data = np.zeros(Nrow, dtype=object)
        for i in range(Nrow):
            refi = ref_list[i]
            refn = np.zeros(len(refi), dtype=int)
            for j in range(len(refi)):
                refn[j] = np.where(refi[j] == ref_uniq)[0][0]
            ref_data[i] = ','.join([f'{n+1}' for n in np.sort(refn)])
        df[labels[ref_idx]] = ref_data

        # Caption
        caption += 'References.'
        for i in range(len(ref_uniq)):
            caption += f" {i+1}: " + "\citealt{" + f"{ref_uniq[i]}" + "},"
        caption = caption[:-1]

    except:
        pass

    # Header
    header = []
    i = 0
    while i < Ncol:
        if i not in err_idx:
            header += ['{'+labels[i]+'}']
            i += 1
        else:
            header += ['{'+labels[i]+'}', '', '']
            i = i_next(i)

    # Nr. of digits
    Ndig = np.zeros((Ncol, 3), dtype=int)
    for i in range(Ncol):
        if i in var_idx:
            var = df0.iloc[:,i]
            sgn_int = 1
            max_int = 0
            max_dec = 0
            for j in range(Nrow):
                if var[j] == nan_rep:
                    continue
                if var[j].find('.') == -1: varj = int  (var[j])
                if var[j].find('.') != -1: varj = float(var[j])
                Nint = len(str(int(abs(varj))))
                Ndec = str(varj)[::-1].find('.')
                if varj < 0      : sgn_int = -1
                if Nint > max_int: max_int = Nint
                if Ndec > max_dec: max_dec = Ndec
            Ndig[i,:] = [sgn_int, max_int, max_dec]

    # Column format
    column_format = ''
    i = 0
    while i < Ncol:
        if (i in var_idx):
            var_int = Ndig[i+0,0]*Ndig[i+0,1]
            var_dec = Ndig[i+0,2]
        if (i in err_idx):
            err_int = Ndig[i+1,0]*Ndig[i+1,1]
            err_dec = Ndig[i+1,2]
        if (i in str_idx) & (i == 0):
            column_format += 'l'
        if (i in str_idx) & (i != 0):
            column_format += ' l'
        if (i in var_idx) & (i not in err_idx):
            if     align:
                column_format += f' S[table-format={var_int}.{var_dec}]'
            if not align:
                column_format +=  ' c'
        if (i in var_idx) & (i     in err_idx):
            if     align:
                if len(np.where(df.iloc[:,i+1]=='$\pm$')[0]) == Nrow:
                    column_format += f' S[table-format={var_int}.{var_dec}]' + '@{\extracolsep{0pt}}@{$\,$}c@{$\,$}@{\extracolsep{0pt}}' + f'S[table-format={err_int}.{err_dec}]'
                else:
                    column_format += f' S[table-format={var_int}.{var_dec}]' + '@{\extracolsep{0pt}}@{$\,$}c@{$\,$}@{\extracolsep{0pt}}l'
            if not align:
                column_format += ' r@{\extracolsep{0pt}}@{$\,$}c@{$\,$}@{\extracolsep{0pt}}l'
            i = i_next(i)-1
        i += 1
    column_format = column_format.split()
    column_format = ' @{\extracolsep{\\fill}} '.join(column_format)

    # LaTeX table: Make
    lt = df.to_latex(index=False,
                        escape=False,
                        caption=caption,
                        header=header,
                        column_format=column_format,
                        multicolumn=True,
                        multicolumn_format='c',
                    )

    # LaTeX table: Edit
    if two_column:
        replace = [
        ['begin{table}'  , 'begin{table*}'               ],
        ['end{table}'    , 'end{table*}'                 ],
        ['begin{tabular}', 'begin{tabular*}{\\textwidth}'],
        ['end{tabular}'  , 'end{tabular*}'               ]
        ]
        for i in range(len(replace)):
            j = lt.find(replace[i][0])
            k = len(replace[i][0])
            lt = lt[:j] + replace[i][1] + lt[j+k:]

    # Return
    return lt

#%%