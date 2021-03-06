# Twitter sentiment analyzer

## Objective
This app aims to collect a stream of Portuguese tweets from Twitter API. The app analyzes the tweet text and classifies the sentiment of the text as **positive**, **negative** or **neutral**. The app stores the original tweet text and the resulting sentiment into a CSV file, which is plotted with live updates into an HTML dashboard.

## Requisites
To run this app you'll need Python 3 installed and the pip package manager to install the dependencies.

## How to use this app
First, clone the repo. After that, you can run locally or as a docker container. Below is the instructions to run these two ways.

### Running as a docker container
* First, build the image
```python
docker build -t twitter-analyzer .
```
* Then, run the container, mapping the port of the dashboard (8060) to your host.
```python
docker run -d -p 8060:8060 twitter-analyzer
```
* Access the real-time dashboard on 127.0.0.1:8060

### Running locally
Obs: The commands in the instructions aim at the Debian-based Linux distros. If you use other command to python or pip (like python3 or pip3), please replace in the follow commands.

1. First, change the default values on [credentials.py](./app/credentials.py) for your own twitter credentials
2. Install the dependencies with pip
```python
pip install -r requirements.txt
```
3. Execute the app
```python
python app.py
```
Obs: The app will start and should create the file "tweets_output.csv" to persist the information. Don't go to the next step before executing the app file, because of the dashboard loads data from this file.

4. With the app running, execute in another terminal the dashboard app
```python
python dashboard.py
```
5. Access the dashboard by the browser in the address 127.0.0.1:8060

## Running the unity tests
To run the unity tests for this project, just type the following command in the terminal:
```python
python unit_tests.py
```

## Running the accuracy report
To run the accuracy report for this project, just type the following command in the terminal:
```python
python accuracy_report.py
```

## The training set
Is not easy to find out a good Portuguese database to research. Version 1.0.0 of this program can create a training dataset because save a CSV with the text of the tweet and the sentiment generated by the textBlob framework. The result can be manually audited and the user can change the answers if judge incorrect. 

However, in my tests with an unfiltered stream by Twitter, the majority of collected tweets are classified as positive, so I don't have many examples of tweets classified as a negative or neutral sentiment.

I've done some research and find out a good training dataset in Portuguese, that also analyze tweets. This dataset has also a neutral sentiment, which I added to my model. The link for the source of this database is [here](https://www.kaggle.com/leandrodoze/tweets-from-mgbr).

### Training set data overview
* Total rows in training dataset: 8199
* Total tweets with sentiment "Positivo": 3262
* Total tweets with sentiment "Negativo": 2438
* Total tweets with sentiment "Neutro": 2423

## The model
The model used on this project was built using a Bag of Words approach and the Naive Bayes Multinomial classifier. In my research i found a neural map that can help to choose the right algoritm for the problem, in [this link](https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html). According to my problem, when i have to predict a category, with labeled data, and less than 100k samples with text data, Naive Bayes is the recommended choice.
The accuracy of the model using two words (ngram_range = (1, 2) parameter on CountVectorizer) increase the accuracy by 1,23% compared with analyzer = "word" only.

### Accuracy Report
The accuracy obtained in this model was 0.8954750579338944 or 89,55%. This evaluation was made divided the training set in 10 parts, 9 for train and 1 for test (cross-validation mode).

Details:

                precision   recall    f1-score  support

    Positivo       0.97      0.88      0.92       3300
    Negativo       0.91      0.93      0.92       2446
    Neutro         0.80      0.89      0.84       2453

    accuracy                            0.90      8199
    macro avg       0.89      0.90      0.89      8199
    weighted avg    0.90      0.90      0.90      8199
Where:
* precision = true positive / (true positive + false positive)
* recall    = true positive / (true positive + false negative)
* f1-score  = 2 * ((precision * recall) / (precision + recall))

#### Confusion matrix
    Predicted  Negativo  Neutro  Positivo   All
    Real                                       
    Negativo       2265     179         2  2446
    Neutro          181    2177        95  2453
    Positivo         43     357      2900  3300
    All            2489    2713      2997  8199

As we can see, real negatives classified as positives or neutral sum 181 (aprox. 7,7% of 2446 in total), real positives classified as negative or neutral is 400 (aprox. 12,12% of 3300 in total) and real neutral classified as positive or negative is 276 (aprox. 11,25% of 2453 in total), which means that our model seem to guess better negative sentiments than neutral or positive sentiment.

Obs: The commands to validate this numbers can be revalidated if you want. See the section "Running the accuracy report" in this document.

## The versions
This section contains a brief explanation contextualizing some changes between one version and another. If you want more objective details about the modifications, please check the [CHANGELOG file](./CHANGELOG.md)

### V 1.0.0
Version 1 of the project aimed to test the whole system. So, the structure of the project was created, the frameworks for manipulate the Twitter API and plot the results into a dashboard was tested in this version. 
For the sentiment analysis, I've used a popular package (Textblob) to obtain the sentiment analysis, but the objective is to replace this part with a personal classifier in the next version of the app.
To persist the result I've chosen a CSV, because of good compatibility with pandas data frames, used on the dashboard. This type of persistence brings some problems to scale the application, so needs to be replaced to provide more scalability to the app.

### V 1.1.0
Version 1.1.0 implements cleansing methods for the received tweets, the classifier, and a new sentiment was added. 
The cleansing functions aim to clear the mess on the tweets (put all text in the same line, remove emoticons, hashtags, links, Twitter usernames, etc.). This will pass a cleaner and lighter text to the classifier. These functions are covered by unity tests (build using TDD).
This version also implements a local classifier. For more information about the model see "The model" section in this document. This classifier replaces the textBlob sentiment analyzer and provides a new answer based on the training model. This answer can be one of the three sentiments: "Positivo" (positive), "Negativo" (negative), or "Neutro" (neutral). The training set also was uploaded and the unity_tests file has a test for the classifier.

### V 1.2.0
Version 1.2.0 reduces some of the payloads of load the training dataset every time that need to predict and creates a Docker version of the project.

## Develop decisions
During the development process, some decisions about the framework and the flow are made. The relevant ones are described below:
* I've searched for a good framework to do the dashboard. [Streamlit](https://www.streamlit.io/) and [Plotly](https://plotly.com/) seem two popular packages and well-maintained projects in Github, with free versions. I've tried first with Streamlit, but the "protobuf" dependency shows some problems on execution. I've researched the solution and apply some solutions but didn't work. To not lose much time on that matter I change to plotlty.
* In the tests I've reached the textBlob quota for translate texts. The framework starts to raise an HTTP error because the API returns the status 429 - 'Too many requests'. To solve this, I've searched for a framework with more usage limits and find the [Googletrans](https://py-googletrans.readthedocs.io/en/latest/), which implements Google Translate API.
* I've spent a lot of time trying to make the dashboard appear out of the container. The argument -p of mapping ports of docker was not sufficient. When I did a curl command inside the container I was able to see the dashboard page, but it was not transmitted to the physical host. The solution was to use other server to serve the application. I've fixed the problem using [gunicorn framework](https://gunicorn.org/).