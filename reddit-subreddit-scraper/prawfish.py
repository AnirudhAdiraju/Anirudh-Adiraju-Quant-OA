import praw
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


#initalize a Reddit class from PRAW reddit API wrapper
reddit = praw.Reddit(
    client_id="-Jxhm8buMMfJJduzz5vVBA",
    client_secret="8T4u_1XztVhpvsjnPb2th905wRTUjQ",
    user_agent="test",
)

#get user input about what subreddit to scrape and validate the input, added a little spice to the validation messages
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

#get start and end dates for the past 26 weeks and place in an array
cur_date = datetime.today()
past_date = cur_date - relativedelta(months=6)
weeks_raw = pd.date_range(start = past_date, end = cur_date, periods = 27).to_pydatetime().tolist()
weeks = {'num_less_than_three': 0}
for week in range(len(weeks_raw)-1):
  weeks[week]={'date_range': (weeks_raw[week].date(),weeks_raw[week+1].date()),'posts': []}


#retrieve all posts on subreddit, sorted by upvotes 
for submission in reddit.subreddit(sub_red).top(time_filter="all", limit=None):
    weeks_ago = (datetime.timestamp(cur_date)-submission.created_utc)/604800
    if(weeks_ago < 26):
      if(len(weeks[int(26-weeks_ago)]['posts'])<5):
          post = {'num_of_upvotes': submission.score, 'replies': submission.comments}
          weeks[int(26-weeks_ago)]['posts'].append(post)

print(weeks)