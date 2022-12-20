import json
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
    lemmatizer = WordNetLemmatizer()
    data = []       # contains dataset json data
    words = []      # contains list of preprocessed words
    classes = []    # contains all non duplicate tag
    doc_x = []      # contains all pattern corresponding to doc_y tag
    doc_y = []      # contains all tag corresponding to doc_x pattern
    model = None
    context = None

    def __load_dataset(self, path):
        with open(path) as file:
            self.data = json.load(file)

    def __preprocessing(self):
        # Tokenization
        for intent in self.data["intents"]:
            tag = intent["tag"]
            for pattern in intent["patterns"]:
                pattern_token = nltk.word_tokenize(pattern)
                self.words.extend(pattern_token)
                self.doc_x.append(pattern_token)
                self.doc_y.append(tag)
            if tag not in self.classes:
                self.classes.append(tag)

        # Lemmatization and remove punctuation
        self.words = [
            self.lemmatizer.lemmatize(word.lower())
            for word in self.words if word not in string.punctuation
        ]

        # Sorting vocab alphabetical order & remove duplicate
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(self.classes)

    def __create_train_data(self):
        training = []
        out_empty = [0] * len(self.classes)

        for index, pattern_tokens in enumerate(self.doc_x):
            bag = []
            text = [self.lemmatizer.lemmatize(word.lower()) for word in pattern_tokens]

            for word in self.words:
                bag.append(1) if word in text else bag.append(0)

            output_row = list(out_empty)
            output_row[self.classes.index(self.doc_y[index])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training, dtype=object)

        train_x = np.array(list(training[:, 0]))
        train_y = np.array(list(training[:, 1]))

        return train_x, train_y

    def __train(self, train_x, train_y):
        input_shape = (len(train_x[0]),)
        output_shape = len(train_y[0])
        epochs = 200

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
            trained_model = load_model("./model")
        except:
            model.fit(x=train_x, y=train_y, epochs=epochs, verbose=1)
            model.save("./model")
            trained_model = model

        return trained_model

    def __clean_text(self, text):
        tokens = nltk.word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word.lower()) for word in tokens]
        return tokens

    def __bag_of_words(self, text):
        tokens = self.__clean_text(text)
        bag = [0] * len(self.words)
        for w in tokens:
            for idx, word in enumerate(self.words):
                if word == w:
                    bag[idx] = 1
        return np.array(bag)

    def __choose_response(self, intents_list):
        tag = intents_list[0]
        list_of_intents = self.data["intents"]
        for intent in list_of_intents:
            if intent["tag"] == tag:
                if "context_set" in intent:
                    self.context = intent["context_set"]
                return random.choice(intent["responses"])
        return None

    def get_bot_response(self, message):
        bow = self.__bag_of_words(message)
        result = self.model.predict(np.array([bow]))[0]

        result_index = [[idx, res] for idx, res in enumerate(result) if res > self.threshold]
        result_index.sort(key=lambda x: x[1], reverse=True)

        return_list = []
        for r in result_index:
            return_list.append(self.classes[r[0]])

        if len(return_list) == 0:
            response = None
        else:
            response = self.__choose_response(return_list)

        return response.format(name=self.name) if response is not None else "Sorry, I don't understand you."

    def get_current_context(self):
        return self.context

    def __init__(self, name, dataset="./dataset/intents.json", threshold = 0.9):
        self.name = name
        self.threshold = threshold

        self.__load_dataset(dataset)
        self.__preprocessing()

        x, y = self.__create_train_data()
        self.model = self.__train(x, y)
