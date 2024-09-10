#!/usr/bin/env python

def fetch_priority_stat(course_sched):

     priority_sum = int(0)
     
     for course in course_sched:

          priority_sum += course.priority

     return priority_sum
          
