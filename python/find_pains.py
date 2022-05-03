import csv
import numpy as np
from tqdm import tqdm
from rdkit import Chem
from rdkit import DataStructs
from chemprop.data.utils import get_data_from_smiles

from rdkit.Chem.FilterCatalog import *

### Path to the assay matrix here
assay_train_file = '../data/assay_matrix_discrete_270_assays.csv'
###

smiles = []
smiles_ = []
with open(assay_train_file) as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        smiles.append([row[0]])
        smiles_.append(row[0])

data = get_data_from_smiles(smiles)
data = data.mols(flatten=True)

params = [FilterCatalogParams(),FilterCatalogParams(),FilterCatalogParams(),FilterCatalogParams()]
params[0].AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
params[1].AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
params[2].AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B)
params[3].AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C)
catalog_pains = FilterCatalog(params[0])
catalog_painsA = FilterCatalog(params[1])
catalog_painsB = FilterCatalog(params[2])
catalog_painsC = FilterCatalog(params[3])

entries_pains = []
entries_painsA = []
entries_painsB = []
entries_painsC = []
entries_painsAll = []

for i in range(len(data)):
    if catalog_pains.HasMatch(data[i]):
        entries_pains.append(i)
    if catalog_painsA.HasMatch(data[i]):
        entries_painsA.append(i)
    if catalog_painsB.HasMatch(data[i]):
        entries_painsB.append(i)
    if catalog_painsC.HasMatch(data[i]):
        entries_painsC.append(i)
    if catalog_pains.HasMatch(data[i]) or catalog_painsA.HasMatch(data[i]) or  catalog_painsB.HasMatch(data[i]) or catalog_painsC.HasMatch(data[i]):
        entries_painsAll.append(i)
        
print(len(entries_pains),len(entries_painsA),len(entries_painsB),len(entries_painsC), len(entries_painsAll) )
print( len(set(entries_pains + entries_painsA + entries_painsB + entries_painsC + entries_painsAll)))

all_matches = set(entries_pains + entries_painsA + entries_painsB + entries_painsC + entries_painsAll)

np.savez('compound_analysis.npz', pains_overall = list(all_matches), pains_a = list(set(entries_painsA)), \
         pains_b = list(set(entries_painsB)), pains_c = list(set(entries_painsC)) )