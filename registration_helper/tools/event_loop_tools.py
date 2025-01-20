#!/usr/bin/env python

from PyQt6.QtWidgets import QScrollArea, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QFileDialog, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QHBoxLayout
import os
from itertools import product
import toml
from PyQt6.QtCore import Qt
import tools.course_tools as ct
import tools.data_frame_tools as dft

# Get the directory of the current script
tool_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the TOML file
toml_path = os.path.join(tool_dir, "registration_misc_tools.toml")

with open(toml_path, "r") as toml_file:
    str_hlpr = toml.load(toml_file)

time_to_row = \
    {
        f"{hour + minute:04d}": table_idx
        for table_idx, (hour, minute) in enumerate(
                product(range(600, 2001, 100), range(0, 60, 5))
        )
    }

class ErrorWindow(QDialog):
    def __init__(self, error_message, fix_message, width, height):
        super().__init__()
        self.setWindowTitle(reg_helper['err_msg_window']['error_title'])
        self.setFixedSize(width, height)  # Set the desired size for the dialog

        # Create the main layout
        layout = QVBoxLayout()

        # Add the error icon (optional)
        error_label = QLabel(reg_helper['err_msg_window']['error_label']) 
        error_label.setStyleSheet(reg_helper['err_msg_window']['error_label_style'])
        layout.addWidget(error_label)

        # Add the error message
        main_message = QLabel(f"Error: {error_message}")
        main_message.setStyleSheet(str_hlpr['err_msg_window']['error_main_msg_style'])
        layout.addWidget(main_message)

        # Add the informative text
        info_message = QLabel(f"Fix: {fix_message}")
        info_message.setStyleSheet(str_hlpr['err_msg_window']['error_info_msg_style'])
        layout.addWidget(info_message)

        # Add OK button
        #
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # Close the dialog on click
        button_layout.addStretch(1)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)

        # Set the dialog layout
        self.setLayout(layout)

def show_error(error_message, fix_message, width, height):
    dialog = ErrorWindow(error_message, fix_message, width, height)
    dialog.exec()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set main window
        #
        self.setWindowLayout()
        self.setMinimumSize(750,750)

        # set a reference to results window
        #
        self.results_window = None

        # set a reference to an error window
        #
        self.error_window = None
        
    def setWindowLayout(self):

        # define layouts
        #
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # instantiate needed widgets
        #
        self.file_loader_hndlr = QPushButton(str_hlpr['main_window']['file_hndlr_str'])
        self.eval_hndlr = QPushButton(str_hlpr['main_window']['eval_hndlr_str'])
        grid_layout_hndlr = QWidget()
        self.grid_scroll_area_hndlr = QScrollArea()

        # set file loader widget properties
        #
        self.file_loader_hndlr.clicked.connect(self.load_file)

        # set evaluate widget properties 
        #
        self.eval_hndlr.clicked.connect(self.load_table)
        
        # set grid layout widget properties
        #
        self.setUpGrid(grid_layout)
        grid_layout_hndlr.setLayout(grid_layout)
        grid_layout_hndlr.setMinimumHeight(800)

        # Set up scroll area widget_properties
        #
        self.grid_scroll_area_hndlr.setWidgetResizable(True)
        self.grid_scroll_area_hndlr.setMinimumSize(500, 500)
        self.grid_scroll_area_hndlr.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.grid_scroll_area_hndlr.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.grid_scroll_area_hndlr.setWidget(grid_layout_hndlr)

        # connect all widgets to main layout
        #
        main_layout.addWidget(self.file_loader_hndlr)
        main_layout.addWidget(self.grid_scroll_area_hndlr)
        main_layout.addWidget(self.eval_hndlr)
        
        # Set the central widget for the main window
        #
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def setUpGrid(self, layout):

        propertys_d = str_hlpr['course_props']['course_props']
        self.line_edits = {property_d: {} for property_d in propertys_d}
        
        for col_idx, col_header in enumerate(str_hlpr['main_window']['grid_col_headers']):
            layout.addWidget(QLabel(col_header), 0, col_idx + 1)

        for course_num in range(1, 16):  
            layout.addWidget(QLabel(f"Course {course_num}:"), course_num, 0) 

            for col_idx, property_d in enumerate(propertys_d):
                line_edit = QLineEdit()
                self.line_edits[property_d][course_num] = line_edit
                layout.addWidget(line_edit,
                                 course_num,
                                 col_idx + 1,
                                 alignment=Qt.AlignmentFlag.AlignCenter)
        
    def load_table(self):

        data_dict = dict()

        propertys_d = str_hlpr['course_props']['course_props']
        data_dict = {property_d: {} for property_d in propertys_d}
        
        for line_edit in range(1,16):

            course_num = line_edit - int(1)
            
            crn = self.line_edits["CRN"][line_edit].text()
            
            if crn:

                
                for property_d in propertys_d:
                    
                    text = self.line_edits[property_d][line_edit].text()
                                        
                    if property_d == str_hlpr['course_props']['course_props'][int(1)]:
                        data_dict[property_d][course_num] = text
                                                
                    else:
                        
                        if len(text) == 0:

                            if property_d != str_hlpr['course_props']['course_props'][int(12)]:

                                data_dict[property_d][course_num] = int(-1)

                            else:
                                
                                data_dict[property_d][course_num] = int(0)
                        else:

                             data_dict[property_d][course_num] = text
                            
        data_frame = dft.create_data_frame_from_dict(data_dict)

        data_frame = dft.cleanup_data_frame(data_frame)
        
        comp_scheds = ct.create_courses(data_frame)

        if not self.create_results_window(comp_scheds):

            return False

        return True
    
    def load_file(self):

        dialog = QFileDialog()
        dialogSuccesful = dialog.exec()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        selected_files = dialog.selectedFiles()

        if len(selected_files) == 0:

            return False
        
        fileParse = dft.FileParser()
        
        data_frames = fileParse.parse_file_list(selected_files)

        data_frame = dft.combine_data_frame_list(data_frames)
        
        courses = dft.cleanup_data_frame(data_frame)

        comp_scheds = ct.create_courses(courses)

        if not self.create_results_window(comp_scheds):
            
            return False

        return True
    
    def create_results_window(self, comp_scheds):

        if not comp_scheds: 
            
            show_error(str_hlpr['err_msg_window']['err_course_creation'],
                       str_hlpr['err_msg_window']['err_course_creation_description'],
                       800,
                       200)
            
            return False  
        
        self.results_window = ResultsWindow()
        self.results_window.transfer_info(comp_scheds)
        self.results_window.setWindowLayout()
        self.results_window.show()
        
class ResultsWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(str_hlpr['results_window']['results_window_title'])
        self.setMinimumSize(750, 750)

    def transfer_info(self, data):

        self.data = data

    def insert_schedule(self, weekly_schedule, table, time_to_row):

        for course in weekly_schedule:
            
            for table_col, day in enumerate(course.weekly_schedule):
                
                start_time = day.start_time

                end_time = day.end_time
                
                if start_time != int(-1):

                    start_row = time_to_row[f"{start_time:04d}"]

                    end_row = time_to_row[f"{end_time:04d}"]

                    for table_idx in range(start_row, end_row + 1):
                        table.setItem(table_idx, table_col, QTableWidgetItem(str(f"{course.CRN}:{course.name}")))
                        
    def setWindowLayout(self):
        
        main_layout = QVBoxLayout()

        # Set up scroll area widget_properties
        #
        self.schedule_scroll_area_hndlr = QScrollArea()
        self.schedule_scroll_area_hndlr.setWidgetResizable(True)
        self.schedule_scroll_area_hndlr.setMinimumSize(700, 700)
        self.schedule_scroll_area_hndlr.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.schedule_scroll_area_hndlr.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        for comp_sched_num, comp_sched in enumerate(self.data):

            weekly_sched_str = \
                f"schedule number : {comp_sched_num}, priority : {ct.fetch_priority_stat(comp_sched)}"
            
            main_layout.addWidget(QLabel(weekly_sched_str))
            table_layout = QTableWidget(169, 5)
            table_layout.setHorizontalHeaderLabels(str_hlpr['results_window']['results_window_header'])
            
            table_layout.setVerticalHeaderLabels(list(time_to_row.keys()))
            table_layout.verticalHeader().setDefaultSectionSize(1)
            table_layout.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table_layout.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table_layout.setMinimumSize(700, 400)
            
            # Example: Add an event
            self.insert_schedule(comp_sched, table_layout, time_to_row)
            main_layout.addWidget(table_layout)
            
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.schedule_scroll_area_hndlr.setWidget(central_widget)
        self.setCentralWidget(self.schedule_scroll_area_hndlr)                  
