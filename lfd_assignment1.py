#!/usr/bin/env python

'''TODO: add high-level description of this Python script'''

import argparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC


# SPLIT 70/15/15
# BOW / TF-IDF
# BEST PERFORMING MODEL: FEATURE SET IMPROVEMENT


# TODO add parser arguments

def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--train_file", default='train.txt', type=str,
                        help="Train file to learn from (default train.txt)")
    parser.add_argument("-d", "--dev_file", default='dev.txt', type=str,
                        help="Dev file to evaluate on (default dev.txt)")
    parser.add_argument("-s", "--sentiment", action="store_true",
                        help="Do sentiment analysis (2-class problem)")
    parser.add_argument("-tf", "--tfidf", action="store_true",
                        help="Use the TF-IDF vectorizer instead of CountVectorizer")
    parser.add_argument("-a", "--algorithm", default="NB", type=str,
                        choices=["NB", "DT","RF", "KNN", "SVC", "LSVC"],
                        help="Algorithm to use (default MultinomialDB)")
    args = parser.parse_args()
    return args


def read_corpus(corpus_file, use_sentiment):
    '''TODO: add function description'''
    documents = []
    labels = []
    with open(corpus_file, encoding='utf-8') as in_file:
        for line in in_file:
            tokens = line.strip().split()
            documents.append(tokens[3:])
            if use_sentiment:
                # 2-class problem: positive vs negative
                labels.append(tokens[1])
            else:
                # 6-class problem: books, camera, dvd, health, music, software
                labels.append(tokens[0])
    return documents, labels


def identity(inp):
    '''Dummy function that just returns the input'''
    return inp


def measures(Y_test, Y_pred):
    '''TODO docstring'''
    
    # TODO: comment this
    acc = accuracy_score(Y_test, Y_pred)
    print(f"Final accuracy: {acc}")

    # PER CLASS
    rep = classification_report(Y_test, Y_pred)
    cm = confusion_matrix(Y_test, Y_pred)
    # mcm = multilabel_confusion_matrix(Y_test, Y_pred)

    print(f"Per class:\n{rep}")
    print(f"Confusion matrix:\n{cm}")


if __name__ == "__main__":
    args = create_arg_parser()

    # TODO: comment
    X_train, Y_train = read_corpus(args.train_file, args.sentiment)
    X_test, Y_test = read_corpus(args.dev_file, args.sentiment)

    # Convert the texts to vectors
    # We use a dummy function as tokenizer and preprocessor,
    # since the texts are already preprocessed and tokenized.
    if args.tfidf:
        vec = TfidfVectorizer(preprocessor=identity, tokenizer=identity)
    else:
        # Bag of Words vectorizer
        vec = CountVectorizer(preprocessor=identity, tokenizer=identity)

    # Choose a classifier
    if args.algorithm == "NB":
        cls = MultinomialNB()
    elif args.algorithm == "DT":
        cls = DecisionTreeClassifier()
    elif args.algorithm == "RF":
        cls = RandomForestClassifier()
    elif args.algorithm ==  "KNN":
        cls = KNeighborsClassifier()
    elif args.algorithm == "SVC":
        cls = SVC()
    elif args.algorithm == "LSVC":
        cls = LinearSVC()

    # Combine the vectorizer with the classifier
    classifier = Pipeline([('vec', vec), ('cls', cls)])

    # TODO: comment this
    classifier.fit(X_train, Y_train)

    # TODO: comment this
    Y_pred = classifier.predict(X_test)

    # TODO: comment this
    acc = accuracy_score(Y_test, Y_pred)
    print(f"Final accuracy: {acc}")

    # Print classification report and confusion matrix
    rep = classification_report(Y_test, Y_pred)
    cm = confusion_matrix(Y_test, Y_pred)
    # cm = multilabel_confusion_matrix(Y_test, Y_pred,)

    print(f"Per class:\n{rep}")
    print(f"Confusion matrix:\n{cm}")
