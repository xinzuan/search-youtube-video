# YouTube Video Finder
Find youtube videos by using input query without using youtube data api

This code was **modified** from https://github.com/hansputera/youtube-finder and https://github.com/alexmercerind/youtube-search-python.git.


# Usage
1. Example searching youtube videos given query
```
import asyncio
from scraper import YouTubeSearch

loop = asyncio.new_event_loop()
search_query = "blackpink pink venom"
search = YouTubeSearch(search_query)

# Perform initial search
res = loop.run_until_complete(search.search())
```
If success, the output will be

```json
{
   "videos":[
      {
         "uploaded":"1년 전",
         "duration":194,
         "id":"gQlMMD8auMs",
         "title":"BLACKPINK - ‘Pink Venom’ M/V",
         "link":"https://www.youtube.com/watch?v=gQlMMD8auMs",
         "thumbnail":"https://i.ytimg.com/vi/gQlMMD8auMs/hqdefault.jpg"
      },
      {
         "uploaded":"1년 전",
         "duration":196,
         "id":"RFMi3v0TXP8",
         "title":"BLACKPINK - ‘Pink Venom’ DANCE PRACTICE VIDEO",
         "link":"https://www.youtube.com/watch?v=RFMi3v0TXP8",
         "thumbnail":"https://i.ytimg.com/vi/RFMi3v0TXP8/hqdefault.jpg"
      },
      {
         "uploaded":"1년 전",
         "duration":188,
         "id":"3or3dp3qNQU",
         "title":"BLACKPINK - ‘Pink Venom’ (Official Audio)",
         "link":"https://www.youtube.com/watch?v=3or3dp3qNQU",
         "thumbnail":"https://i.ytimg.com/vi/3or3dp3qNQU/hqdefault.jpg"
      },
      ...
   ]
}
```

2. To find more results
```
res = loop.run_until_complete(search.next())

```
