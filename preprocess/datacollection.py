import calendar
import datetime
import requests
import pickle as pkl

timestamp = calendar.timegm(datetime.datetime.now().utctimetuple())
timestamp = calendar.timegm(datetime.datetime(2018, 1, 1).utctimetuple())
first = calendar.timegm(datetime.datetime(2014, 1, 1).utctimetuple())
posts = []

while timestamp > first:
    url = ("https://api.pushshift.io/reddit/search/submission/"
           "?subreddit=rateme&sort=desc&sort_type=created_utc&"
           "before={}&size=1000").format(timestamp)
    r = requests.get(url).json()
    posts += r['data']
    print("Added posts from {} to {}".format(datetime.datetime.fromtimestamp(r['data'][-1]['created_utc']),
                                             datetime.datetime.fromtimestamp(r['data'][0]['created_utc'])))
    timestamp = r['data'][-1]['created_utc']

pkl.dump(posts, open("../data/posts.pkl", "wb"))

timestamp = calendar.timegm(datetime.datetime(2018, 1, 1).utctimetuple())
first = calendar.timegm(datetime.datetime(2014, 1, 1).utctimetuple())
comments = []
while timestamp > first:
    url = ("https://api.pushshift.io/reddit/search/comment/"
           "?subreddit=rateme&sort=desc&sort_type=created_utc&"
           "before={}&size=1000").format(timestamp)
    r = requests.get(url).json()
    comments += r['data']
    print("Added comments from {} to {}".format(datetime.datetime.fromtimestamp(r['data'][-1]['created_utc']),
                                                datetime.datetime.fromtimestamp(r['data'][0]['created_utc'])))
    timestamp = r['data'][-1]['created_utc']

pkl.dump(comments, open("../data/comments.pkl", "wb"))
