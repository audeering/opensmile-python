///////////////////////////////////////////////////////////////////////////////////////
///////// > openSMILE configuration file for wave input <            //////////////////
/////////                                                            //////////////////
///////// (c) audEERING GmbH,                                        //////////////////
/////////     All rights reserved.                                   //////////////////
///////////////////////////////////////////////////////////////////////////////////////

[componentInstances:cComponentManager]
instance[extsource].type=cExternalAudioSource

[extsource:cExternalAudioSource]
writer.dmLevel=wave
writer.levelconf.growDyn=1
writer.levelconf.isRb=0
sampleRate=\cm[sampleRate{16000}:sample rate]
nBits=\cm[nBits{16}:sample bits]
channels=\cm[channels{1}:channel size]
