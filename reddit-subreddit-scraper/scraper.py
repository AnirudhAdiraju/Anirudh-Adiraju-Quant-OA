import praw
import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from praw.models import MoreComments

#function to receive and validate user input, there is currently a little bit of sass in the response message but this can be changed for professionalism
def get_user_input():
  sub_red = ""
  valid = False
  count = 0
  while(not valid):
      if(count == 0):
          sub_red = input("Enter a subreddit name (don't include the r/): ")
          count+=1
      else:
          if(sub_red[0]=='r' and sub_red[1]=='/'):
              count+=1
              sub_red = input("Enter the name again, this time without the r/ (Bro I swear I just told you not to include the r/): ")
          else:
              valid = True
  return sub_red

#function to get start and end dates for the past 26 weeks and place in a dictionary that will continue to hold info about the subreddit
def weeks(sub_red_info):
  cur_date = datetime.today()
  past_date = cur_date - relativedelta(months=6)
  weeks_raw = pd.date_range(start = past_date, end = cur_date, periods = 27).to_pydatetime().tolist()
  for week in range(len(weeks_raw)-1):
    sub_red_info[week]={'date_range': (weeks_raw[week].date(),weeks_raw[week+1].date()),'posts': []}

  
  
#function to get top 6 comments and metrics of the comments of a certain subreddit post
def get_comments(comments):
  replies = {}
  comments = comments[0:6]
  for i in range(len(comments)):
    if isinstance(comments[i], MoreComments):
      continue
    else:
      replies[i] = {'upvotes': comments[i].score, 'text': comments[i].body, }
  return replies

#function to get the number of accounts less than 3 months old
def get_num_less_than_three(cur_date, all_comments):
  past_date = cur_date - relativedelta(months=3)
  users = set()
  for comment in all_comments:
    author = comment.author
    if(datetime.fromtimestamp(author.created_utc)>=past_date):
      users.add(author)
  return len(users)

def scraper():
  #initalize a Reddit class from PRAW reddit API wrapper
  reddit = praw.Reddit(
      client_id="-Jxhm8buMMfJJduzz5vVBA",
      client_secret="8T4u_1XztVhpvsjnPb2th905wRTUjQ",
      user_agent="test",
  )
  
  #get user input about what subreddit to scrape and validate the input
  sub_red = get_user_input()
  
  #create a dictionary to store all subreddit info
  sub_red_info = {'num_less_than_three': 0}
  
  #make function call about initializing the 26 weeks to scrape data
  cur_date = datetime.today()
  weeks(sub_red_info)
  
  #retrieve all posts on subreddit, sorted by upvotes and place into dictionary for easy organization
  for submission in reddit.subreddit(sub_red).top(time_filter="all", limit=None):
      weeks_ago = (datetime.timestamp(cur_date)-submission.created_utc)/604800
      if(weeks_ago < 26):
        if(len(sub_red_info[int(26-weeks_ago)]['posts'])<5):
            replies = get_comments(submission.comments)
            post = {'upvotes': submission.score, 'replies': replies}
            sub_red_info[int(26-weeks_ago)]['posts'].append(post)
          
  #run function to get number of users than 3 months old and set value of dictionary to the value returned by this function
  #the number of accounts function goes through many of the comments on the subreddit, but the limit of the comments can be changed here to allow for more accuracy or speed
  sub_red_info['num_less_than_three'] = get_num_less_than_three(cur_date, reddit.subreddit(sub_red).comments(limit=10))
  return(sub_red_info)

#call scraper function and then convert the dictionary that is returned to JSON in order to put it in an output JSON file
x = scraper()
out = open("scraper.json", "w")
json.dump(x, out, indent = 4, sort_keys = False, default = str)
out.close()