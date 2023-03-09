import streamlit as st
import pymongo
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date
from io import StringIO

st.title("Tweeter scrape")
# Setting variables to be used below
maxTweets = 1000
# Creating list to append tweet data to
tweets_list2 = []
# Using TwitterSearchScraper to scrape data and append tweets to list
tagoruser=st.sidebar.text_input("Enter the User_Hashtag:")
fromdate=st.sidebar.date_input("From_date(YYYY-MM-DD):")
enddate=st.sidebar.date_input("End_date(YYYY-MM-DD):")
tweets_count=st.sidebar.number_input("enter the count:",min_value=1,max_value=100)

if st.button('Click me'):
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"from:{tagoruser} since:{fromdate} until:{enddate}").get_items()):
        if i>maxTweets:
            break
        tweets_list2.append([ tweet.id,
                        tweet.user.username,
                        tweet.url,
                        tweet.rawContent,
                        tweet.replyCount,
                        tweet.retweetCount,
                        tweet.likeCount,
                        tweet.lang,
                        tweet.source,
                        tweet.date,])


tweets_df2 = pd.DataFrame(tweets_list2, columns=['Tweet Id','Username', 'URL', 'Content', 'Replay Count', 'Re Tweet', 'Like Count', 'Lang', 'Source','Datetime'])
tweets_df2

myDict=tweets_df2.to_dict('list')

server=pymongo.MongoClient('mongodb+srv://vasanl:12345@cluster0.85yph4l.mongodb.net')
disk=server.DSGUVI
collection=disk.demotweet

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)
    dataframe = pd.read_csv(uploaded_file)
    myDict2=dataframe.to_dict('list')
#     myDict2
    collection.insert_one(myDict2)
    st.success('Upload to MongoDB Successful!', icon="✅")
    
  #Download file  
def convert_df(dataframe):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv().encode('utf-8')

mycsv = convert_df(tweets_df2)

st.download_button(
    label="Download data as CSV",
    data=mycsv,
    file_name='scraped_data.csv',
    mime='text/csv',
)
