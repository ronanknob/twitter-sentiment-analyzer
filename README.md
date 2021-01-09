# Twitter sentiment analyzer

## Objective
This app aims to collect a stream of Portuguese tweets from Twitter API. The app analyzes the tweet text and classifies the sentiment of the text as **positive** or **negative**. The app stores the original tweet text and the resulting sentiment into a CSV file, which is plotted with live updates into an HTML dashboard.

## Requisites
To run this app you'll need Python 3 installed and the pip package manager.

## How to use this app
Obs: The commands in the instructions aim at the Debian-based Linux distros. If you use the pip3 command, replace pip with pip3 in the following commands.

1. Install the dependencies -> pip install -r requirements.txt
2. Configure the access credentials for the Twitter API in the credentials.py file.
3. Execute the app file -> run the command "python3 app.py" on a terminal. The app will start and should create the file "tweets_output.csv" to persist the information. Don't go to the next step before executing the app file, because of the dashboard loads data from this file.
4. With the app running, execute in another terminal the dashboard app -> python3 dashboard.py. The console should return the URL for the dashboard (ex: http://127.0.0.1:8050/). Open this URL in a browser (tested on latest versions of Firefox and Chrome), and you will see the real-time data being processed, with 3 seconds interval on data refreshing.
5. If you need to interrupt the executions, do a break on the terminals (usually ctrl+c)

### Unity tests
Was added some text cleansing functions to this app. These functions aim to clear the mess on the tweets (put all text in the same line, remove emoticons, hashtags, links, twitter usernames, etc.). This will pass a cleaner and lighter text to the model interpreter. These functions are covered by unity tests (build using TDD). So, if you want to run these tests, just type the following command in the terminal:
```python
python3 unit_tests.py
```

## The versions
This section contains a brief explanation contextualizing some changes between one version and another. If you want more objective details about the modifications, please check the [CHANGELOG file](./CHANGELOG.md)

### V 1.0.0
Version 1 of the project aimed to test the whole system. So, the structure of the project was created, the frameworks for manipulate the Twitter API and plot the results into a dashboard was tested in this version. 
For the sentiment analysis, I've used a popular package (Textblob) to obtain the sentiment analysis, but the objective is to replace this part with a personal classifier in the next version of the app.
To persist the result I've chosen a CSV, because of good compatibility with pandas data frames, used on the dashboard. This type of persistence brings some problems to scale the application, so needs to be replaced to provide more scalability to the app.

## Develop decisions
During the development process, some decisions about the framework and the flow are made. The relevant ones are described below:
* I've searched for a good framework to do the dashboard. [Streamlit](https://www.streamlit.io/) and [Plotly](https://plotly.com/) seem two popular packages and well-maintained projects in Github, with free versions. I've tried first with Streamlit, but the "protobuf" dependency shows some problems on execution. I've researched the solution and apply some solutions but didn't work. To not lose much time on that matter I change to plotlty.
* In the tests I've reached the textBlob quota for translate texts. The framework starts to raise an HTTP error because the API returns the status 429 - 'Too many requests'. To solve this, I've searched for a framework with more usage limits and find the [Googletrans](https://py-googletrans.readthedocs.io/en/latest/), which implements Google Translate API.