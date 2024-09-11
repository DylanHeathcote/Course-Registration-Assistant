#!/usr/bin/env python

from day_tools import Day


def fetch_comp_combs(course_list):
"""
method: fetch_comp_combs

arguments:
 course_list: list of courses

return:
 a list of all compatible course schedules

description:
 this method fetches all the compatible course
 schedules
"""
    # fetch the powerset of the course list
    #
    pset = [x for x in powerset(course_list)]

    # for each list in the powerset check
    # compatibility
    #
    for index, set in enumerate(pset):

        # fi the list is not compatible
        #
        if not is_compatible_list(set):

            # pop the index the list resides in 
            #
            pset.pop(index)

    # exit gracefully
    #
    return pset
#
# end of function

def powerset(courses):
    """
    method: powerset

    arguments:
     courses: a list of course objects

    return:
     the generator object containing the
     powerset of courses

    description:
     this method returns the powerset of a courses list
    """

    # if the length of the courses array
    # is less than or equal to one append
    # courses to generator object
    #
    if len(courses) <= 1:
        # append the course to the generator
        #
        yield courses

    # if the length of courses is not less than
    # or equal to one recursively call powerset
    # and append results to a generator object
    #
    else:

        # for each course in a set returned from a powerset
        # that is one smaller in length append courses to 
        # generator
        #
        for course in powerset(courses[1:]):

            # append course retuned in the for 
            # loop to the first course in the current
            # courses list and append to generator
            #
            yield [courses[0]]+course

            # append the course returned by powerset
            # by itself to the generator
            #
            yield course

#
# end of method

def is_compatible_list(course_list):
    """
    method: is_compatible_list

    arguments:
     course_list: list of courses

    return:
     a boolean value indicating if a course
     list is compatible
    """

    # if there is noting in the course list return 
    # false to remove
    # to do: remove this (not needed)
    #
    if not course_list:
        
        # return false to remove empty list
        #
        return False
        
    # create a copy of the course combination indices
    # to do: remove this and place in calling function
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

    return:
     none
     
    description:
     this class holds a courses scheudle for the
     specific day. the day being one of the days
     of the week
    """

    def __init__(self, data_dict, index):

        """
        method: __init__

        argurments:
         data_dict: a dictionary containing course data
         index: the index in the data dictionary to assign
          the courses fields

        return:
         none

        description:
         this method consturcts the Course class object
        """

        # set the course name
        #
        self.name = data_dict['class_name'][index]

        # set the course CRN
        #
        self.CRN = data_dict['CRN'][index]

        # set the course priority
        #    
        self.priority = data_dict['Priority'][index]

        # set the course's monday scheudle
        #
        self.monday = Day('Monday',
                          data_dict['Monday_start'][index],
                          data_dict['Monday_end'][index])

        # set the course's tuesday scheudle
        #
        self.tuesday = Day('Tuesday',
                           data_dict["Tuesday_start"][index],
                           data_dict["Tuesday_end"][index])

        # set the course's wednesday schedule
        #
        self.wednesday = Day('Wednesday',
                             data_dict["Wednesday_start"][index],
                             data_dict["Wednesday_end"][index])

        # set the course's thursday schedule
        #
        self.thursday = Day('Thursday',
                            data_dict["Thursday_start"][index],
                            data_dict["Thursday_end"][index])

        # set the course's friday schedule
        #
        self.friday = Day('Friday',
                          data_dict["Friday_start"][index],
                          data_dict["Friday_end"][index])

        # make a list of the course's schedules
        #
        self.schedule = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday]
    #
    # end of method

    def set_CRN(self, CRN):
           """
        method: constructor

        argurments:
         data_dict: a dictionary containing course data
         index: the index in the data dictionary to assign
          the courses fields

        return:
         boolean value indicating status

        description:
         this method consturcts the Course class object
        """

        # set the CRN
        #
        self.CRN = CRN

        # exit gracefully
        #
        return True
    #
    # end of method

    def set_day(self, day_to_set, start, end):
        """
        method: set day

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
    #
    # end of method

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

            # return false, to courses of the same class name are not 
            # compatible
            #
            return False

        # for every day in the current instantiated course objects schedule
        # and every day in the other courses schedule compare its elements
        # to determine compatibility
        #
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
    # end of method

#
# end of class


#
# end of file
