To run project in virtualenv, do those steps:
1. Install "virtualenv" via pip

2. Create virtualenv "env" folder by using:
	"py -3 -m virtualenv env"
	on linux: "virtualenv env"
	
3. Activate virtualenv:
	"env\Scripts\activate" (.ps1 - PowerShell script)
	on linux: ". env/bin/activate" or "source env/bin/activate" (.sh - bash script)
	
Note1: 	When "Script cannot be loaded because running scripts is disabled on this system" run in cmd: "powershell Set-ExecutionPolicy RemoteSigned"
	After all you can deactivate this policy by running in cmd: "powershell Set-ExecutionPolicy Restricted"
	from: https://stackoverflow.com/questions/4037939/powershell-says-execution-of-scripts-is-disabled-on-this-system
Note2: 	1) "./script" runs the script as an executable file, launching a new shell to run it
	2) ". script" or "source script" reads and executes commands from filename in the current shell environment
		
4. Install required packages via pip: "flask" and "flask-sqlalchemy".
Installed libraries should be visible in "env\Lib\site-packages" folder

Note: 	Don't use "py -3 -m pip install ...". Here our python.exe is in folder "env\Scripts" (In cmd you can use "where python" and see where it is)
	So just simply use "python -m pip install ..."
		
5. Run prepared scipt with:
	"python srsc/app.py" (or change directory of main file)
	
Note: Server runs at url: "localhost:5000"

6. Deactivate virtualenv (while beeing in active environment):
	"deactivate"


Additional:
a) Creation of database:
- Enable virtualenv (3rd point),
- Move to "src" folder,
- Run "python" and write:
>>> from app import app, db
>>> app.app_context().push()
>>> db.create_all()
Db is created in folder "src\instance\test.db"

b) Updating database (https://flask-migrate.readthedocs.io/en/latest/):
- Enable virtualenv (3rd point),
- Move to "src" folder,
- Install pip "Flask-Migrate" package,
- In project import "flask_migrate" from "Migrate" and create instation of migration: "migrate = Migrate(app, db)",
- In opened virtualenv terminal do:
	- Create migration repository: "python -m flask db init",
	- Generate initial migration: "python -m flask db migrate -m 'Initial migration.'",
	- Apply changes described in migration script to db: "python -m flask db upgrade".	

Each time the database models change, repeat the "migrate" and "upgrade" commands.
