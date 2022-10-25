"""
AUTHOR : Khaled Al Moulla
DATE   : 2022-01-01

Example of latex_table.py with NumPy or Pandas table.
"""

#%%
### MODULES

from   latex_table import latex_table
from   numpy       import nan
import numpy       as     np
import pandas      as     pd

#%%
### TABLE | NUMPY

# Values
values = np.array([
['Star 1', 5000, 25 , 25 , 4.4 , 0.1  , 0.1  , nan , 'AlMoulla21,AlMoulla22'],
['Star 2', 6000, 50 , 50 , 4.55, 0.01 , nan  ,  0.1, 'AlMoulla22'           ],
['Star 3', 5500, nan, nan, 4.6 , 0.001, 0.001, -0.1, 'AlMoulla23'           ]
])

# Labels
labels = [
'Target'                      ,
'$T_{\mathrm{eff}}$ [K]'      ,
'$T_{\mathrm{eff}}$ [K] err_u',
'$T_{\mathrm{eff}}$ [K] err_l',
'$\log\,g$'                   ,
'$\log\,g$ err_u'             ,
'$\log\,g$ err_l'             ,
'[Fe/H]'                      ,
'References'
]

#%%
### TABLE | PANDAS

# Values
values_df = pd.DataFrame()
for i in range(len(labels)):
    values_df[labels[i]] = values[:,i]
values = values_df

# Labels
labels = None

#%%
### LATEX TABLE

# Build LaTeX table
table = latex_table(values, labels, sort_column=1, error='unequal', error_suffix=[' err_u',' err_l'])

# Print LaTeX table
print('Requirements:')
print('\\usepackage{siunitx}\n')
print(table)