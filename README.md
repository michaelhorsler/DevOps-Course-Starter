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

# Setting up the MongoDb Integration

Pre-requisite: This app uses a Mongo Database for storing todo items. Therefore a Mongodb database and connection string is required. These are referenced by Global Variables within `.env` - 
  MONGO_CONN_STRING, MONGODB.
These are required to achieve correct operation.

## Data Encryption in Azure Cosmos DB

All Azure Cosmos DB data is now encrypted in transit (over the network) and at rest (nonvolatile storage), providing end-to-end encryption.

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

Integration test stored in test_Mongo_Integration.py within the tests folder.
Pre-requisite: Database connecton string is patched with fake values. These are referenced by Global Variables within `.env.test` - 
  MONGO_CONN_STRING
These are required to achieve correct operation. This test confirms default route request to index page with assertion of returned action.
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

A Multi-stage build has been implemented to invoke either Production, Development or Test modes within the TodoApp. Built via the following commands to create seperate container VM's: 

```
$ docker build --target development --tag todo-app:dev .
$ docker build --target production --tag todo-app:prod .
$ docker build --target test --tag todo-app:test .
```
Binding to the local folder structure to allow for easy code updates without rebuild:

```
docker run --mount type=bind,source=$(pwd)/todo_app,target=/app/todo_app --env-file .env --publish 127.0.0.1:5000:5000  todo-app:dev

docker run --env-file .env --publish 127.0.0.1:5000:5000  todo-app:test
```
Build and Run commands to execute tests:
```
$ docker build --target test --tag todo-app:test .

docker run --env-file .env.test --publish 127.0.0.1:5000:5000  todo-app:test

docker run --env-file .env.test --publish 127.0.0.1:5000:5000  todo-app:test todo_app/tests/test_Trello_Integration.py

docker run --env-file .env.test --publish 127.0.0.1:5000:5000  todo-app:test todo_app/tests/test_view_model.py
```

## Creating an Azure WebApp utilising a Docker image

Utilising the Production image build the application is built and pushed to the Docker repository. Logging in to Azure and Docker within VsCode allows command line interractions with the deployment systems.

```
$ az login
$ docker login
$ docker build --target production --tag michaelsminis/todo-app:latest .
$ docker push michaelsminis/todo-app:latest
```
Docker Image address:
```
https://hub.docker.com/r/michaelsminis/todo-app
```

The next stage is to create an App Service Plan within Azure to manage the WebApp, and create a WebApp referencing the Docker container as the source image.

```
$ az appservice plan create --resource-group Cohort31_MicHor_ProjectExercise -n mrh-todoapp-serviceplan --sku B1 --is-linux
$ az webapp create --resource-group Cohort31_MicHor_ProjectExercise --plan mrh-todoapp-serviceplan --name mrh-todoapp --deployment-container-image-name hub.docker.com/r/michaelsminis/mrh-todoapp:latest
```

The WebApp requires the environment variables to be updated in order to access the Trello board etc. Updating these via json eliminates the requirment of adding each variable independently. Therefore a env.json has been created and added to .gitignore to prevent the details being shared publicaly.

```
$ az webapp config appsettings set -g Cohort31_MicHor_ProjectExercise -n mrh-todoapp --settings @env.json
```
Executed via Gitbash, the following Webhook returns a link to a log-stream relating to the re-pulling of the image and restarting of the app:

```
$ curl -dH -X POST "Webhook address within env."
```
This site can currently be accessed at:
```
<https://mrh-todoapp.azurewebtsites.net>
```
Ci/Cd Github pipeline updated to include build of the Production image if the Tests were passed successfully and committed via main branch as a push request. 
This is deployed to Docker Hub via use of environment variables with Github Actions: 
```
DOCKERHUB_USERNAME, DOCKERHUB_TOKEN
```
Deployed to Azure via use of Webhook contained within Github environment variable:
```
AZURE_WEBHOOK
```

## Vulnerability and Encryption-at-rest and in-transit

Inclusion of external references and packages can introduce potential vulnerabilities into the code structure when external code is modified relevant to your own original intended use. Therefore within the Ci/Cd pipeline, we now invoke vulnerability scanning for all referenced packages to highligh any potential security weakness.
This is achieved via the safety tests in the ci-pipeline.yml:
```
  - run: docker run --entrypoint poetry todo-app:test run safety check
    continue-on-error: true
```

Encryption-in-transit has been added to the project in the form of OAuth authentication to secure communications to and from the app and the user. As mentioned previously, the Cosmos Mongo DB has security applied via the host Azure.
In order to handle the OAuth communication additional secret variables have been added to the .env file as follows:
```
OAUTH_TEST_CLIENT_ID, OAUTH_TEST_CLIENT_SECRET, 
OAUTHLIB_INSECURE_TRANSPORT, OAUTH_CLIENT_ID, 
OAUTH_CLIENT_SECRET
```
These relate to the OAuth apps generated within Azure.

## Provisioning Role for CI/CD
For a CI/CD process to run infrastructure commands, such as Terraform, a specific provisioning role must be created/enabled for use.

Run the following command using the Azure CLI to provision a specifc role for use, updating the role_name, subscription_id and resource_group_name accordingly

```
az ad sp create-for-rbac --name "role_name" --role Contributor --scopes /subscriptions/subscription_id/resourceGroups/resource_group_name
```
Note the response values, these are needed within the CI/CD pipeline and stored within the GitHub Secrets.

## Terraform

The project uses Terraform to deploy its cloud solution using Infrastructure As Code (IAC). Install the appropriate version from their website: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

## Terraform Commands
To run Terraform locally, ensure that the variables.auto.tfvars is completed. Then log into Azure using the Azure CLI tool previously installed, selecting the necessary subscription id.

Additionally, within main.tf ensure that the correct backend is referenced within the backend "azurerm" property

```
$ az login 
- Select subscription
$ terraform init
$ terraform plan
```
The plan will validate the cloud state vs local script, compare and identify changes necessary.

```
$ terraform apply
- Runs a plan and asks to confirm before applying changes
$ terraform apply --auto-approve
- Runs a plan and then automatically applys the changes
```

## Logging
Logging is conducted via action replication to the console and to an external logging application called Loggly.
The level of logging is adjusted via use of the LOG_LEVEL variable. This can produce full logging when set to DEGUG or error logging only when set to ERROR (as per production.)

2 additional variables are stored within the .env file:
```
LOG_LEVEL
LOGGLY_TOKEN
```
The Loggly Token provides an external logging route to store and record the logs. Logs include User id, function performed and database id of corresponding item.
