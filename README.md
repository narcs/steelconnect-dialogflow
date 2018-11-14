# steelconnect-dialogflow
A webhook for handling SteelConnect API calls using Google Dialogflow (https://dialogflow.com)

**_NOTE 1:_**  Formatting of text has been done to suit Slack, which supports markdown. It hasn't been tested with other integrations such as Messenger
## Setting up Firestore Database (Prerequisite)
1. Login to Firebase at https://firebase.google.com/
2. Go to console in the top right
3. Add a new project. Note project name
4. Create `config.py` and place in app root directory. Assign variable `firestore_project_id` to project name. Use `config.py.example` as a template
5. Open newly created project
6. Open main menu. Under 'Develop' section go to 'Database'
7. Create Firestore database
8. Select and enable 'Start in test mode' for Firestore security rules. Rule generated should be as follows:
```
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write;
    }
  }
}
```
## How to set up for local development
* Clone the repo.
* Install Python 2.
* Install dependencies by running `pip install -r requirements.txt`
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
* Copy `default-auth.json.example` to `default-auth.json` and fill it out with the details of your SCM account and organisation.
* Deploy the app by opening Google Cloud SDK Shell/terminal, navigate the apps directory via 'cd /path/to/steelconnect-dialogflow/' and run 'gcloud app deploy'.

### Using Dialogflow
* Click the settings icon next to your agent's name.
* Click 'Export and Import' and then select 'Restore from Zip'
* Upload the 'SteelConnect-Dialogflow-Agent.zip' file from the repository to get started.
* Enable the webhook under Fullfillment and use 'https://your-project-id.appspot.com/webhook/' as the url.
* Lastly, change the organisation value under Intents -> ListSites to your own organisation name as this is used in some of the responses.

You can now use Dialogflow to the test out the intents on your realm and organisation. Have a look at the Dialogflow intents what you can do, you can add/delete to suit your needs.

<!-- Adding this here because I think it'll be useful for future peeps -->
# Known Bugs And Limitations
* Newline characters are not rendered in Dialogflow Web Demo
  E.g. In the code, we may have something like:
  ```
    speech = "First Name: Rick, \nLast Name: Rolling, \nFavourite Pokemon: Magikarp"
  ```

  In DialogFlow, it will be rendered as: 
  ```
    "First Name: Rick, \nLast Name: Rolling, \nFavourite Pokemon: Magikarp"
  ```

  Instead of:
  ```
    "First Name: Rick,
     Last Name: Rolling,
     Favourite Pokemon: Magikarp"
  ```  
  + This is not an issue in Slack

* SteelConnect cannot identify if a city does not exist in a country. It will create a site regardless if the city-country pairing       doesn't make sense. 
  I.e. If you say `create a site in Beijing, Australia`, a site will be created and saved as Beijing, Australia despite the fact that there is no city named Beijing in Australia. 

  Due to the confusing city-country pairing, the site will not be shown the the SteelConnect Map

* In SteelConnect Manager, (and as specified by Shannon) you should not be able to delete RouteVPNs, however if you query the API directly (as we are doing with Dialogflow), you will be to

* DialogFlow only recognises major cities. This means that cities such as "Melbourne" and "New York City" gets recognised, however lesser known cities such as "Gisborne South" and Noble Park" aren't

* DialogFlow will timeout if there is too much content that needs to be passed in. 
  + E.g. For the `List Uplinks` method, it will claim that there is a problem if there are approximately 75 uplinks present and not show it. However, the method works fine (as shown in Google Cloud Platform)

<!-- Adding this here because I think it'll be useful for future peeps, but also because I forgot quite a few stuff that'll be nice reminders after not touching the code for a while -->
# Hints And Tips
* Remember to name the action in the Action And Parameter section in DialogFlow
* Remember to 'Enable Webhook Call For This Intent' in the Fulfillment section when creating a new intent in DialogFlow
* After importing/restoring/uploading files into DialogFlow, the system may not work by constantly printing "Not Available" after invoking each intent. It may be due to the fulfillment section being overwritten. Go to the Fulfillment section on the left, and ensure that the URL field contains the webhook URL for your project
* If there are issues finding out the causes of bugs in DialogFlow, try going to Google Cloud Platform Error Reporting and/or Logging on the left pane to see the stack trace and the possible cause of the bug
* The registration of actions in app.py has been separated according to the entity for easy readability
  + I.e. Uplink actions are grouped together, site actions are grouped together

# Setting Up Testing
**_DISCLAIMER 1:_**  These test cases will be interacting with dynamic information and hence may fail. For the purposes of testing, **please do not delete the HQ site and Mothership site**, as we want to minimise the likelihood of a test failing

**_DISCLAIMER 2:_**  These test cases will take some time (it can take up to 15 seconds per test) due to it communicating with DialogFlow and the SteelConnect systems. 

* Please follow instructions from https://chatbotsmagazine.com/3-steps-setup-automated-testing-for-google-assistant-and-dialogflow-de42937e57c6
    + A sample template json file has been provided, but you will need to rename it to `botium.json`
    + Other useful links are:
        - Source code for Botium: https://github.com/codeforequity-at/botium-cli
        - To find out more about Botium: https://github.com/codeforequity-at/botium-core/wiki/The-Botium-CLI
        - To include extra configurations: https://github.com/codeforequity-at/botium-core/wiki/Botium-Configuration

If you can't connect to DialogFlow or Botium doesn't work, here are some reasons why:
* You may be working on the wrong DialogFlow file. Click on the down caret to the left of the settings button in DialogFlow and change to the correct project
* Ensure the fulfillment URL has been filled out. It may have be overwritten after importing/restoring/uploading files to DialogFlow files

## Testing Requirements/Preconditions:
Tests are run in alphabetical order, so please be careful when naming the .convo.txt especially when there are dependencies. 

The following refers to preconditions that need to be met before running `botium-cli run`
* The HQ site must exist on Clayton, Australia
* The Mothership site must exist on Alice Springs, Australia
* There must not be any appliances on the HQ site
* The Headquarters site (in Clayton, Australia) and Mothership site (in Alice Springs, Australia)  must exist 

## Some Useful Botium Commands:
* To start Botium: `botium-cli emulator`
* To change Botium export files to automated-test-cases: `export BOTIUM_CONVOS=./automated-test-cases`
* to run Botium tests: `botium-cli run`
* To open up a browser UI with the test cases: `botium-cli emulator browser --convos=./spec/convo`

## Untested/Deprecated Functionalities:
The following actions have not been tested out and are deprecated. It has been left in the respository for future possible use:
- Add site to wan
- Add sites to wan
- Clear sites
- Create SSID
- Create Zone

# To Do
* Validate same city names and differents country pairings (E.g. Differentiate between Sydney Canada and Sydney Australia)
* When getting information about uplinks and appliances, we currently have it such that DialogFlow passes information back to the code here, and gets saved so that it can be used for a followup action later on. This feels dirty, and we would ideally like to make it such that the information is stored on DialogFlow (or some other cleaner way) so that it can be retrieved there rather than having to pass it backwards and forwards. 
* Create the ability to get site by id without being dependent on the city and country parameters
  + This will reduce the number parameters needed when invoking an intent
  + E.g. When making an uplink, we have 5 parameters: UplinkName, SiteName, City, Country, WAN. If we can remove the City, and         Country parameter, we will only have at most 3 parameters to deal with in any intent
  + If this is done, the `convo.txt` files in the /steelconnect-dialogflow/automated-test-cases files needs to be updated to remove City, and Country parameters 
* Prevent users from deleting routeVPNs via DialogFlow
* Do a Postman and Newman Proof Of Concept to test the SteelConnect API
* List the available sites/appliances/WANs/Uplinks when making a query or deleting one of those entities. It should look something like this:
  ```
  User: Delete a site
  Bot: Which site would you like to delete? Please select a number corresponding to the available sites:
        1. Branch in Adelaide, Australa
        2. Shop in Perth, Australia
        3. DC in Darwin, Australia
  User: 2
  Bot: The Shop in Perth, Australia has now been deleted
  ```
* Move botium test cases to a separate realm so that dynamic data/information can also be tested
* Port DialogFlow V1 to V2 and make adjustments based on those changes
