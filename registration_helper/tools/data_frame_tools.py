#!/usr/bin/env python

import pandas as pd
import pandera as pa
import copy
import sys
import os
import tools.course_tools as ct
import toml

tool_dir = os.path.dirname(os.path.abspath(__file__))

toml_path = os.path.join(tool_dir, "registration_misc_tools.toml")

with open(toml_path, "r") as toml_file:
    str_hlpr = toml.load(toml_file)
    
class FileParser:
    
    def __init__(self):
        """
        method: __init__

        arguments: None

        return: None

        description:
         this method constructs the clas
        """

        # copy the file types dictionary 
        #
        self.file_types = copy.deepcopy(FTYPE_OBJECTS)

        # set the class name
        #
        FileParser.__CLASS_NAME__ = self.__class__.__name__
        
    #
    # end of method
    
    def parse_file_list(self, flist):
        """
        method: parse file list

        arguments:
         flist: a file list

        return:
         file_data_list: flists data

        description:
         this method parses a file list
        """

        # create a list to hold all data
        #
        file_data_list = list()

        # iterate over each file in the list
        #
        for file in flist:

            # parse the file and append its info
            # to the file data list
            #
            file_data_list.append(self.parse_file(file))

        # exit gracefully
        #  return flists data
        #
        return file_data_list
    #
    # end of method
    
    def parse_file(self, ffile):
        """
        method: parse_file

        arguements:
         ffile: the file to parse

        return: the files infromation

        description:
         this method parses a file
        """
        
        # get file extension
        #
        ext = ffile.split(".")[-1]

        # ensure the extenstion is supported
        #
        if ext not in self.file_types.keys():

            # if its not supported through an error
            # and exit
            #
            print("file type not supported -> '%s'" % ext)
            sys.exit(os.EX_SOFTWARE)        
            
        # exit gracefully
        #  prase and return the files contents
        #
        return self.file_types[ext].parse(ffile)
    #
    # end of method
    
class CsvParser:

    def __init__(self):
        
        CsvParser.__CLASS_NAME__ = self.__class__.__name__

    def parse(self, csv_file):

        data = pd.read_csv(csv_file)

        data_frame = pd.DataFrame(data)
        
        return data_frame
        
class XlsxParser:

    def __init__(self):
        """
        method: __init__

        arguements: None

        return: None

        description:
         this method constructs the class
        """

        # set the class name
        #
        XlsxParser.__CLASS_NAME__ = self.__class__.__name__
    #
    # end of method
    
    def parse(self, xlsx_file):

        """
        method: parse

        arguements: xlsx_file

        return:
         data_dict: a dictionary containing
          the files information

        description:
         this method reads an xlsx files data
        """

        # create a pandas ExceleFIle
        # tool for parsing
        #
        xl = pd.ExcelFile(xlsx_file)

        # parse the files info
        #
        data = xl.parse(xl.sheet_names[0])

        # create a data frame
        # 
        data_frame = pd.DataFrame(data)

        # exit gracefully
        # return the data frame
        #
        return data_frame
    #
    # end of method

#
# end of class

# define a dictionary to hold the compatible
# file types
#
FTYPE_OBJECTS = { 'csv': CsvParser(), 'xlsx' : XlsxParser() }

# Define a function to validate the allowed types
def validate_time(value):
    return isinstance(value, (int, float, str)) or pd.isna(value)

# Define the schema for the pandas data frame
#
Schema = pa.DataFrameSchema({
    str_hlpr['course_props']['course_props'][0]: pa.Column(int, nullable=False, coerce = True),
    str_hlpr['course_props']['course_props'][1]: pa.Column(str, nullable=False),
    str_hlpr['course_props']['course_props'][2]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][3]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][4]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][5]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][6]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][7]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][8]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][9]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][10]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][11]: pa.Column(str, nullable=True, coerce=True),
    str_hlpr['course_props']['course_props'][12]: pa.Column(int, nullable=True, coerce=True),
})

def remove_dupicate_courses(data_frame):

    """
    function: remove_dupicate_courses
    
    arguments:
     data_frame: the info extracted from a file

    return:
     data_frame: a data frame without repeat CRN's

    description:
     this method removes all dulpicate courses which
     is determined by the CRN
    """

    # create a list of know CRN's
    #
    known_CRNs = list()

    # iterate over each CRN 
    #
    for course in range(len(data_frame)):
                        
        # if the CRN key is already in the CRN list
        # that means this CRN is a duplicate
        #
        if data_frame["CRN"][course] in known_CRNs:
            
            # iterate over each property entered
            # by the user 
            #
            for property_d in data_frame.columns:
                
                # pop the duplicate CRN from the
                # property
                #
                data_frame[property_d].pop(CRN_key)
                
        # else if the CRN key is not already in the CRN list
        # append the CRN key
        #
        else:

            # append CRN to CRN list
            # 
            known_CRNs.append(data_frame["CRN"][course])
            
    # exit gracefully
    #  return data with unique courses
    #
    return data_frame
#
# end of function

def refine_data_frame(data_frame):
    
    # Replace all NaN values in the DataFrame with -1
    #
    data_frame = data_frame.fillna(int(-1))

    # Process each column individually
    #
    for property_d in data_frame.columns:

        # Handle non-numeric columns (e.g., object or string types)
        #
        if pd.api.types.is_object_dtype(data_frame[property_d]):
            data_frame[property_d] = \
                data_frame[property_d].apply(lambda x: convert_time_to_int(x))
            
        if property_d != "class_name":
            data_frame[property_d] = \
                data_frame[property_d].astype(float).astype(int)
            
    return data_frame


def convert_time_to_int(value):
    """
    Convert time in "HH:MM" format to an integer (e.g., "13:45" -> 1345).
    If the value is not in time format, return it unchanged.
    """
    if isinstance(value, str) and ":" in value:
        try:
            hour, minute = map(int, value.split(":"))
            return hour * 100 + minute
        except ValueError:
            return value  # Return unchanged if invalid time format
    return value


def cleanup_data_frame(data_frame):
    
    data_frame = Schema.validate(data_frame)

    data_frame = remove_dupicate_courses(data_frame)

    data_frame = refine_data_frame(data_frame)

    return data_frame

def combine_data_frame_list(data_frames):

    return pd.concat(data_frames, axis = 0)

def create_data_frame_from_dict(data_dict):

    return pd.DataFrame(data_dict)
