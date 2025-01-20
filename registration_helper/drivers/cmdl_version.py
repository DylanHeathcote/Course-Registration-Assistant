#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import tools.data_frame_tools as dft
import tools.course_tools as ct
import tools.cmdl_parser_tools as cp

def pretty_print(comp_scheds):

     print("\nCOMPATIBLE SCHEDULE SUMMARY:")
     print('\n', ("-" * 80), '\n')
     for count, comp_sched in enumerate(comp_scheds):
          
          priority = ct.fetch_priority_stat(comp_sched)
          
          print(" Schedule: %s, Priortiy = %s" % ((count+1), priority))
          
          for course in comp_sched:

               print("\n  Course: %s, CRN: %s" % (course.name, course.CRN))

               for day in course.weekly_schedule:

                    print("   %s %s " % (day.name.ljust(10), ':'.rjust(5)), end = ' ')

                    if day.start_time != int(-1):
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

     ComLineParse = cp.CommandLineParser()
     
     fileParse = dft.FileParser()

     flist = ComLineParse.parse_argv(argv)

     data_frames = fileParse.parse_file_list(flist)

     if not data_frames:

          print("no course information (files) inputed")

          return True

     data_frame = dft.combine_data_frame_list(data_frames)
        
     courses = dft.cleanup_data_frame(data_frame)
     
     comp_scheds = ct.create_courses(courses)
     
     pretty_print(comp_scheds)
               
if __name__ == "__main__":          
     main(sys.argv[1:])


#
# end of file
