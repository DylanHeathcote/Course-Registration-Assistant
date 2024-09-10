#!/usr/bin/env python

import argparse
import os
import sys

class CommandLineParser:

    def __init__(self):
        """
        method __init__

        arguments: None

        return: None

        descirption:
        this is a constructor method for
        the command line parser
        """

        # create class name
        #
        CommandLineParser.__CLASS_NAME__ = self.__class__.__name__

        # instantiate an argument parser object
        #
        self.arg_parser = argparse.ArgumentParser()

        # add neccessary arguments to the
        # argument parser
        #
        self.arg_parser.add_argument("files", type=str, nargs='*')

    #
    # end of method
    
    def parse_argv(self, args):
        """
        method: command_line_parse

        arguments:
         args: the command line arguments

        return:
         boolean value indicating status

        description:
         this method parses the command line
         and send the arguments to main
        """
        
        # parse arguments
        #
        arguments = self.arg_parser.parse_args(args)
        
        # if no files are inserted
        # throw an error and exit 
        #
        if arguments is None:
            
            # Throw print error
            #
            print("Error: no arguments/files inputted")
            
            # exit ungracefully
            #
            sys.exit(os.EX_SOFTWARE)

        # fetch file arguments
        #
        file_paths = arguments.files
        
        # expand each file path in the directory
        # and ensure they exist
        #
        self.expand_file_paths(file_paths)

        # exit gracefully
        #
        return file_paths
    #
    # end of method
            
    def expand_file_paths(self, file_paths):

        """
        method: expand_file_paths

        arguments:
         file_paths: a list of file paths

        return:
         boolean value indicating status

        description:
         this method expands file paths
         and ensures the paths exist
        """
        
        for path_index in range(len(file_paths)):

            # expand the file path
            #
            file_paths[path_index] = \
                self.expand_file_path(file_paths[path_index])

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
        # end of method
     
    def expand_file_path(self, file_path):
        """
        method: expand_file_path

        arguments:
         file_path: a file path
     
        return:
         a file path

        description:
         this method expands the file path
        """
        # expand and return the file path
        #

        # exit gracefully
        #
        return os.path.abspath(
            os.path.expanduser(
                os.path.expandvars(
                    file_path)))        
    #
    # end of method
#
# end of class


#
# end of file
