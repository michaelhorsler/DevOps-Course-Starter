# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

# Setting up the Trello API Integration

Pre-requisite: This app uses Trello API for storing todo items. Therefore a Trello account is required with a created board, API Key and Token. These are referenced by Global Variables within `.env` - 
  TRELLO_API_KEY, TRELLO_API_TOKEN, TRELLO_BOARD_ID, TRELLO_ACTIVE_LIST_ID, TRELLO_TODO_LIST_ID, TRELLO_DONE_LIST_ID.
These are required to achieve correct operation.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

Unit tests are stored in test_view_model.py within the tests folder. 
Three unit tests check the status of a pre-determined list confirming 3 possible status of "To Do", "Active" and "Complete".

Integration test stored in test_Trello_Integration.py within the tests folder.
Pre-requisite: API key and token are patched with fake values. These are referenced by Global Variables within `.env.test` - 
  TRELLO_BOARD_ID, TRELLO_TODO_LIST_ID, TRELLO_ACTIVE_LIST_ID, TRELLO_DONE_LIST_ID.
These are required to achieve correct operation. This test confirms default route request to index page with assertion of returned card name.
Testing command for operation: `poetry run pytest`

## Deploying the application via Ansible

To deploy the application via Ansible, copy the `ansible` folder to the host node, update the inventory file (to include the control nodes to deploy to) and run the following command:

```
ansible-playbook my_ansible_playbook.yml -i my_server.ini
```

>Please Note you will need to setup passwordless SSH access from the host to each of the managed nodes.

## Utilising Docker to build and deploy the application

Contained docker images have been created to deploy the application within a controlled VM. The Dockerfile installs the required support applications and creates an entrypoint command setting up the Todo Application. The sensitive configuration variables are imported via the .env file on the command line. Port 5000 is exposed for viewing the Todo App via your browser on localhost.:

```
docker run --env-file .env --publish 127.0.0.1:5000:5000 todo-app:prod
```

A Multi-stage build has been implemented to invoke either Production or Development modes within the TodoApp. Built via the following commands to create seperate container VM's: 

```
$ docker build --target development --tag todo-app:dev .
$ docker build --target production --tag todo-app:prod .
```

Binding to the local folder structure to allow for easy code updates without rebuild:

```
docker run --mount type=bind,source=$(pwd)/todo_app,target=/app/todo_app --env-file .env --publish 127.0.0.1:5000:5000  todo-app:dev
```