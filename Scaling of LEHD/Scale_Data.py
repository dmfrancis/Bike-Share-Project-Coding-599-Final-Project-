import pandas as pd
import geopandas as gp

START_BUFFER_PATH = 'Outputs/Buffers/Split Buffers/'

YEAR = 2009

#MODE = 'MUNI Rail'

KEEP = ['EDHLTH_RAC_SCALED', 'EDHLTH_WAC_SCALED',
       'EMP_RAC_SCALED', 'EMP_WAC_SCALED', 'LEISER_RAC_SCALED',
       'LEISER_WAC_SCALED', 'OTHER_RAC_SCALED', 'OTHER_WAC_SCALED',
       'RETAIL_RAC_SCALED', 'RETAIL_WAC_SCALED','No']
       
       
SCALE_LIST = ['EDHLTH_RAC', 'EDHLTH_WAC',
       'EMP_RAC', 'EMP_WAC', 'LEISER_RAC',
       'LEISER_WAC', 'OTHER_RAC', 'OTHER_WAC',
       'RETAIL_RAC', 'RETAIL_WAC']

       

       

       
def scale(scale_list,df,keep):
    """
    function that scales a list of columns by a specified column (SPLIT_RATIO) and selects out columns of interest.
    
    scale_list = a list of column names that need to be scaled (string)
    df = dataframe that contains the columns needing to be scaled and a scaler-column (SPLIT_RATIO)
    keep = a list of columns that are of interest at the end. Filters out the unscalled columns. 
    
    """
  
    for column in scale_list:
        name = column + '_SCALED'
        df[name] = df[column]*df['SPLIT_RATIO']

    df2 = df[keep].groupby(by = 'No',as_index = False).sum()
    return df2





if __name__ == "__main__":
    
    buffers = [START_BUFFER_PATH + 'co_Split_Buffers.csv',START_BUFFER_PATH + 'oh_Split_Buffers.csv', START_BUFFER_PATH + 'tn_Split_Buffers.csv',START_BUFFER_PATH + 'ky_Split_Buffers.csv',START_BUFFER_PATH  + 'mn_Split_Buffers.csv']
               
    for buffer in buffers:
        
        print('Processing buffer ' + str(buffer))


        
        keep = KEEP
        scale_list = SCALE_LIST
            
        
        print('Reading in the files!')
        
        split = pd.read_csv(buffer)
        
        if buffer == buffers[4]:
            split['No'] = split.Number
            
        else:
            split['No'] = split['No'] 
        
        print('Scaling the Data!')
        split_scaled = scale(scale_list, split, keep)
        
        print('Saving all Files!')
        
        if buffer == buffers[0]:
            split_scaled.to_csv('Outputs/CO_LEHD_Estimation_File.csv')
        
        elif buffer == buffers[1]:
            split_scaled.to_csv('Outputs/OH_LEHD_Estimation_File.csv')
        
        elif buffer == buffers[2]:
            split_scaled.to_csv('Outputs/TN_LEHD_Estimation_File.csv')
        elif buffer == buffers[3]:
            split_scaled.to_csv('Outputs/KY_LEHD_Estimation_File.csv')
        elif buffer == buffers[4]:
            split_scaled.to_csv('Outputs/MN_LEHD_Estimation_File.csv')

    print('ALL DONE TIME FOR MONTY PYTHON!')