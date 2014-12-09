#!/bin/bash
#command file for CreateWF
#for comments and questions, contact kay.oliver.schink@rr-research.no

# Copyright (C) 2014 GE Healthcare
#  
# License: See LICENSE.txt file 

# This script is now obsolete since this functionality is now a menu function in the GE Healthcare SoftWoRx v6 software

# usage - drag and drop a .dv file containing SIM raw data onto the icon of this script to generate a pseudo widefield image.
export infile=$1
/usr/local/softWoRx/bin/i386/OMXGenerateWFImage \
"$infile" \
"${infile%.*}_WF.dv" &> "${infile%.*}_wf.log"
#
