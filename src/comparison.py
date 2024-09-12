from doe_error_estimations import error_estimation
from doe_metrics import DoEType

X_0 = [13.0, 12.0, 11.0, 6.0, 9.0, 8.0, 7.0, 6.0, 6.0, 6.0]  # 6.0, 6.0, 6.0, 7.0, 8.0, 9.0, 6.0, 11.0, 12.0, 13.0]
# result = error_estimation(X_0, c_base = 20 * [3.0], is_current=False, is_optimization=True,doe_method=DoEType.CCF)
# print(result)

# Plackett-Burmann with current     --  f_1 [%]:  84.7862361559255      f_2 [%] 13.412934964881032
# Plackett-Burmann without current  --  f_1 [%]:  84.78623615591854     f_2 [%] 12.684193697475898
# Min - max design without current  --  f_1 [%]:  84.78623615592566     f_2 [%] 4.904738084901398
# Min - max design with current     --  f_1 [%]:  84.78623615591442     f_2 [%] 8.066254322281027
# Box Behnken without currents  190     --  f_1 [%]: 84.78623615592042  f_2 [%] 12.201226710752804
# Box Behnken with currents  232     --  f_1 [%]: 84.78623615592042     f_2 [%] 16.12207305354866
# CCD design with current 2071      f_2 = 22.235812675874715 %
# CCD design without currents 1045  f_2 = 14.10810774391706 %

# X_I = [8.84, 15.88, 26.91, 23.45, 6.57, 18.14, 22.69, 8.95, 12.48, 28.67]

# result = error_estimation(X_I, c_base = 20 * [3.0], is_current=False, is_optimization=False,doe_method=DoEType.PB)
# print(result)


# X_II = [13.68, 15.48, 27.21, 13.20, 14.34, 18.14, 10.13, 18.63, 21.54, 20.71]
# result = error_estimation(X_II, c_base = 20 * [3.0], is_current=False, is_optimization=True,doe_method=DoEType.SOBOL)
# print(result)


# X_III = [25.48, 15.55, 12.52, 23.31, 5.55, 14.67, 12.38, 17.81, 22.18, 17.18]
# result = error_estimation(X_III, c_base = 20 * [3.0], is_current=False, is_optimization=False,doe_method=DoEType.CCF)
# print(result)


X_PBC = [16.67, 28.82, 26.34, 24.15, 15.32, 5.87, 15.79, 16.62, 10.11, 29.23]

# result = error_estimation(X_PBC, c_base = 20 * [3.0], is_current=False, is_optimization=False,doe_method=DoEType.MINMAX)
# print(result)


# PB without current  2.7175145394697307, 1.170451118126417
# PB with currents                        2.7595184125569876
# Minmax without currents  f_1 [%]:  2.7175145394700775 f_2 [%] 2.539122986911315
# Minmax with currents f_1 [%]:  2.717514539470837 f_2 [%] 4.293400279016036


X_MINMAX1 = [14.648894105609035, 5.36700024240791, 24.231700785121845, 8.0784214322869, 12.136589144584885,
             17.239039787160376, 18.45348605305637, 15.457659788832702, 14.89771441651926, 20.0446298580020];
#costs: [0.4117744027820353, 1.7477270642623228]

#result = error_estimation(X_MINMAX1, c_base = 20 * [3.0], is_current=False, is_optimization=False,doe_method=DoEType.CCF)
#print(result)
# Minmax without current f_1 [%]:  0.41177440277967176  f_2 [%] 1.7477270642688498
# Minmax with current    f_1 [%]:  0.41177440278051747  f_2 [%] 3.4503854220533245
# PB with current        f_1 [%]:  0.4117744027792381   f_2 [%] 4.052060290632767
# PB without current     f_1 [%]:  0.4117744027778069   f_2 [%] 2.0494507070565464
# BB with current        f_1 [%]:  0.4117744027841387   f_2 [%] 1.0646412903552067
# BB without current     f_1 [%]:  0.4117744027839652 f_2 [%] 2.220787699305381
# CCD with current       f_1 [%]:  0.4117744027835749 f_2 [%] 4.897994378591952
# CCD without current    f_1 [%]:  0.41177440277876104 f_2 [%] 2.9297037603180076

X_MINMAX2 = [9.642648902292361, 5.282069784346017, 24.537841778121283, 8.059349224813, 12.318525759009816,
             15.019686958780929, 18.63674172150556, 15.770361021866993, 14.876436429127999, 20.0443749044710];
# costs:[0.9035269365144892, 1.50332356458337]

