#!/usr/bin/env python

from itertools import chain, combinations

def fetch_comp_combs(course_list):
    """
    function: fetch_comp_combs

    arguments:
     course_list: a list of course objects

    return:
     a list of lists of compatible courses

    description:
     this function is a fetches all of the
     compatible combinations of courses
    """

    # exit gracefully
    #  return the compatible schedules list
    #
    return [subset for subset in powerset(course_list) if is_compatible_list(subset)]
#
# end of fucntion
    
def powerset(course_list):
    """
    function: powerset

    arguments:
     course_list: a list of courses

    return:
     all possible combinations of courses

    description:
     returns the powerset of the course_list, however,
     not all sets in the powerset are compatible schedules
    """

    # wrap the course list around a list
    #
    s = list(course_list)

    # exit gracefully
    #  return the powerset of course_list
    #
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
#
# end of funciton

def is_compatible_list(course_list):
    """
    function: is_compatible_list

    args:
     course_list: a subset of the course list powerset

    return:
     boolean value indicating if a subset is compatible

    description:
     this function determines whether a course list is
     indeed compatible
    """

    # if the course list is empty then it is
    # the empty set and uninteresting
    #
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


def check_valid_time(start_time, end_time):
    """
    function: check_valid_time

    arguments:
     start_time: a specific course schedules day start time
     end_time: a specific course schedules day end tiem

    reutrn:
     boolean value indicating if the start/stop times
     are valid

    description:
     this function is used to determine if times entered
     by the user are valid
    """

    # if the start time and end time are not specified
    # it means that the course has no class on this day
    # and is thus valid
    #
    if start_time is None and end_time is None:
        return True

    # if the start time is present but not the end time
    # the input is invalid
    #
    if end_time is None:
        return False

    # if the end time is present but not the start time
    # the input is invalid
    #
    if start_time is None:
        return False
    
    # if the start time or end time is less
    # then 6 am in the morning the courses day schedule
    # is not valid
    #
    if start_time < int(600) or end_time < int(600):
        return False

    # if the start time or end time is greator then
    # 8 pm in the courses day schedule is not valid
    #
    if start_time > int(2000) or end_time > int(2000):
        return False

    # if the start time is after the end time the
    # courses day scehdule is not valid
    #
    if start_time > end_time:
        return False

    # exit gracefully
    #  the courses specific day schedule is valid
    #
    return True
#
# end of function

def fetch_priority_stat(course_sched):
     """
     function: fetch_priority_stat

     args:
      course_sched

     return:
      priority_sum: a compatible course schedules
      priority

     description:
      this function sums the priority of the courses
      gvien by the user
     """
     
     # create a varaibel to store the
     # priortiy
     #
     priority_sum = int(0)

     # iterate over each course in
     # the course shecdule
     #
     for course in course_sched:

          # sum the priority of each course
          #
          priority_sum += course.priority

     # exit gracefully
     #  return the priority_sum
     #
     return priority_sum
#
# end of funciton

def create_courses(course_df):

    course_list = list()

    for course_num in range(len(course_df)):
    
        course = course_df.loc[course_num]
        
        course_list.append(Course(course))
        
    return fetch_comp_combs(course_list)
        
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

    def __init__(self, course_df):

        """
        method: constructor

        argurments:
         course_df: a data frame containing a courses
          properties
              
        return:
         boolean value indicating status

        description:
         this method instantiates the object
        """

        # set the course name
        #
        self.name = course_df['class_name']

        # set the course CRN
        #
        self.CRN = course_df['CRN']

        # set the course priority
        #
        self.priority = course_df['Priority']

        # set course schedule
        #
        # set mondays
        #
        self.monday = Day('Monday',
                          course_df['Monday_start'],
                          course_df['Monday_end'])

        # set tuesday
        #
        self.tuesday = Day('Tuesday',
                           course_df["Tuesday_start"],
                           course_df["Tuesday_end"])

        # set wednesday
        #
        self.wednesday = Day('Wednesday',
                             course_df["Wednesday_start"],
                             course_df["Wednesday_end"])

        # set thursday
        #
        self.thursday = Day('Thursday',
                            course_df["Thursday_start"],
                            course_df["Thursday_end"])

        # set firday
        #
        self.friday = Day('Friday',
                          course_df["Friday_start"],
                          course_df["Friday_end"])

        # conbine the courses daily schedules to form a weekly
        # schedule for convienence
        #
        self.weekly_schedule = \
            [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday]
    
    #
    # end of method
    
    def set_CRN(self, CRN):
        """
        method: set_CRN

        args:
         CRN: the course CRN

        return: None

        description:
         this method sets the CRN field
        """

        # set the CRN
        #
        self.CRN = CRN
    #
    # end of method
    
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
            return False

        # iterate over each courses daily schedule
        #
        for self_day, othr_day in zip(self.weekly_schedule, othr_course.weekly_schedule):
            
            # if one of the days start time is none then
            # skip that day as there are no conflicts
            #
            if self_day.start_time == None \
               or othr_day.start_time is None:
                continue

            # if the start time of the instansiated course's
            # lies between the othr_course's start 
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
         name: the day name
         start_time: the course's day start time
         stop_time: the course;s day end time

        return:
         none

        description
         this is the constructor for this class
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

#
# end of file
