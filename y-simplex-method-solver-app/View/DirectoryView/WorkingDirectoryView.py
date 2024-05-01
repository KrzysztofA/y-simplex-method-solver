from PyQt6.QtCore import Qt, QDir
from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel
import os
from Model import SimplexFile
from Controller import SettingsController, SaveLoadController
from typing import Callable, NoReturn, List
import pathlib


class WorkingDirectoryView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setDragEnabled(False)
        self.file_view = QFileSystemModel()
        self.file_view.setReadOnly(True)
        print(self.file_view.rootPath())
        self.file_view.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.Files | QDir.Filter.AllDirs)
        self.file_view.setNameFilters(["*.yse"])
        self.file_view.setNameFilterDisables(False)
        self.file_view.setRootPath(SettingsController().settings.default_save_dir)
        self.file_view.insertRow(0)

        self.setModel(self.file_view)
        self.file_view.setRootPath(SettingsController().settings.default_save_dir)
        self.setRootIndex(self.file_view.index(SettingsController().settings.default_save_dir))
        self.clicked.connect(self.on_clicked)
        self.open_file_callbacks: List[Callable[[SimplexFile], NoReturn]] = []

        for i in range(1, self.file_view.columnCount()):
            self.hideColumn(i)

    def move_up_directory(self):
        pure_path = pathlib.PurePath(self.file_view.rootPath())
        if pure_path == pure_path.parent:
            self.file_view.setRootPath(self.file_view.myComputer())
            self.setRootIndex(self.file_view.index(self.file_view.rootPath()))
        else:
            self.file_view.setRootPath(str(pure_path.parent))
            self.setRootIndex(self.file_view.index(self.file_view.rootPath()))

    def on_clicked(self, index: int):
        file_path = self.file_view.filePath(index)
        if os.path.isdir(file_path):
            self.file_view.setRootPath(file_path)
            self.setRootIndex(self.file_view.index(file_path))
            return
        simplex_file = SaveLoadController().load(file_path)
        for callback in self.open_file_callbacks:
            callback(simplex_file)


