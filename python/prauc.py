import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve
import pandas as pd
import os
from sklearn.metrics import auc
import csv
from decimal import *


if __name__ == "__main__":
	assay_type = {}

	split = 'MOBC_cv4' # This script processes one split at a time
	header = ['assay_id','auc','descriptor','auc_50','auc_70','auc_90','AP','pr_auc']

	true_array_header = list(pd.read_csv('../predictions/{}/assay_matrix_discrete_test_old_scaff.csv'.format(split)).columns.values)[1:]
	true_array = pd.read_csv('../predictions/{}/assay_matrix_discrete_test_old_scaff.csv'.format(split)).to_numpy()[:, 1:].astype(np.float64)
	prediction_files = [i for i in os.listdir('../predictions/{}/predictions/'.format(split)) if '.csv' in i]

	results = {}

	with open('../predictions/{}/2022_01_evaluation_all_data.csv'.format(split), 'w') as f:
		writer = csv.writer(f, lineterminator = '\n')
		writer.writerow(header)
		for prediction_file in prediction_files:
			predictions_array = pd.read_csv('../predictions/{0}/predictions/{1}'.format(split,prediction_file)).to_numpy()[:, 1:].astype(np.float64)
			row = []

			aucs = []
			aps = []
			pr_aucs = []
			auc_50 = 0
			auc_70 = 0
			auc_90 = 0

			good_aps = []
			bad_aps = []

		
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
					if float(Decimal(str(auc_score)[:16])) > 0.5:
						auc_50 = auc_50 + 1
						row.append('TRUE')
					else:
						row.append('FALSE')
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

					row.append(float(Decimal(str(ap)[:16])))
					row.append(float(Decimal(str(pr_auc)[:16])))

				writer.writerow(row)
				results[prediction_file.split('.')[0].replace('predictions_','')] = [np.mean(aucs), auc_50, auc_70, auc_90, np.mean(aps), np.mean(pr_aucs), len(aucs)]

	results = dict(sorted(results.items(), key=lambda item: item[1][0], reverse=True))

	for key in results:
		print(key, results[key][0], results[key][1], results[key][2], results[key][3], results[key][4], results[key][5], results[key][6])
