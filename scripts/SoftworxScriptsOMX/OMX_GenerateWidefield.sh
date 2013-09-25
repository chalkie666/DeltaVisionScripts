#!/bin/bash
#command file for CreateWF
#for comments and questions, contact kay.oliver.schink@rr-research.no
# usage - drag and drop a .dv file containing SIM raw data onto the icon of this script to generate a pseudo widefield image.
export infile=$1
/usr/local/softWoRx/bin/i386/OMXGenerateWFImage \
"$infile" \
"${infile%.*}_WF.dv" &> "${infile%.*}_wf.log"
#
