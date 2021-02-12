# chemprop based assay prediction 
#
# Requirements: 
# * Cuda environment
# * installed ChemProp repository, see https://github.com/swansonk14/chemprop (conda method is recommended)
# * assay data 
# * additional genetic and morphological features stored as npz files (see script )
#
#  see 201910_save_csv_as_npz.ipynb, sample code to export as npz:
#
# ```{python}
# import numpy
# import pandas
# import os 
# 
# def save_as_npz(input_path, output_path):
#     profiles = pandas.read_csv(input_path)
#     del profiles['Metadata_broad_sample_simple']
#     df = numpy.array(profiles)
#     numpy.savez_compressed(output_path, features = df)
# ```
# Tim Becker 


# prepare workspace
input_folder=/storage/data/tim/2018_01_09_PUMA_CBTS/workspace/analysis/scaffold_based_chemprop
output_folder=/storage/data/tim/2018_01_09_PUMA_CBTS/workspace/results/scaffold_based/chemprop
mkdir $output_folder/predictions
mkdir $output_folder/models

## baseline model using chemical descriptors 
# As a baseline, we train a ChemProp model and evaluate it on the hold out data set. This model is based on 
# chemical descriptors only using default parameters, i.e. without hyperparameter optimization. 
 
mkdir $output_folder/models/2019-11-cp

## train with default parmameter 
CUDA_VISIBLE_DEVICES=0 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-cp \
--no_features_scaling \
--quiet 

## predict hold out 
python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-cp \
 --preds_path $output_folder/predictions/predictions_cp.csv

## result: 

# ChemProp model with optimized parameter 
mkdir $output_folder/models/2019-11-cp-op

## hyperparameter optimization
CUDA_VISIBLE_DEVICES=3 python hyperparameter_optimization.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.8 0.1 0.1 \
--dataset_type classification \
--save_dir $output_folder/2019-11-cp-op \
--no_features_scaling \
--num_iters 20 \
--config_save_path $output_folder/2019-11-cp-op/optimized_hyperparameter.json

## train model with optimized parameter
CUDA_VISIBLE_DEVICES=0 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--config_path $output_folder/2019-11-cp-op/optimized_hyperparameter.json \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-cp-op \
--no_features_scaling \
--quiet \
--show_individual_scores

## predict hold out 
python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-cp-op \
 --preds_path $output_folder/predictions/predictions_cp_op.csv


# Train and evaluate a ChemProp model based on morphological features alone 
mkdir $output_folder/models/2019-11-mo
CUDA_VISIBLE_DEVICES=3 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-mo \
--features_path $input_folder/population_mo_train.npz \
--no_features_scaling \
--quiet \
--features_only 

python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --features_path $input_folder/population_mo_test.npz \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-mo \
 --preds_path $output_folder/predictions/predictions_mo.csv \


# Train and evaluate a ChemProp model based on genetic features alone 
mkdir $output_folder/models/2019-11-ge
CUDA_VISIBLE_DEVICES=0 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-ge \
--features_path $input_folder/population_ge_train.npz \
--no_features_scaling \
--quiet \
--features_only 

python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --features_path $input_folder/population_ge_test.npz \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-ge \
 --preds_path $output_folder/predictions/predictions_ge.csv

# Train and evaluate a ChemProp model based on genetic and morphological features 
mkdir $output_folder/models/2019-11-ge_mo
CUDA_VISIBLE_DEVICES=1 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-ge_mo \
--features_path $input_folder/population_gemo_train.npz \
--no_features_scaling \
--quiet \
--features_only 

python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --features_path $input_folder/population_gemo_test.npz \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-ge_mo \
 --preds_path $output_folder/predictions/predictions_ge_mo.csv 

######

# Train and evaluate a ChemProp model based on morphological and chemprop features
mkdir $output_folder/models/2019-11-mo-cp
CUDA_VISIBLE_DEVICES=3 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-mo-cp \
--features_path $input_folder/population_mo_train.npz \
--no_features_scaling \
--quiet 

python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --features_path $input_folder/population_mo_test.npz \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-mo-cp \
 --preds_path $output_folder/predictions/predictions_mo_cp.csv


# Train and evaluate a ChemProp model based on genetic and chemprop features
mkdir $output_folder/models/2019-11-ge-cp
CUDA_VISIBLE_DEVICES=3 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-ge-cp \
--features_path $input_folder/population_ge_train.npz \
--no_features_scaling \
--quiet 

python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --features_path $input_folder/population_ge_test.npz \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-ge-cp \
 --preds_path $output_folder/predictions/predictions_ge_cp.csv


# Train and evaluate a ChemProp model based on genetic, morphological and chemprop features
mkdir $output_folder/models/2019-11-ge-mo-cp
CUDA_VISIBLE_DEVICES=3 python train.py \
--data_path $input_folder/assay_matrix_discrete_train_scaff.csv \
--split_sizes 0.9 0.1 0 \
--dataset_type classification \
--save_dir $output_folder/models/2019-11-ge-mo-cp \
--features_path $input_folder/population_gemo_train.npz \
--no_features_scaling \
--quiet 

python predict.py --test_path $input_folder/assay_matrix_discrete_test_scaff.csv \
 --gpu 1 \
 --features_path $input_folder/population_gemo_test.npz \
 --no_features_scaling \
 --checkpoint_dir  $output_folder/models/2019-11-ge-mo-cp \
 --preds_path $output_folder/predictions/predictions_ge_mo_cp.csv
