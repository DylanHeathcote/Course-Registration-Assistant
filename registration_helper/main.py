#!/usr/bin/env python

import os
import sys
from operator import itemgetter

import course_tools as ct
import cmdl_parser_tools as cp
import file_parser as fp
import scoring_tools as st

def pretty_print(comp_scheds):

     print("\nCOMPATIBLE SCHEDULE SUMMARY:")
     print('\n', ("-" * 80), '\n')
     for count, comp_sched in enumerate(comp_scheds):
          
          priority = st.fetch_priority_stat(comp_sched)
          
          print(" Schedule: %s, Priortiy = %s" % ((count+1), priority))
          
          for course in comp_sched:

               print("\n  Course: %s, CRN: %s" % (course.name, course.CRN))

               for day in course.schedule:

                    print("   %s %s " % (day.name.ljust(10), ':'.rjust(5)), end = ' ')

                    if day.start_time:
                         print("Start Time: %s hours, Stop Time: %s hours".rjust(45) %
                               (day.start_time, day.end_time))
                    else:
                         print("N/A".rjust(7))

          if count != len(comp_scheds)-1:
               print('\n', ('*' * 80), '\n')
               
     print('\n', '-' * 80)
          

def main(argv):
     """
     function: main

     arguments: none

     return: boolean value idicating status

     description:
        This is where the method where everything is processed
    """

     flist = cp.cmld_parse(argv)

     fileParse = fp.FileParser()

     data = fileParse.parse_file_list(flist)

     course_list = list()
     
     for file_data in data:

          for index in list(file_data.values())[0]:

               course_list.append(ct.Course(file_data, index))
               
     compatible_schedules = ct.fetch_comp_combs(course_list)
     
     pretty_print(compatible_schedules)
               
if __name__ == "__main__":
    main(sys.argv[0:])


#
# end of file
