import csv
import numpy as np

results = {}
with open('../predictions/scaffold_median_python_jan22.csv', 'r') as f:
	next(f)
	reader = csv.reader(f)
	for row in reader:
		if row[2] not in results.keys():
			results[row[2]] = {}
		if row[0] not in results[row[2]].keys():
			results[row[2]][row[0]] = []

		#row[5]=AUC90, row[4]=AUC70, row[3]=AUC50
		results[row[2]][row[0]] = row[5]


cs_mo_counts = 0
for assay in results['cp_es_op'].keys():
	if results['cp_es_op'][assay] == 'TRUE' or results['mobc_es_op'][assay] == 'TRUE':
		cs_mo_counts = cs_mo_counts + 1


print('CS+MO', cs_mo_counts)

ge_mo_counts = 0
for assay in results['ge_es_op'].keys():
	if results['ge_es_op'][assay] == 'TRUE' or results['mobc_es_op'][assay] == 'TRUE':
		ge_mo_counts = ge_mo_counts + 1


print('GE+MO', ge_mo_counts)


ge_cs_counts = 0

for assay in results['ge_es_op'].keys():
	if results['ge_es_op'][assay] == 'TRUE' or results['cp_es_op'][assay] == 'TRUE':
		ge_cs_counts = ge_cs_counts + 1

print('GE+CS', ge_cs_counts)


ge_cs_mobc_counts = 0

for assay in results['ge_es_op'].keys():
	if results['ge_es_op'][assay] == 'TRUE' or results['cp_es_op'][assay] == 'TRUE' or results['mobc_es_op'][assay] == 'TRUE':
		ge_cs_mobc_counts = ge_cs_mobc_counts + 1

print('GE+CS+MO', ge_cs_mobc_counts)



ge_cs_LF = 0
for assay in results['ge_es_op'].keys():
	if results['late_fusion_cs_ge'][assay] == 'TRUE' or results['ge_es_op'][assay] == 'TRUE' or results['cp_es_op'][assay] == 'TRUE':
		ge_cs_LF = ge_cs_LF + 1


print('GE+CS + late', ge_cs_LF)


ge_mo_LF = 0
for assay in results['ge_es_op'].keys():
	if results['late_fusion_ge_mobc'][assay] == 'TRUE' or results['mobc_es_op'][assay] == 'TRUE' or results['ge_es_op'][assay] == 'TRUE':
		ge_mo_LF = ge_mo_LF + 1


print('GE+MO + late', ge_mo_LF)


cs_mo_LF = 0

for assay in results['ge_es_op'].keys():
	if results['late_fusion_cs_mobc'][assay] == 'TRUE' or results['mobc_es_op'][assay] == 'TRUE' or results['cp_es_op'][assay] == 'TRUE':
		cs_mo_LF = cs_mo_LF + 1


print('CS+MO + late', cs_mo_LF)



ge_cs_mobc_LF = 0
for assay in results['ge_es_op'].keys():
	if results['late_fusion_cs_ge_mobc'][assay] == 'TRUE' or results['ge_es_op'][assay] == 'TRUE' or results['cp_es_op'][assay] == 'TRUE' or results['mobc_es_op'][assay] == 'TRUE':
		ge_cs_mobc_LF = ge_cs_mobc_LF + 1


print('GE+CS+MO late', ge_cs_mobc_LF)