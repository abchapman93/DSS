#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:39:22 2016

@author: alec
"""
import glob, shutil, os

def adjud2Saved(adjud_path,batch_name='/batch*'):
    """moves xml files from 'adjudication' to 'saved' folder
    these can then be exported to excel through eHOST.
    Takes as argument the path to the adjudicator's folder and the naming schema for batches.
    By default, naming schema is '/batch*'
    If there is already an excel file in the saved folder,
    it is copied into the new folder."""
    #find adjudication and saved folder
    
    if os.path.exists(adjud_path) == False:
        return 'Path does not exist.'
    #return os.listdir(adjud_path)
    old_saved = os.path.join(adjud_path,batch_name,'saved')
    #return old_saved
    new_saved = old_saved
    #if already annotation excel sheet, move it to adjudication folder
    adjud_batches = adjud_path+batch_name
    list_batches = glob.glob(adjud_batches)
    #return old_saved, new_saved, list_batches
    for folder in list_batches:
        #return os.listdir(folder)
        old_saved = os.path.join(folder,'saved')
        new_saved = old_saved
        adjud_folder = os.path.join(folder,'adjudication')
        if os.path.exists(adjud_folder) == True:
            #check if there's already an .xlsx file
            for file in folder:
                try:
                    if file[-5:] == ';.xlsx':
                        shutil.copyfile(old_saved+'/'+file,adjud_folder+'/'+file)
                        print(file)
                        return
                except FileNotFoundError:
                    pass
            #delete old saved folder
            shutil.rmtree(old_saved)
            os.rename(adjud_folder,new_saved) 
            print('Your files have been moved to %s'%new_saved)
        else:
            pass
            #print("There is no adjudication folder in %s"%folder)
          
        
        
    return os.listdir(adjud_path)