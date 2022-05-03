import csv
import numpy as np
from decimal import *

results = {}
for i in range(5):
	with open('../predictions/chemical_jan22_cv' + str(i) + '/2022_01_evaluation_all_data_python.csv', 'r') as f:
		next(f)
		reader = csv.reader(f)
		for row in reader:
			if row[2] not in results.keys():
				results[row[2]] = {}
			if row[0] not in results[row[2]].keys():
				results[row[2]][row[0]] = []

			if row[1] != 'NA':
				results[row[2]][row[0]].append(float(Decimal(row[1])))


header = ['assay_id','auc','descriptor', 'auc_50', 'auc_70','auc_90']
with open('../predictions/scaffold_mean_python_jan22.csv', 'w') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(header)
	for modal in results.keys():
		auc_50 = 0
		auc_70 = 0
		auc_90 = 0
		for assay in results[modal].keys():

			row = [assay]
			mean_auc = np.mean( results[modal][assay])
			row.append(float(Decimal(str(mean_auc)[:16])))
			row.append(modal)
			if float(Decimal(str(mean_auc)[:16])) > 0.5:
				auc_50 = auc_50 + 1
				row.append('TRUE')
			else:
				row.append('FALSE')
			if float(Decimal(str(mean_auc)[:16])) > 0.7:
				auc_70 = auc_70 + 1
				row.append('TRUE')
			else:
				row.append('FALSE')
			
			if float(Decimal(str(mean_auc)[:16])) > 0.9:
				auc_90 = auc_90 + 1
				row.append('TRUE')
			else:
				row.append('FALSE')

			writer.writerow(row)

		print('50', modal, auc_50)		
		print('70', modal, auc_70)
		print('90', modal, auc_90)


print('median')
with open('../predictions/scaffold_median_python_jan22.csv', 'w') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(header)
	for modal in results.keys():
		auc_50 = 0
		auc_70 = 0
		auc_90 = 0
		for assay in results[modal].keys():
			row = [assay]
			median_auc = np.median( results[modal][assay])
			row.append(float(Decimal(str(median_auc)[:16])))
			row.append(modal)
			if float(Decimal(str(median_auc)[:16])) > 0.5:
				auc_50 = auc_50 + 1
				row.append('TRUE')
			else:
				row.append('FALSE')
			if float(Decimal(str(median_auc)[:16])) > 0.7:
				auc_70 = auc_70 + 1
				row.append('TRUE')
			else:
				row.append('FALSE')
			
			if float(Decimal(str(median_auc)[:16])) > 0.9:
				auc_90 = auc_90 + 1
				row.append('TRUE')
			else:
				row.append('FALSE')

			writer.writerow(row)

		print('50', modal, auc_50)
		print('70', modal, auc_70)
		print('90', modal, auc_90)
