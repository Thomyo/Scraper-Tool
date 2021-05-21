# Scraper-Tool

It's a very simple gui for snscrape-twitter and facebook-scraper.

The API come from:  
-snscrape : https://github.com/JustAnotherArchivist/snscrape  
-facebook-scraper : https://github.com/kevinzg/facebook-scraper

The gui works with PyQt5

For Twitter  
-You enter a keyword, the dates (beginning and ending) and the number of tweets.  
-The program calls the API and send you back the tweets and the users data.  
-The first five tweets and users info are shown in the gui. The gui does not allow the selection of particular attributes.  
-You can export it in json.

For Facebook (WARNING : SLOW)   
-You enter a keyword, the dates (beginning and ending), the number of posts and the name of the page (Facebook does not have a general search bar like Twitter).  
-The program calls the API and send you back the posts data (I did not implement yet the users data).  
-The first five posts info are shown in the gui. The gui does not allow the selection of particular attributes.  
-You can export it in json. 
