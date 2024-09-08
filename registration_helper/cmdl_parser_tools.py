#!/usr/bin/env python

import argparse
import os
import sys

def cmld_parse(args):

    # instanisate argument parse object
    #
    ar_parse = argparse.ArgumentParser()

    # add file argument type
    #
    ar_parse.add_argument("files", type=str, nargs='*')

    # parse arguments
    #
    arguments = ar_parse.parse_args(args)

    # exclude main.py
    #
    file_paths = arguments.files[1:]

    # if no files are inserted
    # throw an error and exit 
    #
    if file_paths is None:

        # Throw print error
        #
        print("Error: no files inputted")

        # exit ungracefully
        #
        sys.exit(os.EX_SOFTWARE)

    # expand each file path in the directory
    # and ensure they exist
    #
    expand_and_ensure_files_exist(file_paths)

    # exit gracefully
    #
    return file_paths
#
# end of function
            
def expand_and_ensure_files_exist(file_paths):

    for path_index in range(len(file_paths)):

        # expand the file path
        #
        file_paths[path_index] = os.path.abspath(
            os.path.expanduser(
                os.path.expandvars(
                    file_paths[path_index])))

        # ensure file path exists
        #
        if os.path.exists(file_paths[path_index]) is False:

            # throw an error
            #
            print("Error: file does not exist (%s)" %
                  file_paths[path_index])

            # exit ungracefully
            #
            sys.exit(os.EX_SOFTWARE)

    # exit gracefully
    #
    return True
#
# end of function
