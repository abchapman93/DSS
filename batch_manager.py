#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:01:22 2016

@author: alec
"""

import glob, shutil, os
import pandas as pd

def schema_copier(batch_path=None, source_path=None, user_name=None,
                  overwrite=True):
    """Copies a config schema file from source file into n batches.
    Deletes any old config schemas that exist.
    If you do not wish to delete current config folders, set overwrite to False."""
    
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


    
def adjud2Saved(adjud_path, batch_name='/Batch*'):
    """Iterates through all batch folders in a directory.
    Replaces the files in 'saved' with the files in 'adjudication'.
    These adjudicated xml files can then be exported to excel through eHOST.
    Takes as argument the path to the adjudicator's folder and the naming schema for batches.
    By default, naming schema is '/batch*'"""
    
    if os.path.exists(adjud_path) == False:
        return 'Path does not exist.'
    
    adjud_batches = adjud_path+batch_name

    list_batches = glob.glob(adjud_batches)
    batch_count = 0
    affected_folders = []
    
    for folder in list_batches:
        print(folder)
        old_saved = os.path.join(folder,'saved')
        adjud_folder = os.path.join(folder,'adjudication')
        new_saved = old_saved
        if os.path.exists(adjud_folder) == True:
            batch_count += 1
            affected_folders.append(os.path.basename(folder))
            
            shutil.rmtree(old_saved)
            shutil.copytree(adjud_folder, new_saved)
            
        else:
            print ("There is no adjudication folder in %s"%folder)
    print("You copied files from adjud to save in %d folders"%batch_count)   
    return affected_folders
    
def annotations2Excel(annot_path, output_file='all_annotations.xlsx', batch_name='/Batch*',first_worksheet=True):
    """Finds all Annotations.xlsx files in a directory.
    Copies the content of each file into destination file.
    Provides one excel worksheet with all annotations."""
    if os.path.exists(annot_path) == False:
        return 'Path does not exist.'
    output_path = os.path.join(annot_path, output_file)
    annot_batches = annot_path+batch_name

    affected_folders = []
    annotations_files = []
    batch_count = 0
    file_count = 0
    list_batches = glob.glob(annot_batches)
    #create an excel writer
    data_frames = []
    
    for folder in list_batches:
        batch_count += 1
        affected_folders.append(folder)
        
        #find annotations.xlsx
        annotations_sheet = os.path.join(folder, "saved", "annotations.xlsx")
        if os.path.exists(annotations_sheet) == True:
            annotations_files.append(annotations_sheet)
            file_count += 1
            
            #read in the header of the first file
            if file_count == 1 and first_worksheet == True:
                data_frame = pd.read_excel(annotations_sheet)
                header_row = data_frame.head()
            else:
                data_frame = pd.read_excel(annotations_sheet, skiprows=0)
            data_frames.append(data_frame)
            #return data_frame.dropna(how='all')
        else:
            pass
    all_data_concat = pd.concat(data_frames, axis=0, ignore_index=True)
    writer = pd.ExcelWriter(os.path.join(annot_path, output_file))
    all_data_concat.to_excel(writer, sheet_name="all_annotations", index=False)
    
    #return data_frames
    print("You concatened %d files and saved them in %s"%(file_count,output_path))
    return
        
    
    