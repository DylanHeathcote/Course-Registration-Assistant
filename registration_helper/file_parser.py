#!/usr/bin/env python

import pandas as pd
import copy
import sys
import os

class FileParser:

    def __init__(self):

        self.file_types = copy.deepcopy(FTYPE_OBJECTS)
        
        FileParser.__CLASS_NAME__ = self.__class__.__name__

        self.CRN_list = list()

    def remove_dups(self, data):

        file_CRN_list = list(x for x in data['CRN'].keys())
        
        for CRN_key in file_CRN_list:

            if data["CRN"][CRN_key] in self.CRN_list:
                
                for header_key in data.keys():
                    
                    data[header_key].pop(CRN_key)
            else:

                self.CRN_list.append(data["CRN"][CRN_key])
                
        return data
    
    def parse_file_list(self, flist):

        file_data_list = list()
        
        for file in flist:

            file_data_list.append(self.parse_file(file))

        return file_data_list
        
    def parse_file(self, file):

        # get file extension
        #
        ext = file.split(".")[-1]

        # call corresponding parsing method
        #

        if ext in self.file_types.keys():
    
            data = self.remove_dups(self.file_types[ext].parse(file))
            
            return data
        
        else:

            print("file type not supported -> '%s'" % ext)
            sys.exit(os.EX_SOFTWARE)
            
class CsvParser:

    def __init__(self):

        CsvParser.__CLASS_NAME__ = self.__class__.__name__

    def parse(self, csv_file):

        data = pd.read_csv(csv_file)

        df = pd.DataFrame(data)
        
        data_dict = df.to_dict()

        for header_key in data_dict.keys():

            for index in data_dict[header_key].keys():
 
                if pd.isna(data_dict[header_key][index]):

                    data_dict[header_key][index] = None
                    
                if isinstance(data_dict[header_key][index], float):

                    data_dict[header_key][index] = int(data_dict[header_key][index])

        return data_dict
        
class XlsxParser:

    def __init__(self):

        XlsxParser.__CLASS_NAME__ = self.__class__.__name__

    def parse(self, xlsx_file):

        xl = pd.ExcelFile(xlsx_file)
        
        data = xl.parse(xl.sheet_names[0])

        df = pd.DataFrame(data)
        
        data_dict = df.to_dict()

        for header_key in data_dict.keys():

            for index in data_dict[header_key].keys():

                if pd.isna(data_dict[header_key][index]):

                    data_dict[header_key][index] = None
                    
                if isinstance(data_dict[header_key][index], float):

                    data_dict[header_key][index] = int(data_dict[header_key][index])

        return data_dict
    
    
    
FTYPE_OBJECTS = { 'csv': CsvParser(), 'xlsx' : XlsxParser() }
