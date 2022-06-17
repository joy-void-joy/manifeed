# manifeed
RSS feed for new manifold markets
(If you want the cannonical rss feed: https://whatisthis.world/manifeed.xml )

# Usage
After setting a virtualenv:

```
pip install -r requirements.txt
```
Then:
```
python main.py
```

First pass will just register the newest market. Anytime you run it, it will append new markets to feed.xml.
You might want to run it inside a cron job for automatic updates
