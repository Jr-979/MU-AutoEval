@echo off
py -m pip install -r %~dp0\requirement.txt%
py %~dp0\evaluation.py%