result = error_estimation(X_MINMAX2, c_base = 20 * [3.0], is_current=True, is_optimization=False,doe_method=DoEType.CCF)
print(result)

# PB without current ---  f_1 [%]:  0.903526936517048  f_2 [%] 2.322607440380917
# PB with current    ---  f_1 [%]:  0.9035269365172648 f_2 [%] 4.33851862275213
# Minmax with current --- f_1 [%]: 0.9035269365128196 f_2 [%] 3.1298760562339587
# BB with current         f_1 [%]:  0.9035269365159421 f_2 [%] 2.3170782478181517
# BB without current      f_1 [%]:  0.9035269365132749 f_2 [%] 1.1975813239919424
# CCD with current        f_1 [%]:  0.90352693651965 f_2 [%] 5.052053886062927
# CCD without current     f_1 [%]:  0.9035269365155951 f_2 [%] 3.0707443753592725


# X_PB1 = [15.23, 28.82, 26.92, 15.85, 15.32, 6.03, 22.24, 16.70, 10.11, 29.07]
# result = error_estimation(X_PB1, c_base = 20 * [3.0], is_current=True, is_optimization=False,doe_method=DoEType.PB)
# print(result)

# PB with    current        ---  f_1 [%]:  1.6153417501714058 f_2 [%] 4.526275441123391
# PB without current        ---  f_1 [%]:  1.6153417501723384 f_2 [%] 3.192413114995116
# PB minmax with current    ---  f_1 [%]:  1.6153417501714058 f_2 [%] 4.206917036440578
# PB minmax without current ---  f_1 [%]:  1.6153417501707554 f_2 [%] 2.472125908791747

X_PB2 = [28.21, 27.91, 24.67, 15.79, 11.82, 14.16, 14.67, 23.98, 28.49, 25.37]

# result = error_estimation(X_PB2, c_base = 20 * [3.0], is_current=False, is_optimization=False,doe_method=DoEType.MINMAX)
# print(result)

# PB with current           f_1 [%]:  18.88223516271092 f_2 [%] 1.5027055160626963
# PB without current        f_1 [%]:  18.88223516270831 f_2 [%] 2.1664114827341985
# Minmax with current       f_1 [%]:  18.8822351627074  f_2 [%] 3.7340766584760696
# Minmax without current    f_1 [%]:  18.88223516270703 f_2 [%] 2.422488723238076

X_MINMAX3 = [10.36, 6.98, 5.2, 5.16, 10.49, 19.95, 18.38, 25.16, 8.25, 20.03];

# result = error_estimation(X_MINMAX3, c_base = 20 * [3.0], is_current=False, is_optimization=False,doe_method=DoEType.CCF)
# print(result)

# Minmax without current f_1 [%]:  5.008715010714512 f_2 [%] 0.044740554106003416
# Minmax with current    f_1 [%]:  5.008715010716626 f_2 [%] 1.6271829613575421
# PB without current     f_1 [%]:  5.008715010714415 f_2 [%] 2.3879607676587957
# PB with current        f_1 [%]:  5.008715010715    f_2 [%] 3.59094294044304
# BB with current        f_1 [%]:  5.008715010713861 f_2 [%] 2.457094066575082
# BB without current     f_1 [%]:  5.0087150107146305 f_2 [%] 1.5137933105548802
# c  f_1 [%]:  5.0087150107129075 f_2 [%] 5.664387475121123
# CCF without current    f_1 [%]:  5.008715010714382 f_2 [%] 3.814060033958824

# sample from the another pareto front
X_MINMAX4 = [14.56, 6.22, 6.73, 10.62, 9.54, 21.66, 22.87, 14.26, 25.87, 11.48]
# costs:[1.9844466736266368, 2.7404648932107567]

#result = error_estimation(X_MINMAX4, c_base=20 * [3.0], is_current=True, is_optimization=False, doe_method=DoEType.CCF )
#print(result)

# Minmax without current f_1 [%]

# Minmax without current f_1 [%]:  1.972723601061034 f_2 [%] 1.1380447635083475
# Minmax with current
# PB without current     f_1 [%]:  1.9727236010613811 f_2 [%] 1.6496254396866485
# PB with current        f_1 [%]:  1.9727236010609692 f_2 [%] 3.5932499607418933
# BB with current        f_1 [%]:  1.972723601059603  f_2 [%] 2.418871097678154
# BB without current     f_1 [%]:  1.9727236010630724 f_2 [%] 1.0449829738903935
# CCF with current 2071  f_1 [%]:  1.9727236010627254 f_2 [%] 5.058276989624448
# CCF without current    f_1 [%]:  1.9727236010624438 f_2 [%] 2.663794610363991
