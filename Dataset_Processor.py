import numpy as np
import pandas as pd
import statistics


'''
Function to convert numerical dataframe columns into categorical data by binning
'''
def numerical_col_processing(numeric_column_names, dataset_df):

    for col_name in numeric_column_names:
        value_list = list(dataset_df[col_name])
        value_list.sort()
        max_value = dataset_df[col_name].max()
        min_value = dataset_df[col_name].min()
        first_median = statistics.median(value_list)

        break_index = 0
        temp_list1 = []
        for i in value_list:
            if i < first_median:
                temp_list1.append(i)
            elif i == first_median:
                temp_list1.append(i)
                break_index = value_list.index(i)
            else:
                break
        second_median = statistics.median(temp_list1)

        temp_list2 = []
        for j in range(break_index, len(value_list)):
            temp_list2.append(value_list[j])
        third_median = statistics.median(temp_list2)

        bins = [min_value-1, second_median, first_median, third_median, max_value+1]
        group_names = [str(min_value)+"-"+str(second_median), str(second_median)+"-"+str(first_median), str(first_median)+"-"+str(third_median), str(third_median)+"-"+str(max_value)]

        dataset_df[col_name] = pd.cut(dataset_df[col_name], bins, labels=group_names)
    return dataset_df


'''
Function to convert dataframe to a binary representation
'''
def transform_dataset(column_names, dataset_df):

    processed_dataset_col_names = []
    return_list = []
    for name in column_names:
        sub_names = list(pd.unique(dataset_df[name]))
        for each_sub_name in sub_names:
            processed_dataset_col_names.append(str(name)+"_"+str(each_sub_name))

    zero_data = np.zeros(shape=(len(dataset_df),len(processed_dataset_col_names)), dtype = np.int8)
    processed_dataset_df = pd.DataFrame(zero_data, columns=processed_dataset_col_names)

    for index in range(len(dataset_df)):
        original_row = list(dataset_df.ix[index])
        for col_index in range(len(column_names)):
            derived_column = str(column_names[col_index])+"_"+str(original_row[col_index])
            processed_dataset_df[derived_column][index] = 1

    return_list.append(processed_dataset_df)
    return_list.append(len(processed_dataset_col_names))
    return return_list





