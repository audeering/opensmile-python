///////////////////////////////////////////////////////////////////////////////////////
///////// > openSMILE configuration file for wave input <            //////////////////
/////////                                                            //////////////////
///////// (c) audEERING GmbH,                                        //////////////////
/////////     All rights reserved.                                   //////////////////
///////////////////////////////////////////////////////////////////////////////////////

[componentInstances:cComponentManager]
instance[extsinklld].type=cExternalSink
instance[extsinkfunc].type=cExternalSink

;;;;;;; sink ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[extsinklld:cExternalSink]
reader.dmLevel = \cm[sinkLevelLLD{lld}:sink level]
blocksize = \cm[blockSize{1}:block size]

[extsinkfunc:cExternalSink]
reader.dmLevel = \cm[sinkLevelFunc{func}:sink level]
blocksize = \cm[blockSize{1}:block size]
