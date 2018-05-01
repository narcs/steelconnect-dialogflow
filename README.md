# steelconnect-dialogflow

A webhook for handling SteelConnect API calls using Google Dialogflow (https://dialogflow.com)

## How to set up for local development
* Clone the repo.
* Install Python 2.
* Install and configure the Google Cloud SDK by following the instructions here - https://cloud.google.com/sdk/docs/. On Windows this will install the Google Cloud SDK Shell which can be used to deploy the app, on OSX and Linux simply use the terminal.
* Install the app engine python extension by entering 'gcloud components install app-engine-python' into the Google Cloud SDK Shell if on Windows or the terminal for OSX and Linux
* Run the app from the repo with `dev_appserver.py app.yaml`.

## How to install on Google App Engine

### Creating a Google App Engine project
* Go to https://console.developers.google.com/apis/dashboard.
* Select 'Select a project' in the top left.
* Create a new project using the '+' button
* The projects id will be used as its address (app-id.appsport.com). Write your projects' id down as you will need it later.

* Install and configure the Google Cloud SDK by following the instructions here - https://cloud.google.com/sdk/docs/. On Windows this will install the Google Cloud SDK Shell which can be used to deploy the app, on OSX and Linux simply use the terminal.
* Install the app engine python extension by entering 'gcloud components install app-engine-python' into the Google Cloud SDK Shell if on Windows or the terminal for OSX and Linux

You can either clone the repository using git or download the zip file.

### Cloning using Git
* If git is not already installed get it here https://git-scm.com/.
* Clone this project using `git clone https://github.com/narcs/steelconnect-dialogflow.git`.

### Downloading the Zip
Use this link: https://github.com/narcs/steelconnect-dialogflow/archive/master.zip.

### Deploying
* Fill out 'default-auth.json' with the details of your SCM account and organisation.
* Deploy the app by opening Google Cloud SDK Shell/terminal, navigate the apps directory via 'cd /path/to/steelconnect-dialogflow/' and run 'gcloud app deploy'.

### Using Dialogflow
* Click the settings icon next to your agent's name.
* Click 'Export and Import' and then select 'Restore from Zip'
* Upload the 'SteelConnect-Dialogflow-Agent.zip' file from the repository to get started.
* Enable the webhook under Fullfillment and use 'https://your-project-id.appspot.com/webhook/' as the url.
* Lastly, change the organisation value under Intents -> ListSites to your own organisation name as this is used in some of the responses.

You can now use Dialogflow to the test out the intents on your realm and organisation. Have a look at the Dialogflow intents what you can do, you can add/delete to suit your needs.
