"""
Created on Wed Dec 8 15:13:16 2018

@author: dhrumil vora
"""
import itertools
import pandas as pd
import numpy as np
from decimal import Decimal

from openpyxl import load_workbook
def countOccurenece(transactions, itemsToCount):
    count = 0;
    for transaction in transactions:
        didFindAll = True;
        for item in itemsToCount:
            if item not in transaction:
                didFindAll = False;
                break;

        if didFindAll:
            count = count + 1;
    return count;

def getFrequentItemSet(transactions, list_of_itemSet, min_supported_count):
    list = []

    for item in list_of_itemSet:
        itemCount = countOccurenece(transactions, item);
        if itemCount > 0:
            print(str(item) + ':' + str(itemCount));

        if itemCount >= min_supported_count:
            supportList.append(item)
            supportListCount.append(itemCount)
            list.append(item);

    return list;
def compare_list(list,item):
    for element in list:
        if set(element) - set(item) == set([]):
            return True;
    return False;

def print_freq_itemset(list,list_count):
    if list_count >= min_supported_count:
        print(str(list)+':'+str(list_count));

def combineSet(list_of_items,pass_number):
    combined_list =[];
    for combination in itertools.combinations(list_of_items, 2):
        combined_temp = [] + combination[0];
        for element in combination[1]:
            if element not in combined_temp:
                combined_temp.append(element);
        if compare_list(combined_list,combined_temp) == False and len(combined_temp) == pass_number:
            combined_list.append(combined_temp);
    return combined_list;


def association_rules(supportList,supportListCount):
    for element in supportList:
        element_support = supportListCount[supportList.index(element)];
        for item in supportList:
            if ((len(item) == len(element) - 1) and
                    set(item).issubset(element)):
                item_support = supportListCount[supportList.index(item)];
                rule_confidence = element_support / item_support;
                if rule_confidence >= min_confidence:
                    if element > item:
                        print()
                        print(', '.join([str(x) for x in item] )+' -> '+ ", ".join(str(e) for e in set(element)-set(item))+'\tSupport:'+str(round(Decimal(element_support/len(transactions)*100),2))+' %\tconfidence:'+str(round(Decimal(rule_confidence*100),2))+' %');

# Main Starts From Here
database = 1;
print('Select\n1 for Amazon \n2 for kmart \n3 for Ikea \n4 for Shoprite \n5 for Riteaid')
database = input();
min_support = float(input('Enter minimum support(in decimal)'));
min_confidence = float(input('Enter minimum confidence(in decimal)'));

workbook = load_workbook('./dataset'+str(database)+'.xlsx');
sheet = workbook.get_sheet_by_name('Sheet1')
database_dataframe = pd.DataFrame(sheet.values);
transactions = [];
list_of_itemSet = [];
for i in range(0,len(database_dataframe)):
    current_transaction_itemsSet = database_dataframe.values[i][1].split(',');
    transactions.append(current_transaction_itemsSet)
    for element in current_transaction_itemsSet:
        if element not in list_of_itemSet:
            list_of_itemSet.append(element);
# print(transactions);
size_of_list = len(list_of_itemSet);
min_supported_count = min_support * len(transactions);

itemSet = [];
for item in list_of_itemSet:
    itemSet.append([item]);

supportList = [];
supportListCount = [];
print('------------------candidate itemset:1------------------');
frequentItemSet = getFrequentItemSet(transactions, itemSet, min_supported_count);

print('------------------frequent itemset:1------------------');
for element in frequentItemSet:
    print_freq_itemset(element,countOccurenece(transactions,element));
print('');

index = 2;
while True:
    if len(frequentItemSet) < 2:
        break;
    else:
        candidateSet = combineSet(frequentItemSet, index);
        print('------------------candidate itemset:'+str(index)+'------------------');
        # print(candidateSet);

        frequentItemSet = getFrequentItemSet(transactions, candidateSet, min_supported_count);
        print('------------------frequent itemset:' + str(index)+'------------------');
        for element in frequentItemSet:
            print_freq_itemset(element,countOccurenece(transactions,element));
        print('');
    index = index + 1;
print('------------------Association rules------------------');
association_rules(supportList,supportListCount);
