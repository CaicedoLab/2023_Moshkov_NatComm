import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve
import pandas as pd
import os
from sklearn.metrics import auc
import csv
from decimal import *
import json
import math
from deepchem import metrics
from rdkit.ML.Scoring.Scoring import CalcBEDROC, CalcEnrichment
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve

split = 'chemical_jan22_cv4'
header = ['assay_id','descriptor','EF1%', 'EF5%', 'EF10%']

true_array_header = list(pd.read_csv('../predictions/' + split + '/assay_matrix_discrete_test_old_scaff.csv').columns.values)[1:]
true_array = pd.read_csv('../predictions/' + split + '/assay_matrix_discrete_test_old_scaff.csv').to_numpy()[:, 1:].astype(np.float64)
prediction_files = [i for i in os.listdir('../predictions/' + split + '/predictions/') if '.csv' in i]

results = {}

with open('./' + split + '/2022_01_evaluation_all_data_python_EF.csv', 'w') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(header)
	for prediction_file in prediction_files:
		predictions_array = pd.read_csv('./' + split + '/predictions/' + prediction_file).to_numpy()[:, 1:].astype(np.float64)
		row = []
		for i in range(true_array.shape[1]):
			tr = true_array[:, i]
			pr = predictions_array[:, i]
			nan_index = np.where(np.isnan(tr))
			mask=np.zeros(tr.shape[0], dtype=bool)
			mask[nan_index] = True
			row = []

			if 1.0 not in tr or (len(set(tr[~mask])) == 1 and list(set(tr[~mask]))[0] == 1.0):
				row.append(true_array_header[i])
				row.append(prediction_file.split('.')[0].replace('predictions_',''))
				row.append('NA')
				row.append('NA')
				row.append('NA')
			else:	
				scores = list(zip(tr[~mask], pr[~mask]))
				scores = sorted(scores, key=lambda pair: pair[1], reverse=True)
				tmp = CalcEnrichment(scores, 0, [0.01, 0.05, 0.1])
				if len(tmp) == 1:
					ef1, ef5, ef10 = tmp[0], np.nan, np.nan
				elif len(tmp) == 2:
					ef1, ef5, ef10 = tmp[0], tmp[1], np.nan
				else:
					ef1, ef5, ef10 = tmp[0], tmp[1], tmp[2]

				row.append(true_array_header[i])
				row.append(prediction_file.split('.')[0].replace('predictions_',''))
				row.append(float(Decimal(str(np.format_float_positional(ef1))[:16])))
				row.append(float(Decimal(str(np.format_float_positional(ef5))[:16])))
				row.append(float(Decimal(str(np.format_float_positional(ef10))[:16])))

			writer.writerow(row)