Event Scheduler V 0.0.1

Contact Info:
Curtis Thomas
curtis.thomas2@snhu.edu

IMPORTANT:
This project relies on a virtual environment established at the same level as the root directory. The virtual environment must be created and run
on the local machine in order to ensure consistent behavior. 

IMPORTANT:
In order to begin with this project, some bootstrapping is needed. It is necessary to use the pytest at tests/crud/test_user.py and hardcode 
the values for the user, making sure that all boolean values are set to true. On running (using BASH, 'pytest -v path/to/file.py'), the user values
will be in db. 

IMPORTANT:
Much of this program is dependent on an ENV file being configured. Use the following configurations in a root-level .env file
    PYTHONPATH = "APP"
    POSTGRES_SERVER = "localhost:5432"
    POSTGRES_USER = [your postgres server name]
    POSTGRES_PASSWORD = [Your postgres server password]
    POSTGRES_DB = ""
    FIRST_SUPERUSER_PASSWORD = [generate a superuser password]
    PYTEST_PASSWORD = [use your first superuser password; pytest is configured to use user_id 1]



IMPORTANT:
Hardcode run a permissions create pytest and record the permission id BEFORE creating a user, that way you can pass the permission id to 
your user when you create it. 

to run alembic in order to build tables, open bash and enter 'alembic revision --autogenerate -m [your message in single quotes]'
then run 'alembic upgrade head'. 

To start the server, run uvicorn by typing into BASH 'uvicorn app.main:app', ctrl+c to stop the server.

How it works:
The 'api' section here provides the callable functionality of the code that will be used by a website. The basic idea is that when a call is made to the
apirouter's url (for example, @get /user/food/beans), the code at the endpoint then sends a call to the crud layer, which uses the schema to create a dictionary
style data structure with some basic validation, which is then applied to a model (where applicable) and passed to the database. The returned data is then passed back to
the client. {['name':'cannelini'],['name':'garbanzo']}. When a call is made to an endpoint, there is first a check to see if the user is logged in or in posession of a
web token, followed by another check against the user's permissions (identified by the permissions id, which identifies different sets of permission constellations). 
If a usuer has permission, then the program proceeds to check the data against the schema (schema enforcement is nearly none in normal crud calls). Once the 
data has been validated against the schema, it is then passed on through to or from the database in the appropriate fashion.

The order for setup should first be to establish permissions (grant full) in the db, followed by the first user so that the permissions can be given to the user.
This is most easily accomplished by temporarily hard-coding some pytest values. 

Trying it out:
Under the tests section, there are several pytests that should be able to confirm if the crud layer is working. In its current state, the tests pass for the author. 

Additional guidance:
Text documents have been left in some layers of this project to help quickly explain the role of that layer and how to work with it. 