from PyQt6.QtWidgets import QTabWidget
from Model import SimplexFile
from typing import List
from .FileView import FileView
from Controller import SettingsController
import os


class FileTabBar(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDocumentMode(True)
        self.open_file_paths: List[str] = []
        self.open_files: List[FileView] = []
        self.setTabShape(QTabWidget.TabShape.Triangular)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabBar().tabMoved.connect(self.tab_moved_event)
        self.tabBar().tabCloseRequested.connect(self.tab_close_requested)

    def set_current_file(self, file: SimplexFile):
        if file.filedir in self.open_file_paths:
            return
        self.setTabText(self.currentIndex(), file.filename)
        if len(self.open_files) == 0:
            self.add_file(file)
        else:
            self.open_file_paths.append(file.filedir)
            self.open_files[self.currentIndex()].set_file(file)

    def collect_current_file(self):
        return self.open_files[self.currentIndex()].collect_file()

    def add_new_file(self):
        self.open_files.append(FileView())
        self.addTab(self.open_files[-1], SettingsController().settings.default_save_name)
        self.setCurrentIndex(len(self.open_files) - 1)

    def change_tab_name(self, new_name: str):
        self.setTabText(self.currentIndex(), new_name)

    def add_file(self, file: SimplexFile):
        if file.filedir in self.open_file_paths:
            return
        self.open_files.append(FileView(file))
        self.open_file_paths.append(file.filedir)
        self.addTab(self.open_files[-1], file.filename)
        self.setCurrentIndex(len(self.open_files) - 1)

    def tab_moved_event(self, old_tab_index: int, new_tab_index: int):
        temp = self.open_files[old_tab_index]
        self.open_files.pop(old_tab_index)
        self.open_files.insert(new_tab_index, temp)

    def tab_close_requested(self, index: int):
        temp = self.open_files[index]
        if temp.directory in self.open_file_paths:
            self.open_file_paths.remove(temp.directory)
        self.open_files.pop(index)
        self.removeTab(index)

    def current_file(self):
        if len(self.open_files) == 0:
            return False
        return self.open_files[self.currentIndex()]

    def set_all_view(self, index: int):
        for i in self.open_files:
            i.output_box.set_view(index)
