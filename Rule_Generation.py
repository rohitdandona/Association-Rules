from itertools import chain, combinations


'''
Function to generate subsets of a list of elements.

For compute_type '1', the function generates all possible combinations of different lengths
For compute_type '2', the function generates possible combinations of length k-1 (k is the length of the list of elements)

Returns a list of subsets
'''
def subset_generator(itemset, compute_type):
    subsets = []
    if len(itemset) == 1:
        subsets.append(itemset[0])
        return subsets
    else:
        if compute_type == 1:
            sets = chain.from_iterable(combinations(itemset, r) for r in range(len(itemset) + 1))
        else:
            sets = combinations(itemset, len(itemset) - 1)
        for i in sets:
            temp = list(i)
            if not temp or len(temp) == len(itemset):
                continue
            else:
                subsets.append(temp)
        return subsets


'''
Function to generate rules via the Brute force method

a) Returns the number of computations made for rule generation
b) Returns the number of rules generated (> minimum confidence)
c) Returns the number of rules generated (lift)
'''
def rule_generator_brute_force (final_set_list, min_confidence, row_count):
    rules_dict = {}
    rules_lift_dict = {}
    k_candidate_rule_processed_count = 0
    total_rule_count = 0
    lift_rule_count = 0

    for k_itemset_dict_index in range(1, len(final_set_list)-1):
        k_itemset_dict = final_set_list[k_itemset_dict_index]
        k_itemset_list = list(k_itemset_dict.keys())
        k_candidate_rule_temp = 0
        total_rule_count_temp = 0
        lift_temp = 0
        for each_itemset in k_itemset_list:
            itemset = list(each_itemset)
            subsets = subset_generator(itemset, 1)

            rule_list = []
            for item in subsets:
                operating_list = list(itemset)
                rule = []
                for each_item in item:
                    if each_item in operating_list:
                        operating_list.remove(each_item)
                rule.append(tuple(item))
                operating_list.sort()
                rule.append(tuple(operating_list))
                rule_list.append(rule)
                k_candidate_rule_temp = k_candidate_rule_temp + 1
                k_candidate_rule_processed_count = k_candidate_rule_processed_count + 1

                # Confidence calculation
                temp1 = list(each_itemset)
                if len(item) == 1:
                    temp2 = ''.join(item)
                else:
                    temp2 = tuple(item)

                rule_confidence = float((final_set_list[(len(temp1)-1)][each_itemset])/(final_set_list[(len(item)-1)][temp2]))
                rule_confidence_percent = rule_confidence * 100
                if rule_confidence_percent >= min_confidence:
                    total_rule_count_temp = total_rule_count_temp + 1
                    total_rule_count = total_rule_count + 1
                    rules_dict[tuple(rule)] = rule_confidence_percent

                # Lift calculation
                if len(operating_list) == 1:
                    temp3 = ''.join(operating_list)
                else:
                    temp3 = tuple(operating_list)
                rule_lift = float(rule_confidence / (final_set_list[(len(operating_list)-1)][temp3]))* row_count
                if rule_lift > 1:
                    lift_temp = lift_temp + 1
                    lift_rule_count = lift_rule_count + 1
                    rules_lift_dict[tuple(rule)] = rule_lift

        print("Rule counts for k =", k_itemset_dict_index+1)
        print("Number of candidate confidence computations(brute force) =", k_candidate_rule_temp)
        print("Number of rules with brute force method =", total_rule_count_temp)
        print("Number of rules with lift calculation =", lift_temp)
        print(" ")

    print("Total number of candidate confidence computations(brute force) =", k_candidate_rule_processed_count)
    print("Total number of rules with brute force method =", total_rule_count)
    print("Total number of rules with lift calculation =", lift_rule_count)
    print(" ")
    return_list = [rules_dict, rules_lift_dict]
    return return_list

'''
Recursive function to generate rules via confidence pruning

'''
def candidate_itemset_pruning(each_itemset, each_itemset_list, final_set_list, rules_dict, rejected_rule_list, min_confidence, candidate_rule_processed_count, rule_count):
    if len(each_itemset) != 1:
        subsets = subset_generator(list(each_itemset), 2)
        for item in subsets:
            operating_list = list(each_itemset_list)
            rule = []
            for each_item in item:
                if each_item in operating_list:
                    operating_list.remove(each_item)
            rule.append(tuple(item))
            operating_list.sort()
            rule.append(tuple(operating_list))
            if (rule not in list(rules_dict.keys())) and (rule not in rejected_rule_list):
                candidate_rule_processed_count = candidate_rule_processed_count + 1

                # Confidence calculation
                temp1 = list(each_itemset)
                if len(item) == 1:
                    temp2 = ''.join(item)
                else:
                    temp2 = tuple(item)

                rule_confidence = float((final_set_list[(len(temp1) - 1)][each_itemset]) / (final_set_list[(len(item) - 1)][temp2]))
                rule_confidence_percent = rule_confidence * 100
                if rule_confidence_percent < min_confidence:
                    rejected_rule_list.append(rule)
                else:
                    rules_dict[tuple(rule)] = rule_confidence_percent
                    rule_count = rule_count + 1
                    candidate_itemset_pruning(tuple(item), each_itemset_list, final_set_list, rules_dict, rejected_rule_list, min_confidence, candidate_rule_processed_count, rule_count)

        return_list = [candidate_rule_processed_count, rules_dict, rejected_rule_list, rule_count]
        return (return_list)


'''
Function to generate rules via confidence pruning

a) Returns the number of computations made for rule generation
b) Returns the number of rules generated (> minimum confidence)
'''
def rule_gererator_confidence_pruning (final_set_list, min_confidence):
    total_candidate_rule_processed_count = 0
    rules_dict = {}
    rejected_rule_list=[]
    total_rule_count = 0
    for k_itemset_dict_index in range(1, len(final_set_list)-1):
        k_itemset_dict = final_set_list[k_itemset_dict_index]
        k_itemset_list = list(k_itemset_dict.keys())
        k_candidate_rule_processed_count = 0
        k_rule_count = 0
        for each_itemset in k_itemset_list:
            itemset = list(each_itemset)
            return_list = candidate_itemset_pruning(each_itemset, itemset, final_set_list, rules_dict, rejected_rule_list, min_confidence, 0, 0)
            k_candidate_rule_processed_count = k_candidate_rule_processed_count + return_list[0]
            rejected_rule_list = return_list[2]
            k_rule_count = k_rule_count + return_list[3]
            total_rule_count = total_rule_count + return_list[3]

            total_candidate_rule_processed_count = total_candidate_rule_processed_count + return_list[0]
            rules_dict = return_list[1]

        print("Rule counts for k =", k_itemset_dict_index + 1)
        print("Number of candidate confidence computations(confidence based pruning) =", k_candidate_rule_processed_count)
        print("Number of rules with confidence based pruning method =", k_rule_count)
        print(" ")

    print("Total number of candidate confidence computations(confidence based pruning) =", total_candidate_rule_processed_count)
    print("Total number of rules with confidence based pruning method =", total_rule_count)
    return rules_dict