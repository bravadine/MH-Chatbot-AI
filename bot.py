import json
import os
import random
import nltk
import string
import numpy as np
from nltk.stem import WordNetLemmatizer
from keras import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.models import load_model

nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")

class Bot:
    __lemmatizer = WordNetLemmatizer()
    __data = []  # contains dataset json data
    __words = []  # contains list of preprocessed words
    __classes = []  # contains all non duplicate tag
    __doc_x = []  # contains all pattern corresponding to doc_y tag
    __doc_y = []  # contains all tag corresponding to doc_x pattern

    __chat_context = None

    def greet(self):
        return "Hello, My name is {name}".format(name=self.bot_name)

    def __load_dataset(self, path):
        with open(path, "r") as file:
            self.__data.append(json.load(file))

    def __preprocess_dataset(self):
        # Tokenization
        for dataset in self.__data:
            for intent in dataset["intents"]:
                tag = intent["tag"]
                for pattern in intent["patterns"]:
                    pattern_token = nltk.word_tokenize(pattern)
                    self.__words.extend(pattern_token)
                    self.__doc_x.append(pattern_token)
                    self.__doc_y.append(tag)
                if tag not in self.__classes:
                    self.__classes.append(tag)

        # Lemmatization and remove punctuation
        self.__words = [
            self.__lemmatizer.lemmatize(word.lower())
            for word in self.__words if word not in string.punctuation
        ]

        # Sorting vocab alphabetical order & remove duplicate
        self.__words = sorted(list(set(self.__words)))
        self.__classes = sorted(self.__classes)

    def __create_train_data(self):
        training = []
        out_empty = [0] * len(self.__classes)

        for index, pattern_tokens in enumerate(self.__doc_x):
            bag = []
            text = [self.__lemmatizer.lemmatize(word.lower()) for word in pattern_tokens]

            for word in self.__words:
                bag.append(1) if word in text else bag.append(0)

            output_row = list(out_empty)
            output_row[self.__classes.index(self.__doc_y[index])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training, dtype=object)

        train_x = np.array(list(training[:, 0]))
        train_y = np.array(list(training[:, 1]))

        return train_x, train_y

    @staticmethod
    def __train(train_x, train_y, model_path="./model"):
        input_shape = (len(train_x[0]),)
        output_shape = len(train_y[0])
        epochs = 500

        # Deep learning model
        model = Sequential()
        model.add(Dense(128, input_shape=input_shape, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(output_shape, activation="softmax"))
        adam = Adam(learning_rate=0.01, decay=1e-6)

        model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=["accuracy"])
        print(model.summary())

        # Train data
        try:
            trained_model = load_model(model_path)
        except:
            model.fit(x=train_x, y=train_y, epochs=epochs, verbose=1)
            model.save(model_path)
            trained_model = model

        return trained_model

    def __clean_text(self, text):
        tokens = nltk.word_tokenize(text)
        tokens = [self.__lemmatizer.lemmatize(word.lower()) for word in tokens]
        return tokens

    def __bag_of_words(self, text):
        tokens = self.__clean_text(text)
        bag = [0] * len(self.__words)
        for w in tokens:
            for idx, word in enumerate(self.__words):
                if word == w:
                    bag[idx] = 1
        return np.array(bag)

    def __choose_response(self, intents_list):
        tag = intents_list[0]
        intents_dataset = [dataset["intents"] for dataset in self.__data]
        for list_of_intents in intents_dataset:
            for intent in list_of_intents:
                if intent["tag"] == tag:
                    if "context_set" in intent:
                        self.__chat_context = intent["context_set"]
                    return random.choice(intent["responses"])
        return None

    def chat_respond(self, message):
        bow = self.__bag_of_words(message)
        result = self.__model.predict(np.array([bow]))[0]

        result_index = [[idx, res] for idx, res in enumerate(result) if res >= self.__threshold]
        result_index.sort(key=lambda x: x[1], reverse=True)

        return_list = []
        for r in result_index:
            return_list.append(self.__classes[r[0]])

        if len(return_list) == 0:
            response = None
        else:
            response = self.__choose_response(return_list)

        return response.format(bot_name=self.bot_name) if response is not None \
            else f"Sorry, {self.bot_name} doesn't understand you."

    def chat_context(self):
        return self.__chat_context

    def __init__(self, bot_name, dataset_path="./datasets/", threshold=0.7):
        self.bot_name = bot_name
        self.__threshold = threshold

        for dataset in [file for file in os.listdir(dataset_path) if file.endswith(".json")]:
            self.__load_dataset(dataset_path + dataset)
        self.__preprocess_dataset()

        x, y = self.__create_train_data()
        self.__model = self.__train(x, y)
