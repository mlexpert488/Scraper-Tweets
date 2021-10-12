import streamlit as st
import pandas as pd
import numpy as np
import tweepy
import base64
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

st.write(
    """ 
# Simple Twitter Tweets Scraper 

You can use this tool to scrape tweets from Twitter for multiple users and save them to a CSV file. 
"""
)
consumer_key = "R1coNCuo2L2God23pgjMB4iYn"
consumer_secret = "fQ0THkl7jpWdsXiG0W4D7gVbFC1UiQ1tAZQ0yLkSJB6foi9hUC"
access_token = "1301803926618927105-PwMZBGfZXMhFVSLNlquTk1qzb4ARmB"
access_token_secret = "9brf8CDkk0mdY0zUDp36ayBmuAu6kV0WaDTahxDq2IoIP"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

number_of_tweets = 50
tweets = []
likes = []
time = []
retweets = []
author = []


def csv_downloader(data):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file_{}_.csv".format(timestr)
    st.markdown("#### Download CSV File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here to download!!</a>'
    st.markdown(href, unsafe_allow_html=True)


# take list as an input from the user in streamlit
user_list = st.text_input("Enter a list of Twitter users (separated by commas):")
list1 = user_list.split("," or ", ")

if st.button("Scrape Tweets"):
    for username in list1:
        for i in tweepy.Cursor(
            api.user_timeline, id=username, tweet_mode="extended"
        ).items(number_of_tweets):
            tweets.append(i.full_text)
            likes.append(i.favorite_count)
            time.append(i.created_at)
            retweets.append(i.retweet)
            author.append(i.author.name)

    df = pd.DataFrame(
        {"tweets": tweets, "likes": likes, "time": time, "author": author}
    )
    st.dataframe(df)

    csv_downloader(df)
