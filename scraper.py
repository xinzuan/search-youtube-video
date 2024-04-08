from parsenar import getChannelRenderData, getPlaylistData, getStreamData, getVideoData
from urllib.parse import urlencode
import aiohttp
from json import loads,dumps
from util import *
import json

from urllib.request import Request, urlopen

base_url = "https://www.youtube.com/"



class YouTubeSearch:
    base_url = "https://www.youtube.com/"

    def __init__(self, search_query):
        self.search_query = search_query
        self.token = None

    async def search(self, sp="video"):
        json1 = await self.request(self.search_query, sp, self.token)
        extracted, self.token = self.extract(json1)
        return self.parse_data(extracted)

    async def request(self, query, sp, token):
        
        session = aiohttp.ClientSession()
        res = None

        if not token:
            url = self.search_url(query, sp)
            response = await session.get(url)
            context = await response.text()
            context = ("=".join(("".join(context.split("\n"))).split("var ytInitialData")[1].split("=")[1:])).split(";</script>")[0]

            response = json.loads(context)["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]
        else:
            
            data = {
                "continuation": token,
                'context': {
                    'client': {
                        'clientName': 'WEB',
                        'clientVersion': '2.20200720.00.02'
                    }
                },
                "newVisitorCookie": True,
                "query": query,
            }
            requestBodyBytes = json.dumps(data).encode('utf_8')
            headers = {
                "Content-Type": "application/json",
                'Content-Length': len(requestBodyBytes),
            }
            request = Request('https://www.youtube.com/youtubei/v1/search',
                data=requestBodyBytes,
                headers={
                    'Content-Type': 'application/json; charset=utf-8',
                    'Content-Length': len(requestBodyBytes),
 
                }
            )

            response = urlopen(request).read().decode('utf_8')
            continuationContentPath = ['onResponseReceivedCommands', 0, 'appendContinuationItemsAction', 'continuationItems']
            response = {'sectionListRenderer': {'contents': getValue(json.loads(response), continuationContentPath)}}

        await session.close()

        return response

    def search_url(self, q, sp):
        return self.base_url + "results?" + urlencode({"search_query": q, "sp": sp})

    def extract(self, json, continuation=False):
        render = None
        contents = []

        if continuation:
            for item in section["itemSectionRenderer"]["contents"]:
                if len(item.get("videoRenderer", []) or item.get("playlistRenderer", []) or item.get("channelRenderer", [])) > 0:
                    render.append(section)
                if 'continuationItemRenderer' in section:
                    continuation_renderer = section['continuationItemRenderer']
            if len(render) > 0:
                contents = render[0]["itemSectionRenderer"]["contents"]
        else:
            sectionListRenderer = json.get("sectionListRenderer", None)

            continuation_renderer = None
            if sectionListRenderer is not None:
                render = []
                for section in sectionListRenderer.get("contents", []):
                    if "itemSectionRenderer" in section and "contents" in section["itemSectionRenderer"]:
                        for item in section["itemSectionRenderer"]["contents"]:
                            if len(item.get("videoRenderer", []) or item.get("playlistRenderer", []) or item.get("channelRenderer", [])) > 0:
                                render.append(section)
                    if 'continuationItemRenderer' in section:
                        continuation_renderer = section['continuationItemRenderer']
                if len(render) > 0:
                    contents = render[0]["itemSectionRenderer"]["contents"]

        if continuation_renderer:
            next_continuation = continuation_renderer['continuationEndpoint']['continuationCommand']['token']
        else:
            next_continuation = None

        richGridRenderer = json.get("richGridRenderer", None)
        if richGridRenderer is not None:
            contents = richGridRenderer.get("contents", [])
            _contents = []

            for content in contents:
                if "richItemRenderer" in content and "content" in content["richItemRenderer"]:
                    _contents.append(content["richItemRenderer"]["content"])
            contents = _contents

        return contents, next_continuation

    def parse_data(self, json):
        results = {
            "videos": [],
        }
        for item in json:
            # Channel
            if "channelRenderer" in item:
                try:
                    result = getChannelRenderData(item["channelRenderer"])
                    results["videos"].append(result)
                except Exception as e:
                    raise Exception(buildTraceback(e))

            # Video
            if "videoRenderer" in item and "lengthText" in item["videoRenderer"]:
                try:
                    result = getVideoData(item.get("videoRenderer"))
                    results["videos"].append(result)
                except Exception as e:
                    raise Exception(buildTraceback(e))

            # Live Stream Video
            if "videoRenderer" in item and "lengthText" not in item["videoRenderer"]:
                try:
                    result = getStreamData(item["videoRenderer"])
                    results["videos"].append(result)
                except Exception as e:
                    raise Exception(buildTraceback(e))

            # Playlist
            if "playlistRenderer" in item:
                try:
                    result = getPlaylistData(item["playlistRenderer"])
                    results["videos"].append(result)
                except Exception as e:
                    raise Exception(buildTraceback(e))

        return results

    async def next(self, sp="video"):
        if self.token:
            return await self.search(sp)
        else:
            print("No more results available.")
            return None
