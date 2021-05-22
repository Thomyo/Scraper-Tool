import sys
import numpy as np
import pandas as pd
import datetime
import snscrape.modules.twitter as sntwitter
from facebook_scraper import get_posts
import itertools
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, \
    QLabel, QLineEdit, QCheckBox, QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout, QFrame, QFormLayout
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
from collections import Counter


class Windows(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Scraper")
        self.statusBar().setStyleSheet("color : red")
        self.title = QLabel("Data mining")
        self.title.setStyleSheet("text-decoration: underline")
        self.data_posts = None
        self.data_users = None
        self.data_analyse = None
        self.list_param_users = []
        self.list_param_posts = []

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
        self.CB_twitter.setStyleSheet("text-decoration: underline")
        self.CB_twitter.stateChanged.connect(self.func_CB_twitter)

        # selection of paramters
        self.list_check_box = []
        # twitter tweet parameters
        self.LA_tweet_twitter = QLabel("Parameters Tweet Info :")
        self.LA_tweet_twitter.hide()
        layout_CB_tweet_twitter = QHBoxLayout()
        self.CB_tweet_twitter_url = QCheckBox("url")
        self.list_check_box.append(self.CB_tweet_twitter_url)
        self.CB_tweet_twitter_url.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_url, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_url)
        self.CB_tweet_twitter_date = QCheckBox("date")
        self.list_check_box.append(self.CB_tweet_twitter_date)
        self.CB_tweet_twitter_date.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_date, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_date)
        self.CB_tweet_twitter_content = QCheckBox("content")
        self.list_check_box.append(self.CB_tweet_twitter_content)
        self.CB_tweet_twitter_content.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_content, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_content)
        self.CB_tweet_twitter_renderedContent = QCheckBox("renderedContent")
        self.list_check_box.append(self.CB_tweet_twitter_renderedContent)
        self.CB_tweet_twitter_renderedContent.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_renderedContent, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_renderedContent)
        self.CB_tweet_twitter_id = QCheckBox("id")
        self.list_check_box.append(self.CB_tweet_twitter_id)
        self.CB_tweet_twitter_id.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_id, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_id)
        self.CB_tweet_twitter_user = QCheckBox("user")
        self.list_check_box.append(self.CB_tweet_twitter_user)
        self.CB_tweet_twitter_user.stateChanged.connect(
            lambda: self.parameters_twitter_user(self.CB_tweet_twitter_user, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_user)
        self.CB_tweet_twitter_outlinks = QCheckBox("outlinks")
        self.list_check_box.append(self.CB_tweet_twitter_outlinks)
        self.CB_tweet_twitter_outlinks.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_outlinks, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_outlinks)
        self.CB_tweet_twitter_tcooutlinks = QCheckBox("tcooutlinks")
        self.list_check_box.append(self.CB_tweet_twitter_tcooutlinks)
        self.CB_tweet_twitter_tcooutlinks.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_tcooutlinks, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_tcooutlinks)
        self.CB_tweet_twitter_replyCount = QCheckBox("replyCount")
        self.list_check_box.append(self.CB_tweet_twitter_replyCount)
        self.CB_tweet_twitter_replyCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_replyCount, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_replyCount)
        self.CB_tweet_twitter_retweetCount = QCheckBox("retweetCount")
        self.list_check_box.append(self.CB_tweet_twitter_retweetCount)
        self.CB_tweet_twitter_retweetCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_retweetCount, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_retweetCount)
        self.CB_tweet_twitter_likeCount = QCheckBox("likeCount")
        self.list_check_box.append(self.CB_tweet_twitter_likeCount)
        self.CB_tweet_twitter_likeCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_likeCount, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_likeCount)
        self.CB_tweet_twitter_quoteCount = QCheckBox("quoteCount")
        self.list_check_box.append(self.CB_tweet_twitter_quoteCount)
        self.CB_tweet_twitter_quoteCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_quoteCount, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_quoteCount)
        self.CB_tweet_twitter_conversationId = QCheckBox("conversationId")
        self.list_check_box.append(self.CB_tweet_twitter_conversationId)
        self.CB_tweet_twitter_conversationId.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_conversationId, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_conversationId)
        self.CB_tweet_twitter_lang = QCheckBox("lang")
        self.list_check_box.append(self.CB_tweet_twitter_lang)
        self.CB_tweet_twitter_lang.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_lang, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_lang)
        self.CB_tweet_twitter_source = QCheckBox("source")
        self.list_check_box.append(self.CB_tweet_twitter_source)
        self.CB_tweet_twitter_source.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_source, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_source)
        self.CB_tweet_twitter_sourceUrl = QCheckBox("sourceUrl")
        self.list_check_box.append(self.CB_tweet_twitter_sourceUrl)
        self.CB_tweet_twitter_sourceUrl.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_sourceUrl, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_sourceUrl)
        self.CB_tweet_twitter_sourceLabel = QCheckBox("sourceLabel")
        self.list_check_box.append(self.CB_tweet_twitter_sourceLabel)
        self.CB_tweet_twitter_sourceLabel.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_sourceLabel, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_sourceLabel)
        self.CB_tweet_twitter_media = QCheckBox("media")
        self.list_check_box.append(self.CB_tweet_twitter_media)
        self.CB_tweet_twitter_media.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_media, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_media)
        self.CB_tweet_twitter_retweetedTweet = QCheckBox("retweetedTweet")
        self.list_check_box.append(self.CB_tweet_twitter_retweetedTweet)
        self.CB_tweet_twitter_retweetedTweet.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_retweetedTweet, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_retweetedTweet)
        self.CB_tweet_twitter_quotedTweet = QCheckBox("quotedTweet")
        self.list_check_box.append(self.CB_tweet_twitter_quotedTweet)
        self.CB_tweet_twitter_quotedTweet.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_quotedTweet, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_quotedTweet)
        self.CB_tweet_twitter_mentionedUsers = QCheckBox("mentionedUsers")
        self.list_check_box.append(self.CB_tweet_twitter_mentionedUsers)
        self.CB_tweet_twitter_mentionedUsers.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_mentionedUsers, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_mentionedUsers)
        self.CB_tweet_twitter_coordinates = QCheckBox("coordinates")
        self.list_check_box.append(self.CB_tweet_twitter_coordinates)
        self.CB_tweet_twitter_coordinates.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_coordinates, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_coordinates)
        self.CB_tweet_twitter_place = QCheckBox("place")
        self.list_check_box.append(self.CB_tweet_twitter_place)
        self.CB_tweet_twitter_place.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_tweet_twitter_place, self.list_param_posts))
        layout_CB_tweet_twitter.addWidget(self.CB_tweet_twitter_place)
        self.FR_tweet_twitter = QFrame()
        self.FR_tweet_twitter.setLayout(layout_CB_tweet_twitter)
        self.FR_tweet_twitter.hide()
        # twitter user parameters
        self.LA_user_twitter = QLabel("Parameters Users Info (user needed) :")
        self.LA_user_twitter.hide()
        self.list_check_box_user_twitter = []
        layout_CB_user_twitter = QHBoxLayout()
        self.CB_user_twitter_username = QCheckBox("username")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_username)
        self.CB_user_twitter_username.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_username, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_username)
        self.CB_user_twitter_displayname = QCheckBox("displayname")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_displayname)
        self.CB_user_twitter_displayname.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_displayname, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_displayname)
        self.CB_user_twitter_id = QCheckBox("id")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_id)
        self.CB_user_twitter_id.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_id, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_id)
        self.CB_user_twitter_description = QCheckBox("description")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_description)
        self.CB_user_twitter_description.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_description, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_description)
        self.CB_user_twitter_rawDescription = QCheckBox("rawDescription")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_rawDescription)
        self.CB_user_twitter_rawDescription.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_rawDescription, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_rawDescription)
        self.CB_user_twitter_descriptionUrls = QCheckBox("descriptionUrls")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_descriptionUrls)
        self.CB_user_twitter_descriptionUrls.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_descriptionUrls, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_descriptionUrls)
        self.CB_user_twitter_verified = QCheckBox("verified")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_verified)
        self.CB_user_twitter_verified.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_verified, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_verified)
        self.CB_user_twitter_created = QCheckBox("created")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_created)
        self.CB_user_twitter_created.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_created, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_created)
        self.CB_user_twitter_followersCount = QCheckBox("followersCount")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_followersCount)
        self.CB_user_twitter_followersCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_followersCount, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_followersCount)
        self.CB_user_twitter_friendsCount = QCheckBox("friendsCount")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_friendsCount)
        self.CB_user_twitter_friendsCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_friendsCount, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_friendsCount)
        self.CB_user_twitter_statusesCount = QCheckBox("statusesCount")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_statusesCount)
        self.CB_user_twitter_statusesCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_statusesCount, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_statusesCount)
        self.CB_user_twitter_favouritesCount = QCheckBox("favouritesCount")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_favouritesCount)
        self.CB_user_twitter_favouritesCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_favouritesCount, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_favouritesCount)
        self.CB_user_twitter_listedCount = QCheckBox("listedCount")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_listedCount)
        self.CB_user_twitter_listedCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_listedCount, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_listedCount)
        self.CB_user_twitter_mediaCount = QCheckBox("mediaCount")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_mediaCount)
        self.CB_user_twitter_mediaCount.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_mediaCount, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_mediaCount)
        self.CB_user_twitter_location = QCheckBox("location")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_location)
        self.CB_user_twitter_location.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_location, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_location)
        self.CB_user_twitter_protected = QCheckBox("protected")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_protected)
        self.CB_user_twitter_protected.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_protected, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_protected)
        self.CB_user_twitter_linkUrl = QCheckBox("linkUrl")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_linkUrl)
        self.CB_user_twitter_linkUrl.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_linkUrl, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_linkUrl)
        self.CB_user_twitter_linkTcourl = QCheckBox("linkTcourl")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_linkTcourl)
        self.CB_user_twitter_linkTcourl.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_linkTcourl, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_linkTcourl)
        self.CB_user_twitter_profileImageUrl = QCheckBox("profileImageUrl")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_profileImageUrl)
        self.CB_user_twitter_profileImageUrl.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_profileImageUrl, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_profileImageUrl)
        self.CB_user_twitter_profileBannerUrl = QCheckBox("profileBannerUrl")
        self.list_check_box_user_twitter.append(self.CB_user_twitter_profileBannerUrl)
        self.CB_user_twitter_profileBannerUrl.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_user_twitter_profileBannerUrl, self.list_param_users))
        layout_CB_user_twitter.addWidget(self.CB_user_twitter_profileBannerUrl)
        self.FR_user_twitter = QFrame()
        self.FR_user_twitter.setLayout(layout_CB_user_twitter)
        self.FR_user_twitter.hide()

        # facebook checkbox
        self.CB_facebook = QCheckBox("Facebook")
        self.CB_facebook.setStyleSheet("text-decoration: underline")
        self.CB_facebook.stateChanged.connect(self.func_CB_facebook)

        # facebook page name
        self.LE_facebook_page_name = QLineEdit()
        self.LE_facebook_page_name.setPlaceholderText("Enter Facebook Page (example : nintendo")
        self.LE_facebook_page_name.hide()

        # facebook post parameters
        self.LA_post_facebook = QLabel("Parameters Posts Info :")
        self.LA_post_facebook.hide()
        layout_CB_post_facebook_up = QHBoxLayout()
        layout_CB_post_facebook_bottom = QHBoxLayout()
        self.CB_post_facebook_available = QCheckBox("available")
        self.list_check_box.append(self.CB_post_facebook_available)
        self.CB_post_facebook_available.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_available, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_available)
        self.CB_post_facebook_comments = QCheckBox("comments")
        self.list_check_box.append(self.CB_post_facebook_comments)
        self.CB_post_facebook_comments.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_comments, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_comments)
        self.CB_post_facebook_comments_full = QCheckBox("comments_full")
        self.list_check_box.append(self.CB_post_facebook_comments_full)
        self.CB_post_facebook_comments_full.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_comments_full, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_comments_full)
        self.CB_post_facebook_factcheck = QCheckBox("factcheck")
        self.list_check_box.append(self.CB_post_facebook_factcheck)
        self.CB_post_facebook_factcheck.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_factcheck, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_factcheck)
        self.CB_post_facebook_image = QCheckBox("image")
        self.list_check_box.append(self.CB_post_facebook_image)
        self.CB_post_facebook_image.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_image, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_image)
        self.CB_post_facebook_image_lowquality = QCheckBox("image_lowquality")
        self.list_check_box.append(self.CB_post_facebook_image_lowquality)
        self.CB_post_facebook_image_lowquality.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_image_lowquality, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_image_lowquality)
        self.CB_post_facebook_images = QCheckBox("images")
        self.list_check_box.append(self.CB_post_facebook_images)
        self.CB_post_facebook_images.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_images, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_images)
        self.CB_post_facebook_images_description = QCheckBox("images_description")
        self.list_check_box.append(self.CB_post_facebook_images_description)
        self.CB_post_facebook_images_description.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_images_description, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_images_description)
        self.CB_post_facebook_images_lowquality = QCheckBox("images_lowquality")
        self.list_check_box.append(self.CB_post_facebook_images_lowquality)
        self.CB_post_facebook_images_lowquality.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_images_lowquality, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_images_lowquality)
        self.CB_post_facebook_images_lowquality_description = QCheckBox("images_lowquality_description")
        self.list_check_box.append(self.CB_post_facebook_images_lowquality_description)
        self.CB_post_facebook_images_lowquality_description.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_images_lowquality_description, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_images_lowquality_description)
        self.CB_post_facebook_is_live = QCheckBox("is_live")
        self.list_check_box.append(self.CB_post_facebook_is_live)
        self.CB_post_facebook_is_live.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_is_live, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_is_live)
        self.CB_post_facebook_likes = QCheckBox("likes")
        self.list_check_box.append(self.CB_post_facebook_likes)
        self.CB_post_facebook_likes.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_likes, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_likes)
        self.CB_post_facebook_link = QCheckBox("link")
        self.list_check_box.append(self.CB_post_facebook_link)
        self.CB_post_facebook_link.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_link, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_link)
        self.CB_post_facebook_post_id = QCheckBox("post_id")
        self.list_check_box.append(self.CB_post_facebook_post_id)
        self.CB_post_facebook_post_id.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_post_id, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_post_id)
        self.CB_post_facebook_post_text = QCheckBox("post_text")
        self.list_check_box.append(self.CB_post_facebook_post_text)
        self.CB_post_facebook_post_text.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_post_text, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_post_text)
        self.CB_post_facebook_post_url = QCheckBox("post_url")
        self.list_check_box.append(self.CB_post_facebook_post_url)
        self.CB_post_facebook_post_url.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_post_url, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_post_url)
        self.CB_post_facebook_reactors = QCheckBox("reactors")
        self.list_check_box.append(self.CB_post_facebook_reactors)
        self.CB_post_facebook_reactors.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_reactors, self.list_param_posts))
        layout_CB_post_facebook_up.addWidget(self.CB_post_facebook_reactors)
        self.CB_post_facebook_shared_post_id = QCheckBox("shared_post_id")
        self.list_check_box.append(self.CB_post_facebook_shared_post_id)
        self.CB_post_facebook_shared_post_id.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_shared_post_id, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_shared_post_id)
        self.CB_post_facebook_shared_post_url = QCheckBox("shared_post_url")
        self.list_check_box.append(self.CB_post_facebook_shared_post_url)
        self.CB_post_facebook_shared_post_url.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_shared_post_url, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_shared_post_url)
        self.CB_post_facebook_shared_text = QCheckBox("shared_text")
        self.list_check_box.append(self.CB_post_facebook_shared_text)
        self.CB_post_facebook_shared_text.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_shared_text, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_shared_text)
        self.CB_post_facebook_shared_time = QCheckBox("shared_time")
        self.list_check_box.append(self.CB_post_facebook_shared_time)
        self.CB_post_facebook_shared_time.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_shared_time, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_shared_time)
        self.CB_post_facebook_shared_user_id = QCheckBox("shared_user_id")
        self.list_check_box.append(self.CB_post_facebook_shared_user_id)
        self.CB_post_facebook_shared_user_id.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_shared_user_id, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_shared_user_id)
        self.CB_post_facebook_shared_username = QCheckBox("shared_username")
        self.list_check_box.append(self.CB_post_facebook_shared_username)
        self.CB_post_facebook_shared_username.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_shared_username, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_shared_username)
        self.CB_post_facebook_shares = QCheckBox("shares")
        self.list_check_box.append(self.CB_post_facebook_shares)
        self.CB_post_facebook_shares.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_shares, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_shares)
        self.CB_post_facebook_text = QCheckBox("text")
        self.list_check_box.append(self.CB_post_facebook_text)
        self.CB_post_facebook_text.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_text, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_text)
        self.CB_post_facebook_time = QCheckBox("time")
        self.list_check_box.append(self.CB_post_facebook_time)
        self.CB_post_facebook_time.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_time, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_time)
        self.CB_post_facebook_user_id = QCheckBox("user_id")
        self.list_check_box.append(self.CB_post_facebook_user_id)
        self.CB_post_facebook_user_id.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_user_id, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_user_id)
        self.CB_post_facebook_user_url = QCheckBox("user_url")
        self.list_check_box.append(self.CB_post_facebook_user_url)
        self.CB_post_facebook_user_url.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_user_url, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_user_url)
        self.CB_post_facebook_username = QCheckBox("username")
        self.list_check_box.append(self.CB_post_facebook_username)
        self.CB_post_facebook_username.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_username, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_username)
        self.CB_post_facebook_video = QCheckBox("video")
        self.list_check_box.append(self.CB_post_facebook_video)
        self.CB_post_facebook_video.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video)
        self.CB_post_facebook_video_id = QCheckBox("video_id")
        self.list_check_box.append(self.CB_post_facebook_video_id)
        self.CB_post_facebook_video_id.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_id, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_id)
        self.CB_post_facebook_video_width = QCheckBox("video_width")
        self.list_check_box.append(self.CB_post_facebook_video_width)
        self.CB_post_facebook_video_width.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_width, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_width)
        self.CB_post_facebook_video_duration_seconds = QCheckBox("video_duration_seconds")
        self.list_check_box.append(self.CB_post_facebook_video_duration_seconds)
        self.CB_post_facebook_video_duration_seconds.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_duration_seconds, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_duration_seconds)
        self.CB_post_facebook_video_height = QCheckBox("video_height")
        self.list_check_box.append(self.CB_post_facebook_video_height)
        self.CB_post_facebook_video_height.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_height, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_height)
        self.CB_post_facebook_video_quality = QCheckBox("video_quality")
        self.list_check_box.append(self.CB_post_facebook_video_quality)
        self.CB_post_facebook_video_quality.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_quality, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_quality)
        self.CB_post_facebook_video_size_MB = QCheckBox("video_size_MB")
        self.list_check_box.append(self.CB_post_facebook_video_size_MB)
        self.CB_post_facebook_video_size_MB.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_size_MB, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_size_MB)
        self.CB_post_facebook_video_watches = QCheckBox("video_watches")
        self.list_check_box.append(self.CB_post_facebook_video_watches)
        self.CB_post_facebook_video_watches.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_watches, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_watches)
        self.CB_post_facebook_video_thumbnail = QCheckBox("video_thumbnail")
        self.list_check_box.append(self.CB_post_facebook_video_thumbnail)
        self.CB_post_facebook_video_thumbnail.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_video_thumbnail, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_video_thumbnail)
        self.CB_post_facebook_w3_fb_url = QCheckBox("w3_fb_url")
        self.list_check_box.append(self.CB_post_facebook_w3_fb_url)
        self.CB_post_facebook_w3_fb_url.stateChanged.connect(
            lambda: self.parameters_add_remove(self.CB_post_facebook_w3_fb_url, self.list_param_posts))
        layout_CB_post_facebook_bottom.addWidget(self.CB_post_facebook_w3_fb_url)
        self.FR_post_facebook_up = QFrame()
        self.FR_post_facebook_up.setLayout(layout_CB_post_facebook_up)
        self.FR_post_facebook_up.hide()
        self.FR_post_facebook_bottom = QFrame()
        self.FR_post_facebook_bottom.setLayout(layout_CB_post_facebook_bottom)
        self.FR_post_facebook_bottom.hide()

        # table for showing tweets/posts
        self.LA_text_result = QLabel("Tweets/posts")
        self.LA_text_result.hide()
        self.T_text_result = QTableWidget()
        header = self.T_text_result.horizontalHeader()
        header.setStretchLastSection(True)
        self.T_text_result.hide()

        # table for showing some info about those tweets/posts (words count, letters count, link)
        self.LA_text_info = QLabel("Info about the tweets/posts")
        self.LA_text_info.hide()
        self.T_text_info = QTableWidget()
        header = self.T_text_info.horizontalHeader()
        header.setStretchLastSection(True)
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

        # table for showing the users of those tweets/posts (twitter only)
        self.LA_user_result = QLabel("Users")
        self.LA_user_result.hide()
        self.T_user_result = QTableWidget()
        header = self.T_user_result.horizontalHeader()
        header.setStretchLastSection(True)
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
        layout = QFormLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.LE_keyWord)
        layout.addWidget(self.LE_starting_date)
        layout.addWidget(self.LE_ending_date)
        layout.addWidget(self.LE_tweet_post_number)
        layout.addWidget(self.CB_twitter)
        layout.addWidget(self.CO_twitter_lang)
        layout.addWidget(self.LA_tweet_twitter)
        layout.addRow(self.FR_tweet_twitter)
        layout.addWidget(self.LA_user_twitter)
        layout.addRow(self.FR_user_twitter)
        layout.addWidget(self.CB_facebook)
        layout.addWidget(self.LE_facebook_page_name)
        layout.addWidget(self.LA_post_facebook)
        layout.addWidget(self.FR_post_facebook_up)
        layout.addWidget(self.FR_post_facebook_bottom)
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

        # pre checked boxes
        self.CB_tweet_twitter_id.setChecked(True)
        self.CB_tweet_twitter_date.setChecked(True)
        self.CB_tweet_twitter_url.setChecked(True)
        self.CB_tweet_twitter_user.setChecked(True)
        self.CB_tweet_twitter_retweetedTweet.setChecked(True)
        self.CB_tweet_twitter_replyCount.setChecked(True)
        self.CB_tweet_twitter_quotedTweet.setChecked(True)
        self.CB_tweet_twitter_likeCount.setChecked(True)
        self.CB_tweet_twitter_content.setChecked(True)

        self.CB_user_twitter_id.setChecked(True)
        self.CB_user_twitter_username.setChecked(True)
        self.CB_user_twitter_displayname.setChecked(True)
        self.CB_user_twitter_description.setChecked(True)
        self.CB_user_twitter_verified.setChecked(True)
        self.CB_user_twitter_followersCount.setChecked(True)
        self.CB_user_twitter_created.setChecked(True)

        self.CB_post_facebook_post_id.setChecked(True)
        self.CB_post_facebook_username.setChecked(True)
        self.CB_post_facebook_user_url.setChecked(True)
        self.CB_post_facebook_time.setChecked(True)
        self.CB_post_facebook_text.setChecked(True)
        self.CB_post_facebook_comments.setChecked(True)
        self.CB_post_facebook_post_url.setChecked(True)
        self.CB_post_facebook_reactors.setChecked(True)

    def parameters_twitter_user(self, check_box, list_parameters):
        # uncheck all user data if user is disable
        self.parameters_add_remove(check_box, list_parameters)
        if not check_box.checkState():
            for one_check_box in self.list_check_box_user_twitter:
                one_check_box.setChecked(False)

    def parameters_add_remove(self, check_box, list_parameters):
        # synchronize the list of parameters with the check boxes
        if check_box.checkState():
            list_parameters.append("{}".format(check_box.text()))
            if check_box in self.list_check_box_user_twitter:
                self.CB_tweet_twitter_user.setChecked(True)
        elif check_box.text() in list_parameters:
            list_parameters.remove("{}".format(check_box.text()))

    def func_CB_twitter(self):
        # show/hide widgets
        if self.CB_twitter.checkState():
            self.CB_facebook.setChecked(False)
            self.CO_twitter_lang.show()
            self.LA_tweet_twitter.show()
            self.FR_tweet_twitter.show()
            self.LA_user_twitter.show()
            self.FR_user_twitter.show()
        else:
            self.CO_twitter_lang.hide()
            self.LA_tweet_twitter.hide()
            self.FR_tweet_twitter.hide()
            self.LA_user_twitter.hide()
            self.FR_user_twitter.hide()
        self.hideUselessWidgets()

    def func_CB_facebook(self):
        # show/hide widgets
        if self.CB_facebook.checkState():
            self.CB_twitter.setChecked(False)
            self.LE_facebook_page_name.show()
            self.LA_post_facebook.show()
            self.FR_post_facebook_up.show()
            self.FR_post_facebook_bottom.show()
        else:
            self.LE_facebook_page_name.hide()
            self.LA_post_facebook.hide()
            self.FR_post_facebook_up.hide()
            self.FR_post_facebook_bottom.hide()
        self.hideUselessWidgets()

    def hideUselessWidgets(self):
        # hide widgets and clear data
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
        self.LE_json.clear()
        self.data_posts = None
        self.data_users = None
        self.data_analyse = None

    def func_BU_json(self):
        # export the dataframes on json format
        data_users_parsed = None
        if self.data_posts.empty:
            self.statusBar().showMessage("ERROR: Selection empty")
        elif not self.LE_json.text():
            self.statusBar().showMessage("ERROR: Please enter a file name")
        else:
            data_posts_parsed = json.loads(self.data_posts.to_json(orient="split"))
            with open(".\\export\\{}_posts.json".format(self.LE_json.text()), 'w') as outfile:
                json.dump(data_posts_parsed, outfile)
            if self.data_users is not None and not self.data_users.empty:
                data_users_parsed = json.loads(self.data_users.to_json(orient="split"))
                with open(".\\export\\{}_users.json".format(self.LE_json.text()), 'w') as outfile:
                    json.dump(data_users_parsed, outfile)
            if self.data_analyse is not None and not self.data_analyse.empty:
                data_analyse_parsed = json.loads(self.data_analyse.to_json(orient="split"))
                with open(".\\export\\{}_analyse.json".format(self.LE_json.text()), 'w') as outfile:
                    json.dump(data_analyse_parsed, outfile)

            self.statusBar().showMessage("SUCCESS: Files saved")

    def func_BU_validate(self):
        # recover data and put it in dataframe
        self.hideUselessWidgets()
        self.data_analyse = None
        self.T_user_result.clearContents()
        self.T_text_info.clearContents()
        self.T_text_result.clearContents()
        self.T_text_common.clearContents()

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
            id_text = "Null"
            id_url = "Null"

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
                self.data_posts = pd.DataFrame(sliced_scraped_tweets)[self.list_param_posts]

                # recover data from users
                data_users_old = []
                if 'user' in self.data_posts:
                    for i in range(len(self.data_posts)):
                        data_users_old.append(self.data_posts['user'][i])
                    self.data_users = [None] * len(data_users_old)
                    user_keys = self.list_param_users

                    for i in range(len(data_users_old)):
                        self.data_users[i] = {user_key: data_users_old[i][user_key] for user_key in user_keys}
                    self.data_users = pd.DataFrame(self.data_users)
                if 'content' in self.data_posts:
                    id_text = 'content'
                elif 'renderedContent' in self.data_posts:
                    id_text = 'renderedContent'
                if 'url' in self.data_posts:
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
                for i in range(len(data_posts_old)):
                    self.data_posts[i] = {post_key: data_posts_old[i][post_key] for post_key in self.list_param_posts}
                self.data_posts = pd.DataFrame(self.data_posts)

                if 'text' in self.data_posts:
                    id_text = 'text'
                if 'post_url' in self.data_posts:
                    id_url = 'post_url'

            if id_text in self.data_posts or id_url in self.data_posts:
                # compute some info
                horizontal_header = []
                self.data_analyse = [None] * len(self.data_posts)
                for i in self.data_posts.index:
                    if id_text in self.data_posts:
                        self.data_analyse[i] = {"word_count": len(self.data_posts[id_text][i].split())}
                        self.data_analyse[i]['length'] = len(self.data_posts[id_text][i])
                        if 'words count' not in horizontal_header:
                            horizontal_header.extend(('words count', 'letters count'))
                    if id_url in self.data_posts:
                        if self.data_analyse[i] is None:
                            self.data_analyse[i] = {'source': self.data_posts[id_url][i]}
                        else:
                            self.data_analyse[i]['source'] = self.data_posts[id_url][i]
                        if 'source' not in horizontal_header:
                            horizontal_header.append('source')
                self.T_text_info.setColumnCount(len(horizontal_header))
                self.T_text_info.setHorizontalHeaderLabels(horizontal_header)
                self.data_analyse = pd.DataFrame(self.data_analyse)
            self.show_data_sample(id_text)
            self.BU_json.show()
            self.LE_json.show()

    def unCheckCB(self):
        # uncheck all check boxes
        for check_box in self.list_check_box:
            check_box.setChecked(False)
        for check_box in self.list_check_box_user_twitter:
            check_box.setChecked(False)

    def removeNotShowable(self, list_param, dataframe):
        # remove all parameters which are not showable (it's only for the tables, the dataframe is untouched)
        pd.set_option('display.max_columns', None)
        list_tmp = []
        for param in list_param:
            if isinstance(dataframe[param][0], (str, np.int64, pd._libs.tslibs.timestamps.Timestamp, np.bool_)):
                list_tmp.append(param)
        list_param.clear()
        for param in list_tmp:
            list_param.append(param)

    def show_data_sample(self, id_text):
        # fill in the tables
        self.removeNotShowable(self.list_param_posts, self.data_posts)
        self.T_text_result.setColumnCount(len(self.list_param_posts))
        self.T_text_result.setRowCount(len(self.data_posts))
        self.T_text_result.setHorizontalHeaderLabels(self.list_param_posts)
        if 'user' in self.data_posts:
            self.removeNotShowable(self.list_param_users, self.data_users)
            self.T_user_result.setColumnCount(len(self.list_param_users))
            self.T_user_result.setRowCount(len(self.data_users))
            self.T_user_result.setHorizontalHeaderLabels(self.list_param_users)
        self.T_text_info.setRowCount(len(self.data_posts))
        self.unCheckCB()

        # show posts/tweets
        for i in range(len(self.data_posts)):
            h = 0
            for j in range(len(self.data_posts.columns)):
                if isinstance(self.data_posts.iloc[i, j],
                              (str, np.int64, pd._libs.tslibs.timestamps.Timestamp, np.bool_)):
                    self.T_text_result.setItem(i, h, QTableWidgetItem("{}".format(self.data_posts.iloc[i, j])))
                    h += 1

        # show info about those tweets/posts
        if self.data_analyse is not None:
            for i in range(len(self.data_posts)):
                for j in range(len(self.data_analyse.columns)):
                    self.T_text_info.setItem(i, j, QTableWidgetItem("{}".format(self.data_analyse.iloc[i, j])))
            self.LA_text_info.show()
            self.T_text_info.show()

        # Show most common words
        if id_text in self.data_posts:
            common_words = Counter(" ".join(self.data_posts[id_text]).split()).most_common(5)

            i = 0
            for x, y in common_words:
                self.T_text_common.setItem(0, i, QTableWidgetItem("{}".format(x)))
                self.T_text_common.setItem(1, i, QTableWidgetItem("{}".format(y)))
                i += 1
            self.LA_text_common.show()
            self.T_text_common.show()

        # Show users if it's twitter
        if self.CB_twitter.checkState() and 'user' in self.data_posts:
            for i in range(len(self.data_users)):
                h = 0
                for j in range(len(self.data_users.columns)):
                    if isinstance(self.data_users.iloc[i, j],
                                  (str, np.int64, pd._libs.tslibs.timestamps.Timestamp, np.bool_)):
                        self.T_user_result.setItem(i, h, QTableWidgetItem("{}".format(self.data_users.iloc[i, j])))
                        h += 1
            self.T_user_result.show()
            self.LA_user_result.show()

        self.LA_text_result.show()
        self.T_text_result.show()


app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

Window = Windows()
Window.resize(app.primaryScreen().size().width() - 50, app.primaryScreen().size().height() - 100)
Window.show()

app.exec_()
