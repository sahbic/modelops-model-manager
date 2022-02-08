
import pickle
import pandas as pd
import settings
                            
global _thisModelFit

with open(settings.pickle_path + 'Sklearn_GBT.pickle', 'rb') as _pFile:
    _thisModelFit = pickle.load(_pFile)

def scoreSklearn_GBT(Unique_ID, LOAN, MORTDUE, VALUE, REASON, JOB, YOJ, DEROG
, DELINQ, CLAGE, NINQ, CLNO, DEBTINC, _PARTIND_):
    "Output: EM_EVENTPROBABILITY, EM_CLASSIFICATION"
    
    try:
        _thisModelFit
    except NameError:

        with open(settings.pickle_path + 'Sklearn_GBT.pickle', 'rb') as _pFile:
            _thisModelFit = pickle.load(_pFile)
    
    inputArray = pd.DataFrame([[Unique_ID, LOAN, MORTDUE, VALUE, REASON, JOB, YOJ, DEROG
, DELINQ, CLAGE, NINQ, CLNO, DEBTINC, _PARTIND_]], columns = ['Unique_ID', 'LOAN', 'MORTDUE', 'VALUE', 'REASON', 'JOB', 'YOJ', 'DEROG'
, 'DELINQ', 'CLAGE', 'NINQ', 'CLNO', 'DEBTINC', '_PARTIND_'])
    
    prediction = _thisModelFit.predict_proba(inputArray)

    EM_EVENTPROBABILITY = float(prediction[:,1])

    if (EM_EVENTPROBABILITY >= 0.5):
        EM_CLASSIFICATION = '1'
    else:
        EM_CLASSIFICATION = '0'

    return(EM_EVENTPROBABILITY, EM_CLASSIFICATION)
