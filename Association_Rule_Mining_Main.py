import pandas as pd
from itertools import combinations
import Dataset_Processor
import Rule_Generation


'''
Function to create frequent itemsets

Returns a dictionary of frequent itemsets (key) and their respective support count (value).
Prints frequent itemset count.
'''
def frequent_itemset_generation(transformed_df, candidate_itemset_list, min_support_count):
    frequent_item_support_dict = {}
    frequent_itemset_count = 0
    for itemset in candidate_itemset_list:
        operation_df = transformed_df
        for item in itemset:
            operation_df = operation_df.loc[operation_df[item] != 0]
        count = len(operation_df.index)
        if count >= min_support_count:
            frequent_item_support_dict[tuple(itemset)] = count
            frequent_itemset_count = frequent_itemset_count + 1

    print("Frequent itemset count = ", frequent_itemset_count)
    print(" ")
    return_list = [frequent_item_support_dict, frequent_itemset_count]
    return return_list


'''
Function to create itemsets by the F(k−1) × F1 method
'''
def F_1_itemset_generation(transformed_df, final_set_list, k, min_support_count):
    item_list = []
    k_one = list(final_set_list[0].keys())
    k_one.sort()
    k_minus_one = list(final_set_list[k-2].keys())
    for i in k_minus_one:
        for j in k_one:
            itemset = list(i)
            if j not in itemset:
                itemset.append(j)
                itemset.sort()
                item_list.append(itemset)

    #Removing duplicates
    candidate_itemset_list_set = set(tuple(x) for x in item_list)
    candidate_itemset_list = [list(x) for x in candidate_itemset_list_set]

    #Printing counts
    print("Itemset counts for k = ", k)
    print("Candidate itemset count = ", len(candidate_itemset_list))

    ret_list = frequent_itemset_generation(transformed_df, candidate_itemset_list, min_support_count)
    frequent_item_support_dict = ret_list[0]
    frequent_count = ret_list[1]

    return_list = [frequent_item_support_dict, len(candidate_itemset_list), frequent_count]
    return return_list


'''
Function to create itemsets by the F(k−1) × F(k-1) method
'''
def F_k_minus_one_itemset_generation(transformed_df, final_set_list, k, min_support_count):
    item_list = []
    itemset = []
    two = list(final_set_list[k-2].keys())

    for i in two:
        itemset_1 = list(i)
        itemset_1.sort()
        for j in two:
            itemset_2 = list(j)
            itemset_2.sort()
            match = True
            if itemset_1[-1] != itemset_2[-1]:
                for l in range(k-2):
                    if itemset_1[l] != itemset_2[l]:
                        match = False
                        break
                if match is True:
                    itemset = list(itemset_1)
                    itemset.append(itemset_2[-1])
                    itemset.sort()
                    if itemset not in item_list:
                        item_list.append(itemset)

    # Printing counts
    print("Itemset counts for k = ", k)
    print("Candidate itemset count = ", len(item_list))
    if not item_list:
        frequent_item_support_dict = {}
        frequent_count = 0
    else:
        ret_list = frequent_itemset_generation(transformed_df, item_list, min_support_count)
        frequent_item_support_dict = ret_list[0]
        frequent_count = ret_list[1]

    return_list = [frequent_item_support_dict, len(item_list), frequent_count]
    return return_list


'''
Function to calculate the number of closed frequent itemsets
'''
def closed_frequent_itemsets_count(final_set_list, k):

    first_keys = list(final_set_list[k-1].keys())
    second_keys = list(final_set_list[k].keys())
    closed_frequent_itemsets = 0
    for first_item_tuple in first_keys:
        first_item_list = list(first_item_tuple)
        first_item_list.sort()
        is_closed = True
        for second_item_tuple in second_keys:
            subsets = []
            for sets in combinations(list(second_item_tuple), k):
                set_list = list(sets)
                set_list.sort()
                subsets.append(set_list)
            if first_item_list in subsets:
                if final_set_list[k-1].get(first_item_tuple) == final_set_list[k].get(second_item_tuple):
                    is_closed = False
                    break
        if is_closed is True:
            closed_frequent_itemsets = closed_frequent_itemsets + 1
    return closed_frequent_itemsets


'''
Function to calculate the number of closed frequent itemsets
'''
def maximal_frequent_itemsets_count(final_set_list, k):

    first_keys = list(final_set_list[k-1].keys())
    second_keys = list(final_set_list[k].keys())
    maximal_frequent_itemsets = 0
    for first_item_tuple in first_keys:
        first_item_list = list(first_item_tuple)
        first_item_list.sort()
        is_maximal = True
        for second_item_tuple in second_keys:
            subsets = []
            for sets in combinations(list(second_item_tuple), k):
                set_list = list(sets)
                set_list.sort()
                subsets.append(set_list)
            if first_item_list in subsets:
                is_maximal = False
                break
        if is_maximal is True:
            maximal_frequent_itemsets = maximal_frequent_itemsets + 1
    return maximal_frequent_itemsets



