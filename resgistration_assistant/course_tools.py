#!/usr/bin/env python

from day_tools import Day

def fetch_comp_combs(course_list):

    pset = [x for x in powerset(course_list)]

    for index, set in enumerate(pset):

        if not is_compatible_list(set):

            pset.pop(index)

    return pset

def powerset(courses):
    """
    Returns a generator of all the subsets of courses
    """
    if len(courses) <= 1:
        yield courses
        yield []
        
    else:
        for course in powerset(courses[1:]):
            yield [courses[0]]+course
            yield course

def is_compatible_list(course_list):

    if not course_list:

        return False
    # create a copy of the course combination indices
    #
    course_list_copy = list(course_list)
    
    # ensure scheudles are compatible in combination
    #
    while course_list_copy:

        # pop an index from the course combination inex list
        #
        course_to_compare = course_list_copy.pop()

        # loop over all courses left in course_comb
        #
        for course_index in course_list_copy:

            # if the course we are comparing is not compatible
            # with one of the courses in the course list
            # return false
            #
            if not course_to_compare \
               .is_compatible(course_index):
                
                # exit ungracefully
                #
                return False

    # exit gracefully
    #
    return True
#
# end of function

class Course:
    """
    Class: Course

    arguments:
     none

    description:
     this class holds a courses scheudle for the
     specific day. the day being one of the days
     of the week
    """

    def __init__(self, data_dict, index):

        """
        method: constructor

        argurments:
         none

        return:
         none

        description:
         none
        """

        # set the schedule
        #
        self.name = data_dict['class_name'][index]
        self.CRN = data_dict['CRN'][index]
        self.priority = data_dict['Priority'][index]
        self.monday = Day('Monday',
                          data_dict['Monday_start'][index],
                          data_dict['Monday_end'][index])
        self.tuesday = Day('Tuesday',
                           data_dict["Tuesday_start"][index],
                           data_dict["Tuesday_end"][index])
        self.wednesday = Day('Wednesday',
                             data_dict["Wednesday_start"][index],
                             data_dict["Wednesday_end"][index])
        self.thursday = Day('Thursday',
                            data_dict["Thursday_start"][index],
                            data_dict["Thursday_end"][index])
        self.friday = Day('Friday',
                          data_dict["Friday_start"][index],
                          data_dict["Friday_end"][index])
        self.schedule = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday]
    #
    # end of method

    def set_CRN(self, CRN):

        self.CRN = CRN
        
    def set_day(self, day_to_set, start, end):
        """
        method: constructor

        argurments:
         day_to_set: string representing the day to set
         start: start of course
         end: end of course

        return:
         boolean value indicating
         status

        description:
         this method sets the day_to_set with
         the data
        """

        # set the day's data
        #
        getattr(self, day_to_set).set_schedule(start, end)

        # exit gracefully
        #
        return True
    
    def is_compatible(self, othr_course):
        """
        method: is_compatible

        argurments:
         othr_course: the course to check if compatible

        return:
         boolean value indicating compatability

        description:
         this method tests if othr_course is
         compatible with the current instansiated
         course object 
        """

        # if the course names are the same they are not compatible
        #
        if self.name == othr_course.name:

            return False
        
        for self_day, othr_day in zip(self.schedule, othr_course.schedule):
            
            # if one of the days start time is none then
            # skip that day
            #
            if self_day.start_time == None \
               or othr_day.start_time is None:
                continue

            # if the start time of the instansiated course's
            # start time lies between the othr_course's start
            # and end time they are not compatible
            #
            if self_day.start_time > othr_day.start_time \
               and self_day.start_time <othr_day.end_time:
                return False

            # if the start time of the othr_course's
            # start time lies between the current instantiated
            # courses start and end time they are not compatible
            #
            if othr_day.start_time > self_day.start_time \
               and othr_day.start_time < self_day.end_time:
                return False

            # if the start times are the same then
            # the courses are not compatible
            #
            if self_day.start_time == othr_day.start_time:
                return False
            
        # exit gracefully
        #  the schedules are compatible
        #
        return True
#
# end of class
