#args: $1 - input_folder, $2 - output_folder, $3 - CUDA GPU id
#this script runs hyperparameter optimazation, training of ensemble models and prediction
#

mkdir $2/predictions
mkdir $2/models

mkdir $2/models/2021-02-cp-es-op
mkdir $2/models/2021-02-cpcl-es-op
mkdir $2/models/2021-02-mo-es-op
mkdir $2/models/2021-02-ge-es-op
mkdir $2/models/2021-02-ges-es-op
mkdir $2/models/2021-02-mobc-es-op

CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-cp-es-op --no_features_scaling --num_iters 20 --config_save_path $2/2021-02-cp-es-op/optimized_hyperparameter.json &
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-cpcl-es-op --features_path $1/population_cp_train.npz --no_features_scaling --num_iters 20 --features_only --config_save_path $2/2021-02-cpcl-es-op/optimized_hyperparameter.json &
wait
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-mo-es-op --features_path $1/population_mo_train.npz --no_features_scaling --num_iters 20 --features_only --config_save_path $2/2021-02-mo-es-op/optimized_hyperparameter.json &
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-ge-es-op --features_path $1/population_ge_train.npz --no_features_scaling --num_iters 20 --features_only --config_save_path $2/2021-02-ge-es-op/optimized_hyperparameter.json &
wait
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-ges-es-op --features_path $1/population_ge_scaled_train.npz --no_features_scaling --num_iters 20 --features_only --config_save_path $2/2021-02-ges-es-op/optimized_hyperparameter.json &
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-mobc-es-op --features_path $1/population_mobc_train.npz --no_features_scaling --num_iters 20 --features_only --config_save_path $2/2021-02-mobc-es-op/optimized_hyperparameter.json &
wait

CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-cp-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-cp-es-op --no_features_scaling --quiet --show_individual_scores --ensemble_size 8 --gpu 0 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-cpcl-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-cpcl-es-op --features_path $1/population_cp_train.npz --no_features_scaling --quiet --features_only --ensemble_size 8 --gpu 0 &
wait
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-mo-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-mo-es-op --features_path $1/population_mo_train.npz --no_features_scaling --quiet --features_only --ensemble_size 8 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-ge-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-ge-es-op --features_path $1/population_ge_train.npz --no_features_scaling --quiet --features_only --ensemble_size 8 &
wait
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-ges-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-ges-es-op --features_path $1/population_ge_scaled_train.npz --no_features_scaling --quiet --features_only --ensemble_size 8 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-mobc-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-mobc-es-op --features_path $1/population_mobc_train.npz --no_features_scaling --quiet --features_only --ensemble_size 8 &
wait

CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-cp-es-op --preds_path $2/predictions/predictions_cp_es_op.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_cp_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-cpcl-es-op --preds_path $2/predictions/predictions_cpcl_es_op_fixed.csv &
wait
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_mo_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-mo-es-op --preds_path $2/predictions/predictions_mo_es_op.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_ge_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-ge-es-op --preds_path $2/predictions/predictions_ge_es_op.csv &
wait
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_ge_scaled_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-ges-es-op --preds_path $2/predictions/predictions_ges_es_op.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_mobc_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-mobc-es-op --preds_path $2/predictions/predictions_mobc_es_op.csv &
wait

echo 'Completed'
