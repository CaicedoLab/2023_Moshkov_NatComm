import csv
import numpy as np
from tqdm import tqdm
from rdkit import Chem
from rdkit import DataStructs
from chemprop.data.utils import get_data_from_smiles
from chemprop.features.features_generators import morgan_binary_features_generator

# Generate Morgan fingerprints and get compound similarity matrix, 
# the output of this script is available on Zenodo (see dataset link in the ReadMe).

if __name__ == "__main__":
    smiles_list_file = '../assay_data/smiles.txt'

    smiles = []
    smiles_ = []
    with open(smiles_list_file) as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            smiles.append([row[0]])
            smiles_.append(row[0])
                
    fingerprints = []
    data = get_data_from_smiles(smiles)
    data = data.mols(flatten=True)
    for i in range(len(data)):
        mf = morgan_binary_features_generator(data[i])
        fingerprints.append(mf)
        
    fingerprints = np.array(fingerprints)
    np.savez('fingerprints.npz', features = fingerprints)

    fps = []
    for i in range(len(data)):
        fps.append(Chem.RDKFingerprint(data[i]))

    similarity = np.zeros([16978, 16978])
    for (x, y), _ in tqdm(np.ndenumerate(similarity)):
        similarity[x, y] = DataStructs.FingerprintSimilarity(fps[x], fps[y])
        
    np.savez('similarity_fingerprints.npz', features = similarity)