'''
Start of the main function
'''
if __name__ == '__main__':
    # Ask user for inputs
    print("Enter the csv file path:")
    file_path = input()

    print("Enter comma separated column names:")
    column_names = input().split(",")
    # Read csv file to create a data frame
    original_df = pd.read_csv(file_path, names=column_names, encoding='utf-8')


    # Convert into a binary transaction dataset
    print("Does the dataset have a numerical columns (Enter '1'for Yes, '2'for No)")
    response = int(input())
    if response == 1:
        print("Enter comma separated column names which have numeric values:")
        num_column_names = input().split(",")
        numeric_transformed_df = Dataset_Processor.numerical_col_processing(num_column_names, original_df)
        returned_list = Dataset_Processor.transform_dataset(column_names, numeric_transformed_df)
    else:
        returned_list = Dataset_Processor.transform_dataset(column_names, original_df)

    transformed_df = returned_list[0]
    candidate_count_k1 = returned_list[1]

    # Ask user for other inputs
    print("Enter minimum support value (0-1):")
    min_support = float(input())
    min_support_count = round(min_support * len(transformed_df.index))
    print("Enter candidate itemset generation type ['1' for F(k-1) x F(1)] ['2' for F(k-1) x F(k-1)]:")
    generation_type = int(input())

    final_set_list=[]
    total_candidate_count=0
    total_frequent_count=0

    # Frequent itemset generation for k = 1
    frequent_item_support_dict = {}
    frequent_count_k1 = 0
    for column in transformed_df:
        count = len((transformed_df.loc[transformed_df[column] == 1]).index)
        if count >= min_support_count:
            frequent_item_support_dict[column] = count
            frequent_count_k1 = frequent_count_k1 + 1
    final_set_list.append(frequent_item_support_dict)
    # Printing counts for k = 1
    print("Itemset counts for k = 1")
    print("Candidate itemset count = ", candidate_count_k1)
    print("Frequent itemset count = ", frequent_count_k1)
    print(" ")
    total_candidate_count = total_candidate_count + candidate_count_k1
    total_frequent_count = total_frequent_count + frequent_count_k1

    # Frequent itemset generation for k = 2
    candidate_itemset_list = []
    for element in combinations(list(frequent_item_support_dict.keys()), 2):
        temp = list(element)
        temp.sort()
        element = tuple(temp)
        candidate_itemset_list.append(element)
    candidate_count_k2 = len(candidate_itemset_list)
    print("Itemset counts for k = 2")
    print("Candidate itemset count = ", candidate_count_k2)
    ret_list = frequent_itemset_generation(transformed_df, candidate_itemset_list, min_support_count)
    final_set_list.append(ret_list[0])
    total_candidate_count = total_candidate_count + candidate_count_k2
    total_frequent_count = total_frequent_count + ret_list[1]

    # Frequent itemset generation for the k = n
    k = 2
    generation_complete = False
    while generation_complete is False:
        k = k + 1
        if generation_type == 1:
            ret_list = F_1_itemset_generation(transformed_df, final_set_list, k, min_support_count)
            final_set_list.append(ret_list[0])
            total_candidate_count = total_candidate_count + ret_list[1]
            total_frequent_count = total_frequent_count + ret_list[2]

        else:
            ret_list = F_k_minus_one_itemset_generation(transformed_df, final_set_list, k, min_support_count)
            final_set_list.append(ret_list[0])
            total_candidate_count = total_candidate_count + ret_list[1]
            total_frequent_count = total_frequent_count + ret_list[2]

        if not final_set_list[k-1]:
            generation_complete = True

    #Print total counts
    print("Total candidate itemset count = ", total_candidate_count)
    print("Total frequent itemset count = ", total_frequent_count)
    print(" ")

    # Calculating closed frequent itemset count
    closed_frequent_itemsets = 0
    for index in range(1, k):
        total = closed_frequent_itemsets_count(final_set_list, index)
        closed_frequent_itemsets = closed_frequent_itemsets + total
    print("Closed frequent itemset count: ", closed_frequent_itemsets)

    # Calculating maximal frequent itemset count
    maximal_frequent_itemsets = 0
    for index in range(1, k):
        total = maximal_frequent_itemsets_count(final_set_list, index)
        maximal_frequent_itemsets = maximal_frequent_itemsets + total
    print("Maximal frequent itemset count: ", maximal_frequent_itemsets)
    print(" ")

    print("Enter minimum confidence value for confidence based rule pruning (%):")
    min_confidence = input()
    print (" ")

    print("##########Rule generation commences (Brute Force Method)...")
    print(" ")
    ret_list = Rule_Generation.rule_generator_brute_force(final_set_list, float(min_confidence), len(transformed_df.index))
    rule_dict = ret_list[0]
    rules_lift_dict = ret_list[1]

    # Generating top ten rules (Brute Force Method)
    top_ten_rules = sorted(rule_dict, key=rule_dict.get, reverse=True)[:10]
    print("Top ten rules (Brute Force Method and Confidence):")
    for rule in top_ten_rules:
        rule_list = list(rule)
        print(str(list(rule_list[0]))+"---->"+str(list(rule_list[1]))+"   "+"Confidence: "+str(rule_dict[rule]))
    print(" ")

    top_ten_rules = sorted(rules_lift_dict, key=rules_lift_dict.get, reverse=True)[:10]
    print("Top ten rules (Brute Force Method and List):")
    for rule in top_ten_rules:
        rule_list = list(rule)
        print(
            str(list(rule_list[0])) + "---->" + str(list(rule_list[1])) + "   " + "Lift: " + str(rules_lift_dict[rule]))
    print(" ")

    # Generating rules (Confidence based pruning)
    print("##########Rule generation commences (Confidence based pruning)...")
    print(" ")
    rule_dict = Rule_Generation.rule_gererator_confidence_pruning(final_set_list, float(min_confidence))

    # Generating top ten rules
    top_ten_rules = sorted(rule_dict, key=rule_dict.get, reverse=True)[:10]
    print("Top ten rules (Confidence based pruning):")
    for rule in top_ten_rules:
        rule_list = list(rule)
        print(str(list(rule_list[0]))+"---->"+str(list(rule_list[1]))+"   "+"Confidence: "+str(rule_dict[rule]))

