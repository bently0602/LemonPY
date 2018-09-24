@echo off
REM https://stackoverflow.com/questions/8287628/proxies-with-python-requests-module

set http_proxy=socks5://127.0.0.1:1337 
set https_proxy=socks5://127.0.0.1:1337

taskkill /f /im python.exe
C:\ProgramData\Anaconda3\python Main.py
