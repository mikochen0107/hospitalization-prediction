# define relevant values
labs = ['Female', 'Homeless', 'Age', 'Albumin', 'BUN',
       'Calcium', 'Cholesterol', 'Glucose', 'HDL',
       'A1C', 'LDL', 'Phosphorus', 'Potassium',
       'Sodium', 'eGFR', 'Creatinine', 'Urine PCR',
       'Urine ACR', 'Colonoscopy', 'Hemoglobin', 'Fecal occult',
       'PTH', 'HepB', 'Pneumovax', 'Prevnar', 'CHF',
       'Asthma', 'Diabetes', 'Hypertension', 'CHD', 'Dementia', 'Chronic pain', 'SAD',
       'PCP', 'Inpt count', 'Inpt since', 'Outpt count',
       'Outpt since', 'ED count', 'ED since', 'SBP',
       'DBP', 'Race - American Indian Alaska Native', 'Race - Asian', 'Race - black',
       'Race - Hispanic', 'Race - Native Hawaiian Pacific Islander', 'Race - other', 'Race - white',
       'Language - Chinese', 'Language - English', 'Language - other', 'Language - Russian', 
        'Language - Spanish', 'Language - Tagalog','Language - Vietnamese', 
        'Insurance - Commercial', 'Insurance - Healthy SF', 'Insurance - Medi-Cal', 'Insurance - Medicare',
        'Insurance - other', 'Urine protein 1+', 'Urine protein 2+', 'Urine protein 3+', 'Urine protein 4+', 
        'Urine protein NEGATIVE', 'Urine protein TRACE', 'Urine occult 1+', 'Urine occult 2+', 'Urine occult 3+', 
        'Urine occult NEGATIVE', 'Urine occult TRACE']
measure = [-1.15405089e-01,  9.90362845e-02, -2.96058126e-03, -2.11278844e-01,
       -8.16297964e-04, -4.49209500e-03, -3.61782173e-05,  6.91504901e-04,
        3.45810185e-03,  2.72254112e-02, -5.57956799e-04,  2.78259720e-02,
       -8.30238341e-02, -6.21048522e-03,  1.97326527e-03,  4.78753034e-02,
        7.69704101e-06,  4.91236762e-05,  2.28052503e-02, -7.41703910e-02,
       -7.42290853e-02,  3.05630639e-04, -1.03570113e-01, -3.57709946e-02,
        1.06840651e-01,  2.68823970e-01,  5.65058466e-02,  5.03604111e-02,
       -6.42577605e-02,  9.49211159e-02,  9.51087306e-02,  8.60595345e-02,
        2.82292153e-01, -1.85937432e+00,  1.91754439e-01, -3.34743108e-04,
        3.36668643e-03, -9.94668542e-04,  3.34658945e-02, -1.95456126e-04,
        1.61816216e-03,  2.89233389e-03,  8.01983088e-02, -1.42557526e-01,
       -9.09994392e-03, -4.67763046e-03,  9.19447865e-02, -1.01697192e-01,
       -4.64591100e-02, -9.82315933e-02,  1.35067273e-01,  6.04282652e-02,
       -1.15282528e-01,  1.10315750e-01, -2.04039790e-02, -4.90010416e-02,
       -1.01827870e-02, -2.09290683e-01,  2.94836266e-01,  1.11190350e-01,
       -1.86197939e-01,  1.57179525e-01,  1.94896634e-01,  1.06552638e-01,
        1.64749090e-02,  8.13315097e-02,  9.71747381e-02,  1.79589517e-01,
        1.07272593e-01,  1.30272069e-01,  1.91477473e-01,  8.25717054e-02]
lower = [-1.48384693e-01,  4.45901736e-02, -5.11157677e-03, -2.49156579e-01,
  -2.42163112e-03, -3.68252338e-02, -1.07140723e-03,  2.79774545e-04,
   1.94110624e-03, 7.48954946e-03, -2.05152620e-03 , 3.28277695e-03,
  -1.17166320e-01, -9.13654319e-03,  7.89012732e-04,  2.54983160e-02,
  -4.49354263e-06,  2.88012469e-05, -3.46142049e-02, -9.40597062e-02,
  -1.37245267e-01,  1.32120835e-04, -1.65916878e-01, -7.60062379e-02,
   4.81618359e-02,  2.20460660e-01,  1.86341948e-02,  1.31753884e-02,
  -1.16765795e-01,  5.57744441e-02,  2.89812189e-02,  3.77227811e-02,
   2.42006029e-01, -2.32975468e+00,  1.67293216e-01, -3.78891781e-04,
   2.58444538e-03, -1.07666616e-03,  2.58584714e-02, -2.17768755e-04,
   8.44661050e-04,  1.63093681e-03,  1.83064056e-02, -1.83923620e-01,
  -5.20663143e-02, -6.22478613e-02,  2.34832202e-02, -1.71033562e-01,
  -9.11598405e-02, -1.53750040e-01,  8.55689988e-02, -2.01523349e-02,
  -1.83982170e-01,  4.11449155e-02, -6.12406584e-02, -9.68142812e-02,
  -4.19592505e-02, -2.79969129e-01,  1.97783747e-01,  2.59360836e-02,
  -2.62605248e-01,  1.02019216e-01,  1.07509228e-01,  3.23959889e-02,
  -3.22543662e-04,  3.26870277e-02,  2.51774422e-02,  1.06614870e-01,
   1.93763287e-02,  3.48510236e-02,  1.37786297e-01,  2.08134178e-02,]
