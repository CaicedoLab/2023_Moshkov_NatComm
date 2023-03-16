#args: $1 - input_folder, $2 - output_folder, $3 - CUDA GPU id
#this script runs hyperparameter optimazation, training of ensemble models and prediction
 
mkdir $2/models/2021-02-cp-es-op-bal
mkdir $2/models/2021-02-cpcl-es-op-bal
mkdir $2/models/2021-02-mo-es-op-bal
mkdir $2/models/2021-02-ge-es-op-bal
mkdir $2/models/2021-02-ges-es-op-bal
mkdir $2/models/2021-02-mowh-es-op-bal


CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-cp-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-cp-es-op-bal --no_features_scaling --quiet --show_individual_scores --class_balance --ensemble_size 8 --gpu 0 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-cpcl-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-cpcl-es-op-bal --features_path $1/population_cp_train.npz --no_features_scaling --quiet --features_only --class_balance --ensemble_size 8 --gpu 0 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-mo-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-mo-es-op-bal --features_path $1/population_mo_train.npz --no_features_scaling --quiet --features_only --class_balance --ensemble_size 8 &
wait
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-ge-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-ge-es-op-bal --features_path $1/population_ge_train.npz --no_features_scaling --quiet --features_only --class_balance --ensemble_size 8 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-ges-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-ges-es-op-bal --features_path $1/population_ge_scaled_train.npz --no_features_scaling --quiet --features_only --class_balance --ensemble_size 8 &
CUDA_VISIBLE_DEVICES=$3 python train.py --data_path $1/assay_matrix_discrete_train_scaff.csv --config_path $2/2021-02-mobc-es-op/optimized_hyperparameter.json --split_sizes 0.9 0.1 0 --dataset_type classification --save_dir $2/models/2021-02-mobc-es-op-bal --features_path $1/population_mobc_train.npz --no_features_scaling --quiet --features_only --class_balance --ensemble_size 8 &
wait

CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-cp-es-op-bal --preds_path $2/predictions/predictions_cp_es_op-bal.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_cp_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-cpcl-es-op-bal --preds_path $2/predictions/predictions_cpcl_es_op_fixed-bal.csv &
wait
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_mo_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-mo-es-op-bal --preds_path $2/predictions/predictions_mo_es_op-bal.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_ge_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-ge-es-op-bal --preds_path $2/predictions/predictions_ge_es_op-bal.csv &
wait
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_ge_scaled_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-ges-es-op-bal --preds_path $2/predictions/predictions_ges_es_op-bal.csv &
CUDA_VISIBLE_DEVICES=$3 python predict.py --test_path $1/assay_matrix_discrete_test_scaff.csv  --gpu 0  --features_path $1/population_mobc_test.npz  --no_features_scaling  --checkpoint_dir  $2/models/2021-02-mobc-es-op-bal --preds_path $2/predictions/predictions_mobc_es_op-bal.csv &
wait

echo 'Completed'
