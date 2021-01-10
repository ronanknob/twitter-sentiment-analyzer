import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict


dataset = pd.read_csv('tweets_training_set.csv',encoding='utf-8')
tweets = dataset['Text'].values
classes = dataset["Classificacao"].values
vectorizer = CountVectorizer(ngram_range = (1, 2))
freq_tweets = vectorizer.fit_transform(tweets)
model = MultinomialNB()
model.fit(freq_tweets, classes)


#General accuracy by cross-validation
results = cross_val_predict(model, freq_tweets, classes, cv = 10)
print(f"General accuracy: {metrics.accuracy_score(classes, results)}")
print("----")

# Detailed accuracy report
sentiments = ['Positivo', 'Negativo', 'Neutro']
print("Detailed:")
print(metrics.classification_report(classes, results, sentiments))
print("----")

# Confusion matrix
print("Confusion Matrix")
print(pd.crosstab(classes, results, rownames = ["Real"], colnames = ["Predicted"], margins = True))