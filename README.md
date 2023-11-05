# CSC4022-TuringTribe
Group Project of the Turing Tribe group in the CSC4022 Course. To install and run the Django web framework, clone and read the installation instruction within the FinApp folder.

## Install Instructions

1) Clone Repo to Local Machine
    - "git Clone https://github.com/AaDGarrison/CSC4022-TuringTribe.git"

2) Python Virtual Environment Setup
	- Go into CSC4022-TuringTribe\FinApp Directory and create a folder called "PythonEnvironment".
	- Open CMD and Navigate to FinApp directory of Repo "CSC4022-TuringTribe\FinApp".
	- Run "python -m venv ./PythonEnvironment".
	- Activate your virtual environment ".\PythonEnvironment\Scripts\activate".
		- Should see Python Envroment come up in the bottom left.
		- Run "pip install -r requirements.txt".
	- Open VsCode, open folder CSC4022-TuringTribe\FinApp
		- Shift+Ctrl+P Select interpreter and select the python.exe that is in the PythonEnvironment Directory.
			- This should stay active for all future times opening visual studio code.
			- I recommend downloading Python Environment Manager since you can see all local venv as well.

3) Running Application from Vscode
	- Open Visual Studio Code 
	- Open FinApp Folder
	- "python manage.py runserver"

4) Adding a Dependency
	- Go into CSC4022-TuringTribe\FinApp Directory
	- Activate your virtual environment ".\PythonEnvironment\Scripts\activate"
	- "pip install "dependency""
	- "pip freeze > requirements.txt"
	- git commit changes to requirements.txt for everyone else
	- git push

5) Run Django Test
	- Using CMD go into CSC4022-TuringTribe\FinApp directory
	- Activate your virtual environment ".\PythonEnvironment\Scripts\activate"
	- Run python manage.py runserver
	- Open http://127.0.0.1:8000/ and verify that a Django page has opened


6) If you are having security issues and see the following error 
    Visual studio code cmd error: Cannot be loaded because running scripts is disabled on this system
    open this page and follow the directions 
    https://stackoverflow.com/questions/56199111/visual-studio-code-cmd-error-cannot-be-loaded-because-running-scripts-is-disabl
