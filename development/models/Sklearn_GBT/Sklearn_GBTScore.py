
import pickle
import pandas as pd
                            
global _thisModelFit
        
with open('Sklearn_GBT.pickle', 'rb') as _pFile:
    _thisModelFit = pickle.load(_pFile)

def scoreSklearn_GBT(LOAN, MORTDUE, VALUE, REASON, JOB, YOJ, DEROG, DELINQ, CLAGE
, NINQ, CLNO, DEBTINC):
    "Output: EM_EVENTPROBABILITY, EM_CLASSIFICATION"
    
    try:
        _thisModelFit
    except NameError:

        with open('Sklearn_GBT.pickle', 'rb') as _pFile:
            _thisModelFit = pickle.load(_pFile)
    
    inputArray = pd.DataFrame([[LOAN, MORTDUE, VALUE, REASON, JOB, YOJ, DEROG, DELINQ, CLAGE
, NINQ, CLNO, DEBTINC]], columns = ['LOAN', 'MORTDUE', 'VALUE', 'REASON', 'JOB', 'YOJ', 'DEROG', 'DELINQ', 'CLAGE'
, 'NINQ', 'CLNO', 'DEBTINC'])
    
    prediction = _thisModelFit.predict_proba(inputArray)

    EM_EVENTPROBABILITY = float(prediction[:,1])

    if (EM_EVENTPROBABILITY >= 0.5):
        EM_CLASSIFICATION = '1'
    else:
        EM_CLASSIFICATION = '0'

    return(EM_EVENTPROBABILITY, EM_CLASSIFICATION)
