import sys
import pandas as pd
import datetime
import snscrape.modules.twitter as sntwitter
from facebook_scraper import get_posts
import itertools
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, \
    QVBoxLayout, QLabel, QLineEdit, QCheckBox, QTableWidget, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from collections import Counter

class Windows(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.statusBar().setStyleSheet("color : red")
        self.title = QLabel("Data mining")
        self.data_posts = None
        self.data_users = None
        self.data_analyse = None

        # keyword
        self.LE_keyWord = QLineEdit()
        self.LE_keyWord.setPlaceholderText("Enter keyword")

        # lang (twitter only)
        self.CO_twitter_lang = QComboBox(self)
        self.CO_twitter_lang.addItems(["en", "fr"])
        self.CO_twitter_lang.hide()

        # starting date
        self.LE_starting_date = QLineEdit()
        self.LE_starting_date.setPlaceholderText("Starting date : YYYY-MM-DD")
        onlyDate = QRegExpValidator(QRegExp("[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}"))
        self.LE_starting_date.setValidator(onlyDate)

        # ending date
        self.LE_ending_date = QLineEdit()
        self.LE_ending_date.setPlaceholderText("Ending date : YYYY-MM-DD")
        self.LE_ending_date.setValidator(onlyDate)

        # number of tweets/pages
        self.LE_tweet_post_number = QLineEdit()
        self.LE_tweet_post_number.setPlaceholderText("Number of tweets/posts")
        onlyInt = QIntValidator()
        onlyInt.setRange(1, 999)
        self.LE_tweet_post_number.setValidator(onlyInt)

        # twitter checkbox
        self.CB_twitter = QCheckBox("Twitter")
        self.CB_twitter.stateChanged.connect(self.func_CB_twitter)

        # facebook checkbox
        self.CB_facebook = QCheckBox("Facebook")
        self.CB_facebook.stateChanged.connect(self.func_CB_facebook)

        # facebook page name
        self.LE_facebook_page_name = QLineEdit()
        self.LE_facebook_page_name.setPlaceholderText("Enter Facebook Page")
        self.LE_facebook_page_name.hide()

        # table for showing the five first tweets/posts
        self.LA_text_result = QLabel("First 5 tweets/posts")
        self.LA_text_result.hide()
        self.T_text_result = QTableWidget()
        self.T_text_result.setRowCount(5)
        self.T_text_result.setColumnCount(7)
        header = self.T_text_result.horizontalHeader()
        header.setStretchLastSection(True)
        self.T_text_result.hide()

        # table for showing some info about those 5 tweets/posts (words count, letters count, link)
        self.LA_text_info = QLabel("Info about the first 5 tweets/posts")
        self.LA_text_info.hide()
        self.T_text_info = QTableWidget()
        self.T_text_info.setRowCount(5)
        self.T_text_info.setColumnCount(3)
        header = self.T_text_info.horizontalHeader()
        header.setStretchLastSection(True)
        self.T_text_info.setHorizontalHeaderLabels(['words count', 'letters count', 'link'])
        self.T_text_info.hide()

        # table for showing the five most common words on all the tweets/posts
        self.LA_text_common = QLabel("5 most common words")
        self.LA_text_common.hide()
        self.T_text_common = QTableWidget()
        self.T_text_common.setRowCount(2)
        self.T_text_common.setColumnCount(5)
        header = self.T_text_common.horizontalHeader()
        header.setStretchLastSection(True)
        self.T_text_common.setHorizontalHeaderLabels(['first', 'second', 'third', 'fourth', 'fifth'])
        self.T_text_common.hide()

        # table for showing the five users of those five tweets/posts (twitter only)
        self.LA_user_result = QLabel("First 5 users")
        self.LA_user_result.hide()
        self.T_user_result = QTableWidget()
        self.T_user_result.setRowCount(5)
        self.T_user_result.setColumnCount(7)
        header = self.T_user_result.horizontalHeader()
        header.setStretchLastSection(True)
        self.T_user_result.setHorizontalHeaderLabels(
            ['id', 'username', 'displayname', 'description', 'verified', 'followersCount', 'created'])
        self.T_user_result.hide()

        # button for validation
        self.BU_validate = QPushButton("Confirm")
        self.BU_validate.clicked.connect(self.func_BU_validate)

        # button for tables' exportation (all tweets/posts, all info and all users if it's twitter) on json format
        self.BU_json = QPushButton("Export")
        self.BU_json.clicked.connect(self.func_BU_json)
        self.BU_json.hide()

        # line edit for the output file's name
        self.LE_json = QLineEdit()
        self.LE_json.setPlaceholderText("Enter name file")
        onlyChar = QRegExpValidator(QRegExp("[a-z-A-Z-0-9_]+"))
        self.LE_json.setValidator(onlyChar)
        self.LE_json.hide()

        # layout
        self.widgets = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.LE_keyWord)
        layout.addWidget(self.LE_starting_date)
        layout.addWidget(self.LE_ending_date)
        layout.addWidget(self.LE_tweet_post_number)
        layout.addWidget(self.CB_twitter)
        layout.addWidget(self.CO_twitter_lang)
        layout.addWidget(self.CB_facebook)
        layout.addWidget(self.LE_facebook_page_name)
        layout.addWidget(self.LA_text_result)
        layout.addWidget(self.T_text_result)
        layout.addWidget(self.LA_text_info)
        layout.addWidget(self.T_text_info)
        layout.addWidget(self.LA_text_common)
        layout.addWidget(self.T_text_common)
        layout.addWidget(self.LA_user_result)
        layout.addWidget(self.T_user_result)
        layout.addWidget(self.BU_validate)
        layout.addWidget(self.LE_json)
        layout.addWidget(self.BU_json)
        self.widgets.setLayout(layout)
        self.setCentralWidget(self.widgets)

        self.setWindowTitle("Scraper")
        self.resize(200, 250)

    def func_CB_twitter(self):
        # show/hide widgets
        if self.CB_twitter.checkState():
            self.CB_facebook.setChecked(False)
            self.CO_twitter_lang.show()
            self.T_text_result.setHorizontalHeaderLabels(
                ['id', 'date', 'replyCount', 'retweetCount', 'likeCount', 'lang', 'content'])
        else:
            self.CO_twitter_lang.hide()
        self.hideUselessWidgets()

    def func_CB_facebook(self):
        # show/hide widgets
        if self.CB_facebook.checkState():
            self.CB_twitter.setChecked(False)
            self.LE_facebook_page_name.show()
            self.T_text_result.setHorizontalHeaderLabels(
                ['post_id', 'time', 'comments', 'shares', 'likes', 'text', 'username'])
        else:
            self.LE_facebook_page_name.hide()
        self.hideUselessWidgets()

    def hideUselessWidgets(self):
        self.statusBar().clearMessage()
        self.T_user_result.hide()
        self.LA_user_result.hide()
        self.LA_text_result.hide()
        self.T_text_result.hide()
        self.LA_text_info.hide()
        self.T_text_info.hide()
        self.LE_json.hide()
        self.BU_json.hide()
        self.T_text_common.hide()
        self.LA_text_common.hide()
        self.resize(200, 250)
        self.move(859, 364)

    def func_BU_json(self):
        # export the dataframes on json format
        if self.CB_twitter.checkState():
            data_users_parsed = json.loads(self.data_users.to_json(orient="split"))
        data_posts_parsed = json.loads(self.data_posts.to_json(orient="split"))
        data_analyse_parsed = json.loads(self.data_analyse.to_json(orient="split"))

        if not self.LE_json.text():
            self.statusBar().showMessage("ERROR: Please enter a file name")
        else:
            self.statusBar().showMessage("SUCCESS: Files saved")
            if self.CB_twitter.checkState():
                with open(".\\export\\{}_users.json".format(self.LE_json.text()), 'w') as outfile:
                    json.dump(data_users_parsed, outfile)
            with open(".\\export\\{}_posts.json".format(self.LE_json.text()), 'w') as outfile:
                json.dump(data_posts_parsed, outfile)
            with open(".\\export\\{}_analyse.json".format(self.LE_json.text()), 'w') as outfile:
                json.dump(data_analyse_parsed, outfile)

    def func_BU_validate(self):
        # recover data and put it in dataframe

        self.hideUselessWidgets()

        if not self.LE_keyWord.text():
            self.statusBar().showMessage("ERROR: Please enter a keyword")
        elif self.CB_facebook.checkState() and not self.LE_facebook_page_name.text():
            self.statusBar().showMessage("ERROR: Please specify a page name")
        elif not self.LE_tweet_post_number.text():
            self.statusBar().showMessage("ERROR: Please specify a number of tweets")
        elif not self.LE_starting_date.text() or not self.LE_ending_date.text():
            self.statusBar().showMessage("ERROR: Please specify dates")
        elif not self.CB_facebook.checkState() and not self.CB_twitter.checkState():
            self.statusBar().showMessage("ERROR: Please select one social network")
        else:
            self.statusBar().clearMessage()

            if self.CB_twitter.checkState():
                # the scraped tweets, this is a generator
                scraped_tweets = sntwitter.TwitterSearchScraper(
                    '{} since:{} until:{} lang:{}'.format(self.LE_keyWord.text(),
                                                          self.LE_starting_date.text(),
                                                          self.LE_ending_date.text(),
                                                          self.CO_twitter_lang.currentText())).get_items()
                # slicing the generator to keep only the numbers of tweets needed
                sliced_scraped_tweets = itertools.islice(scraped_tweets, int(self.LE_tweet_post_number.text()))
                # convert to a DataFrame and keep only relevant columns
                self.data_posts = pd.DataFrame(sliced_scraped_tweets)[
                    ['id', 'date', 'replyCount', 'retweetCount', 'likeCount', 'lang', 'content', 'user', 'url']]

                # recover data from users
                data_users_old = []
                for i in range(len(self.data_posts)):
                    data_users_old.append(self.data_posts['user'][i])
                self.data_users = [None] * len(data_users_old)
                user_keys = ['id', 'username', 'displayname', 'description', 'verified', 'followersCount',
                             'created']
                for i in range(len(data_users_old)):
                    self.data_users[i] = {user_key: data_users_old[i][user_key] for user_key in user_keys}
                self.data_users = pd.DataFrame(self.data_users)

                id_text = 'content'
                id_url = 'url'
            else:
                data_posts_old = []
                for post in get_posts(self.LE_facebook_page_name.text(), pages=100):
                    # loading bar because it's very slow
                    print("{}/{}".format(len(data_posts_old), self.LE_tweet_post_number.text()))
                    # date verification
                    year, month, day = self.LE_starting_date.text().split('-')
                    if post['time'].replace(tzinfo=None) < datetime.datetime(int(year), int(month), int(day)):
                        continue
                    year, month, day = self.LE_ending_date.text().split('-')
                    if post['time'].replace(tzinfo=None) > datetime.datetime(int(year), int(month), int(day)):
                        continue
                    # keyword verification
                    if not post['text'] or self.LE_keyWord.text().lower() not in post['text'].lower():
                        continue
                    data_posts_old.append(post)
                    # we leave when we have enough posts
                    if len(data_posts_old) == int(self.LE_tweet_post_number.text()):
                        break
                # tranformation in dataframe with only the columns needed
                self.data_posts = [None] * len(data_posts_old)
                post_keys = ['post_id', 'time', 'comments', 'shares', 'likes', 'text', 'username', 'user_id',
                             'post_url']
                for i in range(len(data_posts_old)):
                    self.data_posts[i] = {post_key: data_posts_old[i][post_key] for post_key in post_keys}
                self.data_posts = pd.DataFrame(self.data_posts)

                id_text = 'text'
                id_url = 'post_url'

            # compute some info
            self.data_analyse = [None] * len(self.data_posts)
            for i in self.data_posts.index:
                strings = self.data_posts[id_text][i].split()
                self.data_analyse[i] = {"word_count": len(strings)}
                self.data_analyse[i]['length'] = len(self.data_posts[id_text][i])
                self.data_analyse[i]['source'] = self.data_posts[id_url][i]
            self.data_analyse = pd.DataFrame(self.data_analyse)

            self.show_data_sample()
            self.BU_json.show()
            self.LE_json.show()
            self.resize(1200, 1000)
            self.move(350, 0)

    def show_data_sample(self):
        # fill in the tables

        # show 5 posts/tweets
        for i in range(5):
            for j in range(len(self.data_posts.columns) - 2):
                self.T_text_result.setItem(i, j, QTableWidgetItem("{}".format(self.data_posts.iloc[i, j])))

        # show info about those 5 tweets/posts
        for i in range(5):
            for j in range(len(self.data_analyse.columns)):
                self.T_text_info.setItem(i, j, QTableWidgetItem("{}".format(self.data_analyse.iloc[i, j])))

        # Compute the most common words
        if self.CB_twitter.checkState():
            common_words = Counter(" ".join(self.data_posts["content"]).split()).most_common(5)
        else:
            common_words = Counter(" ".join(self.data_posts["text"]).split()).most_common(5)
        i = 0
        for x, y in common_words:
            self.T_text_common.setItem(0, i, QTableWidgetItem("{}".format(x)))
            self.T_text_common.setItem(1, i, QTableWidgetItem("{}".format(y)))
            i += 1

        # Show 5 users if it's twitter
        if self.CB_twitter.checkState():
            for i in range(5):
                for j in range(len(self.data_users.columns)):
                    self.T_user_result.setItem(i, j, QTableWidgetItem("{}".format(self.data_users.iloc[i, j])))
            self.T_user_result.show()
            self.LA_user_result.show()
        self.LA_text_result.show()
        self.T_text_result.show()
        self.LA_text_info.show()
        self.T_text_info.show()
        self.LA_text_common.show()
        self.T_text_common.show()

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

Window = Windows()
Window.show()

app.exec_()