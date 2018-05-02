import geopandas as gp
import pandas as pd
import datetime
import numpy as np

#set which buffer shapefiles that are going to be processed
BUFFERS_FILE = 'Outputs/Buffers/5.28Buffer_Indexed.shp'

#change the paths to do a different set of census blocks or to save the output in a different directory
BLOCKS_FILE_START = 'Inputs/LEHD Data/Processed Data/Shapefile/'


OUTFILE_CSV_START = 'Outputs/Buffers/Split Buffers/'
OUTFILE_SHP_START = 'Outputs/Buffers/Split Buffers/'

YEARS = [2015]

# leave out ky for now, need grid of stations from Danny

STATES = ['ky']

#set the index column which each row has a unique identifier
INDEX = 'No'


def blocks_area(blocks):

    blocks['AREA'] = blocks['ALAND10']*0.0000229568
    
    return blocks

    
def clean_area(blocks):

    if blocks['ALAND00'] == 0:
        blocks['ALAND00'] = blocks['ALAND']
    else:
        blocks['ALAND00'] = blocks['ALAND00']
    return blocks['ALAND00']    

        

def clean_area_column(row):
   
    if np.isnan(row['AREA_y']):
        area = row['AREA_x']
    else:
        area = row['AREA_x']
    return area
        

def intersect(buffers,blocks,index):
    """
    function to intersect buffers with census blocks and calculate the portion of area that the original census block is within the buffer
    
    buffers = shapefile with all of the buffers
    blocks = shapefile with all of the census blocks
    
    """
    #loop through the buffers one stop at a time
    final_buffers = pd.DataFrame()
    count = 0
    
    #set the start time to check how long it takes to intersect one buffer
    start = datetime.datetime.now()

    for buf in buffers[index]:
    #select out one of the buffers to intersect
        buffer = buffers[buffers[index] == buf]
    #select out the census blocks that intersect the buffer
        buffer.crs = {'init':'epsg:4269'}
        blocks.crs = buffer.crs
        
        blocks_select = gp.sjoin(blocks,buffer,op = 'intersects')
        #identity keeps only the left geodataframe and splits it based on the right geodataframe
        identity = gp.overlay(buffer,blocks_select,how = 'identity')
        identity.crs = {'init' :'epsg:4269'}
        
    #reproject the split buffer into stateplane so that the split polygons' area can be calculated
        stateplane = identity.to_crs(epsg = '6420')
        
    #convert ft^2 to acres
        stateplane['SPLIT_AREA'] = stateplane.area*0.0000229568


        stateplane['SPLIT_RATIO'] = stateplane['SPLIT_AREA']/stateplane['AREA']
       
        data = stateplane[stateplane[index] == buf]
        
        final_buffers = final_buffers.append(data)
        count = count+1
        end = datetime.datetime.now()
        time = end - start

        print(str(count) + ' buffer(s) took ' + str((time.seconds/60)) + ' minutes')
    return final_buffers
    

if __name__ == "__main__":
    for y in YEARS:
        
        for state in STATES:
            print('Working on the state of ' + str(state))

            if state == 'ky':
                fips_list = ['067','209','239','113']
                census_state = '_21_'
                state_for_col = 'KY'
                fips = '067'
            elif state == 'co':
                fips = '013'
                census_state = '_08_'
                state_for_col = 'CO'

            elif state == 'tn':
                fips = '065'
                census_state = '_47_'
                state_for_col = 'TN'

            elif state == 'oh':
                fips = '049'
                census_state = '_39_'
                state_for_col = 'OH'

            elif state == 'mn':
                fips = '053'
                census_state = '_27_'
                state_for_col = 'MN'
            else:
                print('bad state!')
            
            count = 0
            year = y
            buffers_path = BUFFERS_FILE
            
				
            blocks_path = BLOCKS_FILE_START + state + '_' + fips + '_Employment.shp'
            
            print('Started New Buffer Titled: ' + buffers_path)


            buffers = gp.read_file(buffers_path)
            blocks = gp.read_file(blocks_path)
            buffers.crs = {'init':'epsg:4269'}
            blocks.crs = {'init':'epsg:4269'}
            #buffers = buffers[buffers['State'] == state_for_col]
            
            #have to comment this line out for MN data
            blocks = blocks[blocks['COUNTYFP10'].isin(fips_list)]
            
            # calculate the area of the cenusus blocks (in acres)
            blocks = blocks_area(blocks)
            #blocks['AREA'] = blocks.apply(lambda row: clean_area_column(row),axis = 1)
			print(buffers.columns)
            # function that intersects the census blocks with the buffers and calculates ratio of the split area over the original block area
            split_buffers = intersect(buffers,blocks,INDEX)
            
           #write the intersected tenth-mile buffers to a csv and shapefile
            #split_buffers.to_file(OUTFILE_SHP_START + state + '_Split_Buffers.shp', driver = 'ESRI Shapefile')
            
            
            split_buffers.to_csv(OUTFILE_CSV_START + state + '_Split_Buffers.csv')
            
            count = count + 1

                
                
    print('ALL DONE TIME FOR SOME HALO!!!')

    
    
    
