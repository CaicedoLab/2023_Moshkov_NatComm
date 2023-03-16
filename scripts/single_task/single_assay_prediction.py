import os
import sys

if __name__=="__main__":
    root_folder = '/raid/data/PUMA/PUMA/4publication/data/single_assay_chemical_jan22_cv1/'
    for i in range(1,271):
        command = 'CUDA_VISIBLE_DEVICES=2 python predict.py --test_path {0}/assay_matrix_discrete_test_scaff_{1}.csv  --gpu 0 --no_features_scaling  --checkpoint_dir  {0}/models/assay_{1} --preds_path {0}/output/predictions/predictions_cp_es_op_{1}.csv'.format(root_folder, i)
        os.system(command)