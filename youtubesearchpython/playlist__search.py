import json
import asyncio

from youtubesearchpython.__requesthandler import RequestHandler
from youtubesearchpython.playlist__scripthandler import ScriptHandler


class SearchPlaylists(RequestHandler, ScriptHandler):

    '''
    Search for playlists in YouTube.

    Parameters
    ----------
    keyword : str
        Used as a query to search for playlists in YouTube.
    offset : int, optional
        Offset for result pages on YouTube. Defaults to 1.
    mode : str
        Search result mode. Can be 'json', 'dict' or 'list'.
    maxResults : int, optional
        Maximum number of playlist results. Defaults to 20.

    Methods
    -------
    search()
        Searches for the playlists in YouTube
    result()
        Returns the playlists fetched from YouTube by search().
    '''

    networkError = False
    validResponse = False
    searchComplete = False

    def __init__(self, keyword: str, offset : int = 1, mode : str = 'json', maxResults : int = 20):

        self.offset = offset
        self.mode = mode
        self.keyword = keyword
        self.maxResults = maxResults
        self.searchPreferences = 'EgIQAw%3D%3D'

    async def search(self):
        
        await self.request()

        if self.networkError:
            self.networkError = True
        else:
            self.scriptResponseHandler()
        self.searchComplete = True

    def result(self):

        '''
        Returns
        -------
        None, str, dict, list
            Returns playlist results from YouTube. Returns None if self.search() is not awaited or called.
        '''

        if self.searchComplete:
            if self.networkError:
                return None

            else:

                result = []
                
                if self.mode in ['json', 'dict']:

                    for index in range(len(self.ids)):
                        result_index = {
                            'index': index,
                            'id': self.ids[index],
                            'link': self.links[index],
                            'title': self.titles[index],
                        }
                        result+=[result_index]

                    if self.mode == 'json':
                        return json.dumps({'search_result': result}, indent=4)
                    else:
                        return {'search_result': result}
                
                elif self.mode == 'list':
                    
                    for index in range(len(self.ids)):
                        list_index=[
                            index,
                            self.ids[index],
                            self.links[index],
                            self.titles[index],
                        ]
                        result+=[list_index]
                    
                    return result
        else:
            return None

    def __enter__(self):
        return self

    def __exit__(self, execType, execValue, traceback):
        pass
