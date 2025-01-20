Title of Tool: Registration_Helper

Requirements:
	This tool requires pandas, toml, and pandera. In order for it to work you must create a virtual environment by typing into the terminal the following "virtualenv -p python3 venv_name". Next Activate the environment by typing "scource bin/activate". Finally, use pip to install all requirements in requirements.txt by typing "pip install -r requirements.txt". Here is a video describing how to create a python virtual environment: "https://www.youtube.com/watch?v=hC5rfoIY8nU"
	for setting up the environment please run either setup_bash.bat for windows or setup_env.sh for linux (bash). then to run the tools simply find the drivers directory and type either "python cmdl_version.py [files]" ( where [files] is a single file or list of files to calculate compatible schedules for) or "python gui_version.py" for the gui.

Pandera:
- Pandera (https://github.com/pandera-dev/pandera)
  Licensed under the MIT License.

Main functionality:
	This registration tool has a gui and command-line version that take XLSX and CSV files as arguments and outputs all compatible weekly academic schedules. Please make a copy of the CSV and XLSX files inside the example directory and add as many courses as you like. Additionally, input can be given directly to the GUI as well

General Structure of supported file types:
	All supported files have the same structure. The information is formatted in the following order:

CRN, Course Name, Monday start time, Monday end time, ... Friday start time, Friday end time, Priority.

        CRN: The CRN is a unique number identifier for each class. Please ensure that CRN numbers are unique, as duplicate CRNS are ignored.
     
	Course Name: The course name may or may not be a unique identifier. However, please note that two courses with two different CRNs but the same name are incompatible.

     	Start Time/End Time: the start and end time for the course on a specific day of the week. As of now, it only supports the 24-hour clock. The start/end times can be entered in two different formats an integer (i.e. 1100 for 11 am) or as two integers seperated by a semicolon (i.e. 11:00 for 11 am).

     	Priority: The user sets the Priority. Each comparable schedule outputted will have a priority number above the course list. This can help find the optimal schedule if some courses are needed more than others.

CSV specific:
	If a course is not scheduled during a specific day of the week, input 'NaN' for nonapplicable

XLSX specific:	    
        If a course is not scheduled during a specific day of the week, input 'N/A' for nonapplicable

Future Updates:
- More Bug Prevention Update
- Documentation update
- GUI help window
- Exectuable GUI file


