import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve
import pandas as pd
import os
from sklearn.metrics import auc
import csv
from decimal import *
import json
import math

#Paths
path_to_baseline_predictions = '../data/201802_pumr_baseline_prediction_177_assays.csv'
path_test_assays = '../predictions/predictions_split_1/assay_matrix_discrete_test_old_scaff.csv'
path_prediction_files = '../predictions/predictions_split_1/predictions/'
path_output_file = '../predictions/predictions_split_1/2021_03_evaluation_all_data_python.csv'

assay_type = {}


with open(path_to_baseline_predictions) as f:
	next(f)
	reader = csv.reader(f)
	for row in reader:
		assay_type[row[2]] = row[-4]


header = ['assay_id','auc','descriptor','auc_70','auc_90','ASSAY_TYPE','AP','pr_auc']

true_array_header = list(pd.read_csv(path_test_assays).columns.values)[1:]
true_array = pd.read_csv(path_test_assays).to_numpy()[:, 1:].astype(np.float64)
prediction_files = os.listdir(path_prediction_files)

results = {}

with open(path_output_file, 'w') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(header)
	for prediction_file in prediction_files:
		predictions_array = pd.read_csv(os.path.join(path_prediction_files,prediction_file)).to_numpy()[:, 1:].astype(np.float64)
	
		row = []

		aucs = []
		aps = []
		pr_aucs = []
		auc_70 = 0
		auc_90 = 0
	
		for i in range(true_array.shape[1]):
			tr = true_array[:, i]
			pr = predictions_array[:, i]
			nan_index = np.where(np.isnan(tr))
			mask=np.zeros(tr.shape[0], dtype=bool)
			mask[nan_index] = True
			row = []
			if 1.0 not in tr or (len(set(tr[~mask])) == 1 and list(set(tr[~mask]))[0] == 1.0):
				row.append(true_array_header[i])
				row.append('NA')
				row.append(prediction_file.split('.')[0].replace('predictions_',''))
				row.append('NA')
				row.append('NA')
				if true_array_header[i] in assay_type.keys():
					row.append(assay_type[true_array_header[i]])
				else:
					row.append('NA')
				row.append('NA')
				row.append('NA')
			else:
				prec, rec, _  = precision_recall_curve(tr[~mask], pr[~mask])
				pr_auc = auc(rec,prec)
				pr_aucs.append(pr_auc)
				auc_score = roc_auc_score(tr[~mask], pr[~mask])
				aucs.append(auc_score)
				ap = average_precision_score(tr[~mask], pr[~mask])
				aps.append(ap)

				row.append(true_array_header[i])
				row.append(float(Decimal(str(auc_score)[:16])))
				row.append(prediction_file.split('.')[0].replace('predictions_',''))

				if float(Decimal(str(auc_score)[:16])) > 0.7:
					auc_70 = auc_70 + 1
					row.append('TRUE')
				else:
					row.append('FALSE')
				if float(Decimal(str(auc_score)[:16])) > 0.9:
					auc_90 = auc_90 + 1
					row.append('TRUE')
				else:
					row.append('FALSE')


				if true_array_header[i] in assay_type.keys():
					row.append(assay_type[true_array_header[i]])
				else:
					row.append('NA')
				row.append(float(Decimal(str(ap)[:16])))
				row.append(float(Decimal(str(pr_auc)[:16])))

			writer.writerow(row)
	
		results[prediction_file.split('.')[0].replace('predictions_','')] = [np.mean(aucs), auc_70, auc_90, np.mean(aps), np.mean(pr_aucs), len(aucs)]

results = dict(sorted(results.items(), key=lambda item: item[1][0], reverse=True))

for key in results:
	print(key, results[key][0], results[key][1], results[key][2], results[key][3], results[key][4], results[key][5])
