///////////////////////////////////////////////////////////////////////////////////////
///////// > openSMILE configuration file for wave input <            //////////////////
/////////                                                            //////////////////
///////// (c) audEERING GmbH,                                        //////////////////
/////////     All rights reserved.                                   //////////////////
///////////////////////////////////////////////////////////////////////////////////////

[componentInstances:cComponentManager]
instance[extsink].type=cExternalSink

;;;;;;; sink ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[extsink:cExternalSink]
reader.dmLevel = \cm[sinkLevel{func}:sink level]
blocksize = \cm[blockSize{1}:block size]
