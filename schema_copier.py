#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:08:14 2016

@author: alec
"""

import glob, shutil, os

def schema_copier(batch_path=None, source_path=None, user_name=None,
                  box_sync=True, overwrite=True):
    """Copies a config schema file from source file into n batches.
    Deletes any old config schemas that exist.
    By default looks in Brian Bucher's Rad. Annotation box folder under the folder name "user_name".
    If box_sync is false, must provide batch_path and source_path.
    If you do not wish to delete current config folders, set overwrite to False."""
    
    if box_sync == True:
        batchDIR = os.path.join(os.path.expanduser('~'),'Box Sync',
        'Bucher_Surgical_MIMICIII','Radiology_Annotation',user_name)
        sourceDIR=sourceDIR = os.path.join(os.path.expanduser('~'), 'Box Sync','Bucher_Surgical_MIMICIII',
        'Radiology_Annotation','source_xml')
    else:
        batchDIR=batch_path
        sourceDIR=source_path
    if os.path.exists(batchDIR) == False:
        raise ValueError("batch_path does not exist.")
    elif os.path.exists(sourceDIR) == False:
        raise ValueError("source_path does not exist.")
    else:
        pass
    sourceXML=sourceDIR+"/projectschema.xml"
    
    annotatorWorkspaceBatches = batchDIR+"//Batch*"
    print("Path to Annotator's workspace: %s"%annotatorWorkspaceBatches)
    listOfBatches = glob.glob(annotatorWorkspaceBatches)
    print("There are %d batches in this folder."%len(listOfBatches) )
    
    if overwrite==True:
        for folder in listOfBatches:
            try:
                oldConfigFolder='%s/config/'%str(folder)    
                shutil.rmtree(oldConfigFolder)
            except FileNotFoundError:
                pass
    new_files = 0
    for folder in listOfBatches:
        newConfigFolder="%s/config/"%str(folder)
        os.mkdir(newConfigFolder)
        destinationXML="%s/config/projectschema.xml"%str(folder)
        shutil.copyfile(sourceXML,destinationXML)
        new_files += 1
    print("You have added your schema to %d folders "%new_files)
    return 

        