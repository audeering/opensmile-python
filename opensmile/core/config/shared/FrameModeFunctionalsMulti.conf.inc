
;; set this to override the previously included BufferModeRb.conf.inc (in GeMAPS sets only) for the functionals
;; or (in all other sets), define the RbConf here to save memory on the functionals levels:
;writer.levelconf.growDyn = 0
;writer.levelconf.isRb = 1
;writer.levelconf.nT = 5

frameMode = list
frameList = \cm[frameList(F){0.0s-0.0s}:list with frame end and stop times separated by comma, e.g. 1.0s-1.5s,2.0s-2.5s]
frameSize = 0
frameStep = 0
frameCenterSpecial = left
