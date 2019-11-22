import pandas as pd
import numpy as np

'''
# code i used to filter data initially
# you would probably have this in a seperate file

data = pd.read_csv("openpowerlifting.csv", low_memory=False) # this is the data i downloaded from openpowerlifting.org

classes = ['53', '59', '66', '74', '83', '93', '105', '120', '120+',
            '43', '47', '52', '57', '63', '72', '84', '84+']

filtered = data[(data['BirthYearClass']=='14-18') &
                (data['Event']=='SBD') &
                (data['Equipment']=='Raw') &
                (data['Tested']=='Yes') &
                (data.WeightClassKg.isin(classes))]

filtered.to_csv('filtered-openpl.csv') # saved it so i wouldnt have to re-filter data every time
'''

data = pd.read_csv("filtered-openpl.csv", low_memory=False)

# this is just to round it to the nearest 2.5kg
def myround(x, base=2.5):
    return base * round(x/base)

def calculatevalues(wclass):
    #calculating all means and standard deviations
    smean = data[data['WeightClassKg']==wclass]['Best3SquatKg'].mean()
    sdeviation = data[data['WeightClassKg']==wclass]['Best3SquatKg'].std()

    bmean = data[data['WeightClassKg']==wclass]['Best3BenchKg'].mean()
    bdeviation = data[data['WeightClassKg']==wclass]['Best3BenchKg'].std()

    dmean = data[data['WeightClassKg']==wclass]['Best3DeadliftKg'].mean()
    ddeviation = data[data['WeightClassKg']==wclass]['Best3DeadliftKg'].std()

    tmean = data[data['WeightClassKg']==wclass]['TotalKg'].mean()
    tdeviation = data[data['WeightClassKg']==wclass]['TotalKg'].std()

    # then printing them and manually placed them into a table
    print('----------------------------------------------')
    print(wclass, "squat")
    print('untrained:', myround(smean-2.5*sdeviation))
    print('novice:', myround(smean-2*sdeviation))
    print('intermediate:', myround(smean-1*sdeviation))
    print('advanced:', myround(smean))
    print('master:', myround(smean+1*sdeviation))
    print('elite:', myround(smean+2*sdeviation))
    print('world class:', myround(smean+2.5*sdeviation))
    print('')

    print(wclass, "bench")
    print('untrained:', myround(bmean-2.5*bdeviation))
    print('novice:', myround(bmean-2*bdeviation))
    print('intermediate:', myround(bmean-1*bdeviation))
    print('advanced:', myround(bmean))
    print('master:', myround(bmean+1*bdeviation))
    print('elite:', myround(bmean+2*bdeviation))
    print('world class:', myround(bmean+2.5*bdeviation))
    print('')

    print(wclass, "deadlift")
    print('untrained:', myround(dmean-2.5*ddeviation))
    print('novice:', myround(dmean-2*ddeviation))
    print('intermediate:', myround(dmean-1*ddeviation))
    print('advanced:', myround(dmean))
    print('master:', myround(dmean+1*ddeviation))
    print('elite:', myround(dmean+2*ddeviation))
    print('world class:', myround(dmean+2.5*ddeviation))
    print('')

    print(wclass, "total")
    print('untrained:', myround(tmean-2.5*tdeviation))
    print('novice:', myround(tmean-2*tdeviation))
    print('intermediate:', myround(tmean-1*tdeviation))
    print('advanced:', myround(tmean))
    print('master:', myround(tmean+1*tdeviation))
    print('elite:', myround(tmean+2*tdeviation))
    print('world class:', myround(tmean+2.5*tdeviation))
    print('')

# just calling the function with all the male weight classes
calculatevalues('53')
calculatevalues('59')
calculatevalues('66')
calculatevalues('74')
calculatevalues('83')
calculatevalues('93')
calculatevalues('105')
calculatevalues('120')
calculatevalues('120+')
