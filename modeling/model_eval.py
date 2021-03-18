# eval model
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, precision_score, recall_score

def ppv_n(y_true, y_proba, n):
    '''
    Function that calculates the ppv score for the top n predictions (instead of number of positives). 
    If the number of positives is smaller than n, then the function defaults to the normal ppv function.
    '''

    num_of_1s = np.sum(y_true == 1)
    if num_of_1s < n:
        return ppv(y_true, y_proba)
    sorted_y_true = np.flip([x for _, x in sorted(zip(y_proba, y_true))])
    ppv_n_score = np.sum(sorted_y_true[:n] == 1) / n  # percentage of positives in top-rated peptides
    
    return ppv_n_score

def model_metrics(y_true, y_pred, y_proba):
    
    print('Accuracy:', balanced_accuracy_score(y_true, y_pred))
    print('AUC:', roc_auc_score(y_true, y_proba))
    print('PPV:', precision_score(y_true, y_pred))
    print('PPV100:', ppv_n(y_true, y_proba, 100))
    print('Sensitivity (TPR):', recall_score(y_true, y_pred))
