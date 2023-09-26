///////////////////////////////////////////////////////////////////////////////////////
///////// > openSMILE configuration file for data output <           //////////////////
/////////                                                            //////////////////
///////// (c) 2014-2016 audEERING,                                   //////////////////
/////////     All rights reserved. See file COPYING for details      //////////////////
///////////////////////////////////////////////////////////////////////////////////////


/*
   This file can be included as data output file for standard feature
   extraction configuration files. It provides commandline options
   for the batch extraction GUI, and supports LLD and Functionals (summaries)
   saving.

   It requires the main extractor configuration file to provide the following
   data memory levels:  lld and func
 */

;;;;;;;;; output LLD features to CSV ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[componentInstances:cComponentManager]
instance[lld_csv_sink].type=cCsvSink
instance[func_csv_sink].type=cCsvSink

[lld_csv_sink:cCsvSink]
reader.dmLevel = lld
filename=\cm[lld_csv_output{?}:output csv file for LLD, disabled by default ?, only written if filename given]
append = \cm[lld_csv_append{0}:set to 1 to append to the LLD output csv file, default is not to append]
timestamp = \cm[lld_csv_timestamp{1}:set to 0 to suppress timestamp column, default is 1, i.e. to show timestamp in second column]
number = 0
printHeader = \cm[lld_csv_header{1}:set to 0 to suppress header line with feature names, default is 1, i.e. to show header line]
errorOnNoOutput = 1

[func_csv_sink:cCsvSink]
reader.dmLevel = func
filename=\cm[func_csv_output{?}:output CSV file for summarised parameters, set to a valid filename to enable this output sink, data is appended if file exists]
append=\cm[func_csv_append{0}:set to 0 to disable appending to an existing csv parameter summary file, given by the csvoutput option]
frameIndex=0
frameTime=\cm[func_csv_timestamp{1}:set to 0 to suppress timestamp column, default is 1, i.e. to show timestamp in second column]
errorOnNoOutput = 1
printHeader = \cm[func_csv_header{1}:set to 0 to suppress header line with feature names, default is 1, i.e. to show header line]

