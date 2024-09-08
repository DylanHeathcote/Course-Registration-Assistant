Title of Tool: Registration_Helper

Requirements:
	This tool requires pandas. In order for it to work you must create a virtual environment by typing into the terminal the following "virtualenv -p python3 venv_name". Next Activate the environment by typing "scource bin/activate". Finally, use pip to install all requirements in requirements.txt by typing "pip install -r requirements.txt". Here is a video describing how to create a python virtual environment: "https://www.youtube.com/watch?v=hC5rfoIY8nU" 
	
Main functionality:
	This registration tool takes the command-line XLSX and CSV files as arguments and outputs all compatible weekly academic schedules. Please make a copy of the CSV and XLSX files inside the example directory and add as many courses as you like.

General Structure of supported file types:
	All supported files have the same structure. The information is formatted in the following order:

CRN, Course Name, Monday start time, Monday end time, ... Friday start time, Friday end time, Priority.

        CRN: The CRN is a unique number identifier for each class. Please ensure that CRN numbers are unique, as duplicate CRNS are ignored.
     
	Course Name: The course name may or may not be a unique identifier. However, please note that two courses with two different CRNs but the same name are incompatible.

     	Start Time/End Time: the start and end time for the course on a specific day of the week. As of now, it only supports the 24-hour clock.

     	Priority: The user sets the Priority. Each comparable schedule outputted will have a priority number above the course list. This can help find the optimal schedule if some courses are needed more than others.

CSV specific:
	If a course is not scheduled during a specific day of the week, input 'NaN' for nonapplicable

XLSX specific:	    
        If a course is not scheduled during a specific day of the week, input 'N/A' for nonapplicable

Future Updates:
- Documentation update
- optional GUI update

Note this file is avaliable in the registration_helper directory as well
