import json
import wget
import os
import sys, subprocess
from PyPDF2 import PdfReader

import win32api
import win32print
from time import sleep
with open('config.json') as f:
    config = json.load(f)
    libpath = config['libpath']
    tmppath = config['tmppath']
    tmp_clean_time = config['tmp_clean_time']
    paper_size = config['paper_size']
class Printer():
    def __init__(self, _filename):
        self.filename = _filename
        self.SumatraPDF_PATH = f"{libpath}/SumatraPDF.exe"
        self.currentprinter = win32print.GetDefaultPrinter()
        self.status = "Success"
        self.error_list = []
    @staticmethod
    def get_default_printer():
        return win32print.GetDefaultPrinter()

    def check_pdf_vaild(self):
        try:
            PdfReader(self.filename)
        except Exception as e:
            self.status = "Fail"
            self.error_list.append(str(e))

    def chk_offline(self):
        handle = win32print.OpenPrinter(self.currentprinter)
        attributes = win32print.GetPrinter(handle)[13]
        return (attributes & 0x00000400) >> 10

    def del_trash(self, file_path):
        subprocess.Popen(f"python -c \"import os, time; time.sleep({tmp_clean_time}); os.remove('{file_path}');\"")

    def printer(self):
        try:
            # print(f'-ghostscript "{self.GHOSTSCRIPT_PATH}" -printer "{self.currentprinter}" "{self.filename}"')
            win32api.ShellExecute(0, 'open', self.SumatraPDF_PATH, f' -print-to-default -print-settings "paper={paper_size},fit"  "{self.filename}"', '.', 0)
        # -g378x567
        except Exception as e:
            self.status = "Fail"
            self.error_list.append(str(e))

    def run(self):
        if self.chk_offline():
            self.status = "Fail"
            self.error_list.append(f"{self.currentprinter} is offline")
        else:
            self.check_pdf_vaild()
            self.printer()
            self.del_trash(self.filename.replace("\\","\\\\"))
