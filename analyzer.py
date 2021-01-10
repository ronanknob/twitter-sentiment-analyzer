import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def classify_tweet(tweet):
    # Load training dataset
    dataset = pd.read_csv('tweets_training_set.csv',encoding='utf-8')
    tweets = dataset['Text'].values
    classes = dataset["Classificacao"].values

    # The training model will be made using a Bag of Words approach and the Naive Bayes Multinomial algoritm
    # Convert a collection of text documents to a matrix of token counts
    # Using two words (ngram_range = (1, 2)) increase the accuracy by 1,23% compared with analyzer = "word" parameter
    vectorizer = CountVectorizer(ngram_range = (1, 2))
    '''
    vectorizer.fit_transform will do the count of how much times the words appear in the text
    Example:
    (0, 1) 1
        -> 0 : row[the sentence index]
        -> 1 : get feature index(i.e. the word) from vectorizer.vocabulary_[1]
        -> 1 : count/tfidf (as you have used a count vectorizer, it will give you count)
    ''' 
    freq_tweets = vectorizer.fit_transform(tweets)
    # Create a Naive Bayes Multinomial algoritm
    model = MultinomialNB()
    # Train the model with the training data and the classes in the dataset
    model.fit(freq_tweets, classes)
    
    tweet_transformed = vectorizer.transform([tweet])
    predicted = model.predict(tweet_transformed)
    if not predicted:
        return None
    return predicted[0]