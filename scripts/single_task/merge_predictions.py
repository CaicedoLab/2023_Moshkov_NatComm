import pandas as pd
import os

# Merge predictions of single assays into one matrix
if __name__=="__main__":
    split = 'single_assay_chemical_jan22_cv1'
    pred_folder = '/path/data//output/predictions/{}'.format(split)
    prediction_filenames = sorted([i for i in os.listdir(pred_folder)])
    df = pd.read_csv(pred_folder + prediction_filenames[0])
    for i in range(1,len(prediction_filenames)):
        df = pd.merge(df, pd.read_csv(pred_folder + prediction_filenames[i]), on='smiles')
        
    df.to_csv(pred_folder + 'predictions_cp_es_op.csv', index=False)
    
