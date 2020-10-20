
///////////////////////////////////////////////////////////////////////////////////////
///////// > openSMILE configuration file <                           //////////////////
///////// > basic functionals <                                      //////////////////
///////// (c) audEERING GmbH,                                        //////////////////
/////////     All rights reserved.                                   //////////////////
///////////////////////////////////////////////////////////////////////////////////////

/*
Basic functionals:
min, max, range, range-ratio, mean, stddev, linear slope & errorQ, quad slope & error Q
*/

[componentInstances:cComponentManager]
instance[basic_func].type=cFunctionals

[basic_func:cFunctionals]
reader.dmLevel=is13_lld_nzsmo;is13_lldA_smo;is13_lldB_smo;is13_lld_nzsmo_de;is13_lldA_smo_de;is13_lldB_smo_de
writer.dmLevel=compare2016_func
copyInputName = 1
\{\cm[bufferModeRbConf]}
\{\cm[frameModeFunctionalsConf{../shared/FrameModeFunctionals.conf.inc}:path to included config to set frame mode for all functionals]}
functionalsEnabled=Regression;Moments;Percentiles
Regression.linregc1 = 1
Regression.linregc2 = 0
Regression.linregerrA = 0
Regression.linregerrQ = 1
Regression.qregc1 = 1
Regression.qregc2 = 0
Regression.qregc3 = 0
Regression.qregerrA = 0
Regression.qregerrQ = 1
Regression.centroid = 0
Regression.oldBuggyQerr = 0
Regression.normInputs = 1
Regression.normRegCoeff = 2
Regression.doRatioLimit = 1
Moments.variance = 0
Moments.stddev = 1
Moments.skewness = 0
Moments.kurtosis = 0
Moments.amean = 1
Moments.doRatioLimit = 1
Percentiles.quartiles = 0
Percentiles.iqr = 0
Percentiles.iqq = 0
Percentiles.percentile[0] = 0.06
Percentiles.percentile[1] = 0.94
Percentiles.pctlrange[0] = 0-1
; NOTE: in compare2016_basic, pctlquotient was never used
;  as the binary had the option, but it was not implemented.
; Percentiles.pctlquotient[0] = 0-1
Percentiles.interp = 1

