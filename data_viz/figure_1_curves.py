#### ROC AUC curves

X_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_train_knn.csv", delimiter=',')
y_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_train.csv", delimiter=',')
y_train = y_train[1:,1]

X_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_test_knn.csv", delimiter=',')
y_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_test.csv", delimiter=',')
y_test = y_test[1:,1]

from joblib import dump, load
lr = load('lr.joblib')
rf = load('rf.joblib')
gb = load('rbc.joblib')

from sklearn.metrics import plot_roc_curve

lr_disp = plot_roc_curve(lr, X_train, y_train, name='Logistic Regression')
rf_disp = plot_roc_curve(rf, X_train, y_train, ax=lr_disp.ax_, name='Random Forest')
gb_disp = plot_roc_curve(gb, X_train, y_train, ax=rf_disp.ax_, name='Gradient Boosting')
plt.plot([0, 1], [0, 1], color='grey', lw=1, linestyle='--')
plt.show()

lr_disp = plot_roc_curve(lr, X_test, y_test, name='Logistic Regression')
rf_disp = plot_roc_curve(rf, X_test, y_test, ax=lr_disp.ax_, name='Random Forest')
gb_disp = plot_roc_curve(gb, X_test, y_test, ax=rf_disp.ax_, name='Gradient Boosting')
plt.plot([0, 1], [0, 1], color='grey', lw=1, linestyle='--')
plt.show()

#### precision-recall curves

from sklearn.metrics import plot_precision_recall_curve

lr_disp = plot_precision_recall_curve(lr, X_train, y_train, name='Logistic Regression')
rf_disp = plot_precision_recall_curve(rf, X_train, y_train, ax=lr_disp.ax_, name='Random Forest')
gb_disp = plot_precision_recall_curve(gb, X_train, y_train, ax=rf_disp.ax_, name='Gradient Boosting')
plt.show()

lr_disp = plot_precision_recall_curve(lr, X_test, y_test, name='Logistic Regression')
rf_disp = plot_precision_recall_curve(rf, X_test, y_test, ax=lr_disp.ax_, name='Random Forest')
gb_disp = plot_precision_recall_curve(gb, X_test, y_test, ax=rf_disp.ax_, name='Gradient Boosting')
plt.show()