# import geopandas as gp
# import pandas as pd
# import datetime
# import numpy as np

# #set which buffer shapefiles that are going to be processed
# BUFFERS_FILE = 'Outputs/Buffers/Quarter_Buffer.shp'

# #change the paths to do a different set of census blocks or to save the output in a different directory
# BLOCKS_FILE = 'Inputs/LEHD Data/Processed Data/Shapefile/067_Employment.shp'


# OUTFILE_CSV = 'Output/Buffers/Split Buffers/Split_Buffers_Quarter.csv'
# OUTFILE_SHP = 'Output/Buffers/Split Buffers/Split_Buffers_Quarter.shp'

# YEARS = [2015]

# def blocks_area(blocks):
    # """
    # function to calculate the area (in acres) of census blocks 
    
    # blocks = shapefile with all of the census blocks 
    
    # """

    # blocks['AREA'] = blocks['ALAND10']*0.0000229568
    
    # return blocks

    
# def clean_area(blocks):

    # """
    # San Mateo and San Francisco have two different names for their area columns. This function sets the areas to one column name, ALAND00.
    
    # blocks = census blocks dataframe with area columns 
    
   # """

    # if blocks['ALAND00'] == 0:
        # blocks['ALAND00'] = blocks['ALAND']
    # else:
        # blocks['ALAND00'] = blocks['ALAND00']
    # return blocks['ALAND00']    

        

# def clean_area_column(row):
    # """
    # function to clean the area column. There are two data sets; one being the 2010 pop/housing and the other being the LEHD data. The pop/housing data has better coverage, but didnt have area pre-calculated. LEHD data does have area pre-calculated. LEHD block areas are used unless it is missing, where the user-calculated areas for pop/housing blocks are used.

    # row = using the apply method with lambda allows python to iterate through the rows of a dataframe. This takes in one of the rows. 
    
    # Example: df['new_column'] = df.apply(lambda row: function(row))
    # """
    # if np.isnan(row['AREA_y']):
        # area = row['AREA_x']
    # else:
        # area = row['AREA_x']
    # return area
        

# def intersect(buffers,blocks):
    # """
    # function to intersect buffers with census blocks and calculate the portion of area that the original census block is within the buffer
    
    # buffers = shapefile with all of the buffers
    # blocks = shapefile with all of the census blocks
    
    # """
    # #loop through the buffers one stop at a time
    # final_buffers = pd.DataFrame()
    # count = 0
    
    # #set the start time to check how long it takes to intersect one buffer
    # start = datetime.datetime.now()

    # for buffer in buffers.No.unique():
    # #select out one of the buffers to intersect
        # buffer = buffers[buffers['No'] == buffer]
    # #select out the census blocks that intersect the buffer
        # print(buffer.head())
        # print(blocks.head())
        # blocks_select = gp.sjoin(blocks,buffer,op = 'intersects')
       
    # #identity keeps only the left geodataframe and splits it based on the right geodataframe
        # identity = gp.overlay(buffer,blocks_select,how = 'identity')
        # identity.crs = {'init' :'epsg:4269'}
        
    # #reproject the split buffer into stateplane so that the split polygons' area can be calculated
        # stateplane = identity.to_crs(epsg = '6420')
        
    # #convert ft^2 to acres
        # stateplane['SPLIT_AREA'] = stateplane.area*0.0000229568


        # stateplane['SPLIT_RATIO'] = stateplane['SPLIT_AREA']/stateplane['AREA']
       
        # data = stateplane[stateplane['STOP_ID'] == stop]
        
        # final_buffers = final_buffers.append(data)
        # print(len(final_buffers.STOP_ID.unique()))
        # count = count+1
        # end = datetime.datetime.now()
        # time = end - start

        # print(str(count) + ' buffer(s) took ' + str((time.seconds/60)) + ' minutes')
    # return final_buffers
    

# if __name__ == "__main__":
    # for y in YEARS:
        
        # count = 0
        # year = y
        # buffers_path = BUFFERS_FILE
        
        # blocks_path = BLOCKS_FILE
        
        # print('Started New Buffer Titled: ' + buffers_path)


        # buffers = gp.read_file(buffers_path)
        # blocks = gp.read_file(blocks_path)
        # buffers.crs = {'init':'epsg:4269'}
        # blocks.crs = {'init':'epsg:4269'}

        
        # # calculate the area of the cenusus blocks (in acres)
        # blocks = blocks_area(blocks)
        # #blocks['AREA'] = blocks.apply(lambda row: clean_area_column(row),axis = 1)
       
        # # function that intersects the census blocks with the buffers and calculates ratio of the split area over the original block area
        # split_buffers = intersect(buffers,blocks)
        
       # #write the intersected tenth-mile buffers to a csv and shapefile
        # split_buffers.to_file(OUTFILE_SHP_START + str(year) + OUTFILE_SHP_END[count])
        # split_buffers.to_csv(OUTFILE_CSV_START + str(year) + OUTFILE_CSV_END[count])
        
        # count = count + 1

                
                
    # print('ALL DONE TIME FOR SOME HALO!!!')

