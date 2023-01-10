@echo off
echo.
echo.
echo Windows Print Management Dashboard
echo **********************************
echo 1. Dashboard
echo 2. API
echo.
set app_name=1
set /p app_name="Choose your option [1] or [2]: "

echo Activating conda environment...
call activate print-server
echo.

if '%app_name%' == '1' (
set port_number=8501
set /p port_number="Enter your port number [8501]: "
echo Running dashboard on %port_number% ...
streamlit run dashboard.py --server.port %port_number%
)

if '%app_name%' == '2' (
set port_number=5000
set /p port_number="Enter your port number [5000]: "
echo Running API on %port_number% ...
python api.py --port %port_number%
)
