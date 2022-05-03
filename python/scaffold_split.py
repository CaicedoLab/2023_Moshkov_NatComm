import csv
import os
import pickle
import random
import numpy as np
from copy import deepcopy

from chemprop.data import scaffold_to_smiles
from chemprop.data.utils import get_data_from_smiles, split_data, filter_invalid_smiles
from chemprop.data.scaffold import scaffold_split

        
def split_indices(all_indices,
                  num_folds,
                  data,
                  shuffle = True):
    num_data = len(all_indices)
    scaffold_to_indices = scaffold_to_smiles(data.mols(flatten=True), use_indices=True)
    print(len(scaffold_to_indices))
    print(scaffold_to_indices)
    index_sets = sorted(list(scaffold_to_indices.values()),
                        key=lambda index_set: len(index_set),
                        reverse=True)
    fold_indices = [[] for _ in range(num_folds)]
    for s in index_sets:
        length_array = [len(fi) for fi in fold_indices]
        min_index = length_array.index(min(length_array))
        fold_indices[min_index] += s
    if shuffle:
        random.shuffle(fold_indices)

    return fold_indices


def create_crossval_splits():
    assay_file = '../data/assay_matrix_discrete_270_assays.csv'

    smiles = []
    smiles_ = []

    with open(assay_file) as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            smiles.append([row[0]])
            smiles_.append(row[0])
            
    
            
    data = get_data_from_smiles(smiles)
    all_indices = list(range(len(data)))    
    fold_indicies = split_indices(all_indices, num_folds=5, data=data)
    array = np.array(fold_indicies)
    print(array.shape)
    np.savez('../data/scaffold_based_split_jan22.npz', features = array)

if __name__ == '__main__':
    random.seed(0)
    create_crossval_splits()
