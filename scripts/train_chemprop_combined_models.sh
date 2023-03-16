#args: $1 - input_folder, $2 - output_folder, $3 - CUDA GPU id
#this script runs hyperparameter optimazation, training of ensemble models and prediction
#
mkdir $2/predictions
mkdir $2/models

mkdir $2/models/2021-02-ge-cp-es-op
mkdir $2/models/2021-02-mobc-cp-es-op
mkdir $2/models/2021-02-ge-mobc-es-op
mkdir $2/models/2021-02-ge-mobc-cp-es-op

CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-ge-cp-es-op --no_features_scaling --gpu 0 --num_iters 20 --features_path $1/population_ge_train.npz --config_save_path $2/2021-02-ge-cp-es-op/optimized_hyperparameter.json &
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-mobc-cp-es-op --no_features_scaling --num_iters 20 --features_path $1/population_mobc_train.npz --config_save_path $2/2021-02-mobc-cp-es-op/optimized_hyperparameter.json &
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-ge-mobc-es-op --no_features_scaling --num_iters 20 --features_path $1/population_gemobc_train.npz --gpu 0 --features_only --config_save_path $2/2021-02-ge-mobc-es-op/optimized_hyperparameter.json &
CUDA_VISIBLE_DEVICES=$3 python hyperparameter_optimization.py --data_path $1/assay_matrix_discrete_train_scaff.csv --split_sizes 0.8 0.1 0.1 --dataset_type classification --save_dir $2/2021-02-ge-mobc-cp-es-op --no_features_scaling --num_iters 20 --features_path $1/population_gemobc_train.npz --gpu 0 --config_save_path $2/2021-02-ge-mobc-cp-es-op/optimized_hyperparameter.json &
wait

CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-ge-cp-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-ge-cp-es-op --features_path $1/population_ge_train.npz --no_features_scaling --quiet --show_individual_scores --ensemble_size 8 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-mobc-cp-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-mobc-cp-es-op --features_path $1/population_mobc_train.npz --no_features_scaling --quiet --show_individual_scores --ensemble_size 8 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-ge-mobc-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-ge-mobc-es-op --features_path $1/population_gemobc_train.npz --features_only --no_features_scaling --quiet --show_individual_scores --ensemble_size 8 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-ge-mobc-cp-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-ge-mobc-cp-es-op  --features_path $1/population_gemobc_train.npz --no_features_scaling --quiet --show_individual_scores --ensemble_size 8 &
wait

CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_ge_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-ge-cp-es-op --preds_path $2/predictions/predictions_ge_cp_es_op.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_mobc_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-mobc-cp-es-op --preds_path $2/predictions/predictions_mobc_cp_es_op.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_gemobc_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-ge-mobc-es-op --preds_path $2/predictions/predictions_ge_mobc_es_op.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_gemobc_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-ge-mobc-cp-es-op --preds_path $2/predictions/predictions_ge_mobc_cp_es_op.csv &
wait

echo 'Completed'
