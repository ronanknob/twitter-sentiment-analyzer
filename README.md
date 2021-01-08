# Twitter sentiment analyzer

## Objective
This app aims to collect a stream of portuguese tweets from Twitter API. The app analyzes the tweet text and classifies the sentiment of the text as **positive** or **negative**. The app stores the original tweet text and the result sentiment into a CSV file, wich is plotted with live updates into a HTML dashboard.

## Requisites
To run this app you'll need a Python 3 installed and the pip package manager.

## How to use this app
Obs: The commands in instructions aim the Debian-based linux distros. If you use pip3 command, replace pip by pip3 in the following commands.

1. Install the dependencies -> pip install -r requirements.txt
2. Configure the access credentials for the Twitter API in the credentials.py file.
3. Execute the app file -> run the command "python3 app.py" on a terminal. The app will start and should create the file "tweets_output.csv" to persist the informations. Don't go to the next step before execute the app file, because the dashboard loads data from this file.
4. With the app running, execute in other terminal the dashboard app -> python3 dashboard.py. The console should return the URL for the dashboard (ex: http://127.0.0.1:8050/). Open this URL in a browser (tested on latest versions of Firefox and Chrome), and you will see the real-time data beeing processed, with 3 seconds interval on data refreshing.
5. If you need to interrupt the executions, do a break on the terminals (usually ctrl+c)

## The versions

### V 1.0.0
The version 1 of the project aimed to test the hole system. So, the structure of the project was created, the frameworks for manipulate the Twitter API and plot the results into a dashboard was tested in this version. 
For the sentiment analysis, i've used a popular package (Textblob) to obtain the sentiment analysis, but the objective is to replace this part by a personal classifier in the next version of the app.
For persist the result i choosen a CSV, because of a good compatibility with panda dataframes, used on dashboard. This type of persistence bring some problems to scale the application, so need to be replaced to provide more scalability to the app.

## Develop decisions
During the develop process, some decisions about the framework and the flow are maded. The relevant ones are described below:
* I've searched a good framework to do the dashboard. [Streamlit](https://www.streamlit.io/) and [Plotly](https://plotly.com/) seems two popular packages and well maintained projects in Github, with free versions. I've tried first with Streamlit, but the "protobuf" dependency show some problems on execution. I've researched for the solution and apply some solutions but din't work. To not loose much time on that matter i change to plotlty.
* In the tests i've reached the textBlob quota for translate texts. The framework start to raise an HTTP error because the API returns the status 429 - 'Too many requests'. To solve this, i've searched by a framework with more usage limit and find the [Googletrans](https://py-googletrans.readthedocs.io/en/latest/), wich implements Google Translate API.