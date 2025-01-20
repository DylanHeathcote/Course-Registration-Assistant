#!/usr/bin/env python

import sys
from PyQt6.QtWidgets import QApplication
import event_loop_tools as elt

def main(argv):
     """
     function: main

     arguments: none

     return: boolean value idicating status

     description:
      This is where the method where everything is processed
    """

     app = QApplication([])
     Gui = elt.MainWindow()
     Gui.show()
     app.exec()
     
if __name__ == "__main__":          
     main(sys.argv)
