#!/usr/bin/env python

class Day:
    """
    Class: Day

    arguments:
     none

    description:
     this class holds a courses scheudle for the
     specific day. the day being one of the days
     of the week
    """

    def __init__(self, name, start_time, stop_time):

        """
        method: constructor

        argurments:
         scheudle: a time scheudle for
         a specific day

        return:
         none

        description
         none
        """

        # set the schedule
        #
        self.name = name
        self.start_time = start_time
        self.end_time = stop_time

    #
    # end of method

    def set_schedule(self, start_time, end_time):

        """
        method: set_schedule

        argurments:
         scheudle: a time scheudle for
         a specific day

        return:
         boolean value indicating status

        description:
         this method sets the schedule's data
        """

        # set the schedule
        # 
        self.start_time = start_time
        self.end_time = end_time

        # exit gracefully
        #
        return True

    #
    # end of method
#
# end of class
