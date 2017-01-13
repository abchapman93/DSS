#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 12:00:51 2017

@author: alec
"""
import os
import glob
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt



def dict_of_lengths(batches,path):
    """Returns a dictionary of notes and their lengths."""
    dictionary = defaultdict(int)
    batch_count = 0
    note_count = 0
    for batch in batches:
        batch_count += 1
        batch_notes = [os.path.join(path,batch,x) for x in os.listdir(batch)]
        for note in batch_notes:
            #print(note)
            note_count += 1
            with open(note,'r') as f0:
                text = ''
                text += f0.read()
                dictionary[os.path.basename(note)] = len(text)
    return dictionary

def note_lengths_summary(dictionary,path,batch_naming):
    """Gives a summary of the number of notes in batches and their lengths.
    Takes as arguments a dictionary of lengths, path to batches, and batch naming schema."""
    list_of_batches = glob.glob(path+batch_naming)
    batch_count = 0
    note_count = 0
    for batch in list_of_batches:
        batch_count += 1
    for note in dictionary:
        note_count += 1
    largest_length = max(dictionary.values())
    smallest_length = min(dictionary.values())
    print('Number of batches: %d'%batch_count)
    print('Number of notes: %d'%note_count)
    print('Average length of notes: %d'%np.mean(list(dictionary.values())))
    for note in dictionary:
        if dictionary[note] == largest_length:
            print('Largest note: %s, %d characters'%(note,dictionary[note]))
    for note in dictionary:
        if dictionary[note] == smallest_length:
            print('Smallest note: %s, %d characters'%(note,dictionary[note]))
    return
    
def outlier_ident(dictionary,lower_thresh=None,upper_thresh=None):
    """Identifies any notes of unusual length.
    Takes as arguments a dictionary of note lengths, lower thresh,
    and upper thresh.
    By default, threshes are set as 2 standard deviations away from mean."""
    mean_length = np.mean(list(dictionary.values()))
    std = np.std(list(dictionary.values()))
    if lower_thresh == None:
        lower_thresh = mean_length - 2*std
    if upper_thresh == None:
        upper_thresh = mean_length + 2*std
    low_outliers = {}
    high_outliers = {}
    for note in dictionary:
        if dictionary[note] <= lower_thresh:
            low_outliers[note] = dictionary[note]
        if dictionary[note] >= upper_thresh:
            high_outliers[note] = dictionary[note]
    print('Low outliers:\n\nHigh outliers:')
    return low_outliers, high_outliers
    