upper = [-7.44523041e-02,  1.56170440e-01, -1.26470018e-03, -1.45216513e-01,
   9.29042325e-04,  2.45413599e-02,  1.16078695e-03,  1.03400437e-03,
   4.83081055e-03,  4.92506505e-02,  6.35263528e-04,  4.74720420e-02,
  -4.80051817e-02, -3.23314419e-03,  2.97137689e-03,  6.60371456e-02,
   1.98855166e-05,  7.04139358e-05,  7.34779139e-02, -5.39213487e-02,
  -1.48817332e-02,  4.44915424e-04, -2.92323124e-02,  5.52758187e-03,
   1.64063018e-01,  3.07065179e-01,  9.31592121e-02,  9.04801595e-02,
  -5.10794019e-03,  1.32638560e-01,  1.54973118e-01,  1.31046899e-01,
   3.23585842e-01, -8.58810422e-01,  2.12962557e-01, -3.00437219e-04,
   4.20863727e-03, -9.26065846e-04,  4.61931784e-02, -1.68201957e-04,
   2.27618588e-03,  4.67396306e-03,  1.45898962e-01, -9.78131361e-02,
   5.67859686e-02,  6.06187051e-02,  1.54160591e-01, -2.14806966e-02,
  -4.51167938e-04, -4.37678850e-02,  1.76791965e-01,  1.28767502e-01,
  -3.96365275e-02,  1.80327834e-01,  1.95800829e-02,-8.31251442e-03,
   2.55172228e-02, -1.05599374e-01,  3.44745128e-01, 1.56713854e-01,
  -7.87266762e-02,  1.94129103e-01,  2.45586890e-01, 1.68894060e-01,
   3.84919236e-02,  1.19898203e-01,  1.77345094e-01,  2.21728275e-01,
   1.81289287e-01,  2.00760449e-01,  2.27532524e-01,  1.48152680e-01,]

x = pd.DataFrame({'var name': labs, 'estimate': np.exp(measure), 'lower': np.exp(lower), 'upper': np.exp(upper)})

x = x.sort_values(by='estimate', ascending=False)
x = x.reset_index()

# plotting all variables

import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
import zepid
from zepid.graphics import EffectMeasurePlot

p = EffectMeasurePlot(label=x['var name'], 
                      effect_measure=x['estimate'], 
                      lcl=x['lower'], 
                      ucl=x['upper'])

p.labels(effectmeasure='RR')
p.colors(pointshape="D", color='b')
ax=p.plot(figsize=(20,30), max_value=2, min_value=0)
#plt.title("Random Effect Model(Risk Ratio)",loc="right",x=1, y=1.045)
#plt.suptitle("Missing Data Imputation Method",x=-0.1,y=0.98)
ax.set_xlabel("Hospitalization risk ratio", fontsize=16)
ax.set_xticks(np.arange(0, 2, 0.25)) 
ax.set_xticklabels(np.arange(0, 2, 0.25), fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(False)
plt.savefig("Logistic regression forest plot all", bbox_inches='tight')

# plotting variables with +- 0.15 RR
abovebelow015 = x[(x['estimate'] > 1.15) | (x['estimate'] < 0.85)]
abovebelow015 = abovebelow015.reset_index()

import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
import zepid
from zepid.graphics import EffectMeasurePlot

p = EffectMeasurePlot(label=abovebelow015['var name'], 
                      effect_measure=abovebelow015['estimate'], 
                      lcl=abovebelow015['lower'], 
                      ucl=abovebelow015['upper'])

p.labels(effectmeasure='RR')
p.colors(pointshape="D")
ax=p.plot(figsize=(15,7), max_value=2, min_value=0)
#plt.title("Random Effect Model(Risk Ratio)",loc="right",x=1, y=1.045)
#plt.suptitle("Missing Data Imputation Method",x=-0.1,y=0.98)
ax.set_xlabel("Hospitalization risk ratio", fontsize=12)
ax.set_xticks(np.arange(0, 2, 0.25)) 
ax.set_xticklabels(np.arange(0, 2, 0.25), fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(False)
plt.savefig("Logistic regression forest plot all", bbox_inches='tight')

