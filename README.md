# A risk prediction model for 6-month hospitalization among patients with chronic kidney disease
<hr />

## Abstract
Hospitalization is responsible for considerable financial and disease burden in healthcare systems and patient populations. Individuals with chronic kidney disease (CKD) are twice more likely than the general population to be hospitalized. Though interventions have been devised to reduce hospitalization, risk stratification is necessary to ensure that the finite healthcare resources are intelligently allocated to patients who truly need it. A risk prediction modeling approach is proposed to identify patients with CKD who are most at-risk for hospitalization. We developed three statistical models: logistic regression, random forest classifier, and gradient boosting classifier. The models are trained with 80% of the data and tested/validated by the remaining 20%. San Francisco Health Network’s (SFHN) electronic health record is used to construct a retrospective (2008-2018) CKD cohort dataset (N = 275,721), where demographics, comorbidity, laboratory, and clinical utilization variables are extracted. The prevalence of CKD is 14.4% in the SFHN population, and hospitalization rate is 8.8% in the SFHN CKD population. Model performances (AUC = 0.89-0.90) consistently outperforms previously published models (AUC = 0.70-0.80). To demonstrate the utility of the predictive model, a cost-benefit analysis is conducted using the Johns Hopkins Community Health Partnership program (J-CHiP) as an example. Comparing cost reductions in J-CHiP with the predictive model ($6,467,593) to J-CHiP alone ($1,176,945), the incorporation of the model boosted cost reduction by $5,290,648. The validated risk prediction model for hospitalization among the CKD population may be useful to health insurance and health systems to reduce the burden of hospitalization. 

## Code Documentation
#### Data Preparation
If you're using macOS, install `pipenv` with Homebrew
```
$ brew install pipenv
```
More documentation: https://github.com/pypa/pipenv

#### Modeling
```
$ git clone https://github.com/mikochen0107/mhc-1-immunopeptidome-characterization.git
$ cd mhc-1-immunopeptidome-characterization
$ pipenv install
```
#### Data Visualization
