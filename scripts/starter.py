import os
import sys
import subprocess
from multiprocessing import Process

# Example training starter, replace shell scripts in main (ChemProp class) and GPU ids and splits in main
# Also adjust the path in main (ChemProp class)
class ChemProp(object):
    def __init__(self, gpu, split):
        self.gpu = gpu
        self.split = split

    def main(self):
        os.makedirs('/path/data/{}/output/'.foramt(self.split), exist_ok = True)
        os.system('sh train_chemprop_models_single_models_balanced.sh /path/data/{0}/ /path/data/{0}/output/ {1}'.foramt(self.split, self.gpu))


if __name__=="__main__":
    def run(*fns):
        proc = []
        for fn in fns:
            p = Process(target=fn.main)
            p.start()
            proc.append(p)
        for p in proc:
            p.join()

    # several trainings can be run on a single GPU, add or remove object passed to run() method
    aa = ChemProp('3', 'chemical_jan22_cv0')
    bb = ChemProp('3', 'chemical_jan22_cv1')

    run(aa,bb)
