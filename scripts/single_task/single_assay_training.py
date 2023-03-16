import os
import sys

# Training for single assays
if __name__=="__main__":
    split = 'chemical_jan22_cv1'
    root_folder = '/path/data/single_assay_{}/'.format(split)
    old_folder = '/path/4publication/data/{}/output/'.format(split)
    os.makedirs(root_folder + 'outputs/models/', exist_ok=True)
    os.makedirs(root_folder + 'outputs/predictions/', exist_ok=True)
    # Each assay has a separate folder
    for i in range(1,271):
        os.makedirs(root_folder + 'outputs/models/assay_{}'.format(i), exist_ok=True)
        command = 'CUDA_VISIBLE_DEVICES=2 python train.py --data_path {0}/assay_matrix_discrete_train_scaff_{1}.csv --config_path {2}/2021-02-cp-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir {0}/models/assay_{1} --no_features_scaling --quiet --show_individual_scores --class_balance --ensemble_size 8 --gpu 0'.format(root_folder, i, old_folder)
        os.system(command)