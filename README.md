# Scraper-Tool

It's a very simple gui for snscrape-twitter and facebook-scraper.

The 2 API for scraping come from:  
-snscrape : https://github.com/JustAnotherArchivist/snscrape  
-facebook-scraper : https://github.com/kevinzg/facebook-scraper

The gui works with PyQt5
Fasttext is used to analyse the text

For Twitter
-You can search for a specific tweet via its id.
 OR
-You enter a keyword, the dates (beginning and ending) and the number of tweets.  

-You choose the attributes you want to retrieve.  
-The program calls the API and send you back the tweets and the users data.  
-The tweets and users info showable (str, date, int...) are shown in the gui.
-Basic information about the text is calculated: number of words/letter, most used (not stopwords) words.
-Prediction the emotion of the text and its propensity to be false.
-You can export it in json or csv.

For Facebook (WARNING : SLOW)   
-You enter a keyword, the dates (beginning and ending), the number of posts and the name of the page (Facebook does not have a general search bar like Twitter).   
-You choose the attributes you want to retrieve.  
-The program calls the API and send you back the posts data (I did not implement yet the users data).  
-The posts info showable (str, date, int...) are shown in the gui.
-Basic information about the text is calculated: number of words/letter, most used (not stopwords) words.
-Prediction the emotion of the text and its propensity to be false.
-You can export it in json or csv. 
