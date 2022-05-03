from tqdm import tqdm
import numpy as np
import seaborn as sb
from matplotlib import pyplot as plt
import subprocess
from multiprocessing import Process

class Starter(object):
    def __init__(self, test_indicies, similarity_fingerprints, name):
        self.test_indicies = test_indicies
        self.similarity_fingerprints = similarity_fingerprints
        self.coords = coords
        self.name = name

    def main(self):
        self.similarities_train_test = []
        self.similarities_train = []
        self.similarities_test = []
        for coord in tqdm(self.coords): 
            xin = coord[0] in self.test_indicies
            yin = coord[1] in self.test_indicies
            if (xin and not yin) or (not xin and yin):
                self.similarities_train_test.append(self.similarity_fingerprints[coord[0], coord[1]])
            if (not xin and not yin):
                self.similarities_train.append(self.similarity_fingerprints[coord[0], coord[1]])
            if (xin and yin):
                self.similarities_test.append(self.similarity_fingerprints[coord[0], coord[1]])
        
        self.plot_()
        
    def plot_(self):
        x = [(self.similarities_train_test,'blue', 'Training vs Test set similarity'), (self.similarities_train, 'red', 'Training set inner similarity') , (self.similarities_test,'green', 'Test set inner similarity')]
        plt.figure(figsize=(12,12))
        
        for a in range(3):
            sb.distplot(x[a][0], hist=False, kde_kws = {'shade': True, 'linewidth': 3}, label = x[a][2], color = x[a][1])

        plt.legend(prop={'size': 16})
        plt.xlabel('Similarity', size = 16)
        plt.ylabel('Density', size = 16)
        plt.savefig(self.name)


if __name__=="__main__":
    similarity_fingerprints = '../data/similarity_fingerprints.npz'
    with open(similarity_fingerprints, "rb") as data:
        sim_fp = np.load(data) 
        sim_fp = sim_fp['features']

    with open('../data/compounds16978to16170.npy', 'rb') as data:
        compounds_final_indicies_from_16978 = np.load(data)
    
    mask=np.zeros( (16978, 16978), dtype=bool)
    mask[compounds_final_indicies_from_16978, compounds_final_indicies_from_16978] = True
    sim_fp = sim_fp[np.ix_(compounds_final_indicies_from_16978,compounds_final_indicies_from_16978)]
        
    coords = []
    for x in range(sim_fp.shape[0]):
        for y in range(sim_fp.shape[0]):
            if x < y:
                coords.append((x,y))
    
    
    #For plotting of scaffold-based data use this
    
    #with open('../data/scaffold_based_split_jan22.npz', 'rb') as data:
    #    indicies = np.load(data, allow_pickle=True)
    #    indicies = indicies['features']
        

    #For morphology just replace the input file and output files
    with open('../data/geneexp_clusters_size_constrained_jan22.npz', 'rb') as data:
        indicies = np.load(data, allow_pickle=True) 
        indicies = indicies['features']
        
    def run(*fns):
        proc = []
        for fn in fns:
            p = Process(target=fn.main)
            p.start()
            proc.append(p)
        for p in proc:
            p.join()


    a1 = Starter(np.array(np.argwhere(indicies==0)), sim_fp, '../plots/similarities/GEcv0_jan22.svg')
    a2 = Starter(np.array(np.argwhere(indicies==1)), sim_fp, '../plots/similarities/GEcv1_jan22.svg')
    a3 = Starter(np.array(np.argwhere(indicies==2)), sim_fp, '../plots/similarities/GEcv2_jan22.svg')
    a4 = Starter(np.array(np.argwhere(indicies==3)), sim_fp, '../plots/similarities/GEcv3_jan22.svg')
    a5 = Starter(np.array(np.argwhere(indicies==4)), sim_fp, '../plots/similarities/GEcv4_jan22.svg')
    run(a1,a2,a3,a4,a5)