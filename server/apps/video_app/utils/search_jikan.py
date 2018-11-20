import difflib
from requests import Session

session = Session()

SEARCH_URL = "https://api.jikan.moe/search/anime/?q={}"


def search_jikan(anime):
    """ 
    searchs the jikan api for anime information from MAL 
    """
    # all_results = session.get(SEARCH_URL.format(anime), verify=False).json()["result"]
    all_results = session.get(SEARCH_URL.format(anime)).json()["result"]
    titles = [result["title"].lower() for result in all_results]
    matches = difflib.get_close_matches(anime, titles, n=1, cutoff=0.5)
    entry = ""
    if len(matches) > 0:
        for result in all_results:
            if result["title"].lower() == matches[0]:
                entry = result
                break
    else:
        # fallback if the name doesn't match
        entry = all_results[0]
    return entry