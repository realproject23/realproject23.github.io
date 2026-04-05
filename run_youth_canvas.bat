@echo off
cd /d "C:\anti\real_project"
call .\.venv\Scripts\activate
start /b python -m uvicorn main:app --port 8000 --host 0.0.0.0
exit
