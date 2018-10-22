#!/usr/bin/python
# -*- coding: utf-8 -*-

app_title = "Notion to PDF"
app_description = ""
main_python_file = "main.py"

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable(main_python_file, base=base)
]

setup(
    name=app_title,
    version = '0.1',
    description = app_description,
    options = dict(build_exe = buildOptions),
    executables = executables
)