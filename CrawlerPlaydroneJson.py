
#   Crawler for extracting privacy policy links from Playdrone
#   @AminRabinia
#   March 19

import json
from urllib.request import urlopen
import mechanize

playdrone_url="https://ia800501.us.archive.org/27/items/playdrone-snapshots/2014-10-31.json"

# reads Playdrone content from a local JSON DB and returns a list of privacy policy links
def read_JSON_local_db(db_name):
    jsondata=open(db_name)
    jdata=json.load(jsondata)
    linklist = []

    # search inside the metadata page for privacy_policy_url credit: Van4ozA
    def pretty_search(dict_of_data, key_to_search, search_for_first_only=True):

        search_result = set()
        if isinstance(dict_of_data, dict):
            for key in dict_of_data:
                key_value = dict_of_data[key]
                if key == key_to_search:
                    if search_for_first_only:
                        return key_value
                    else:
                        search_result.add(key_value)
                if isinstance(key_value, dict) or isinstance(key_value, list) or isinstance(key_value, set):
                    _search_result = pretty_search(key_value, key_to_search, search_for_first_only)
                    if _search_result and search_for_first_only:
                        return _search_result
                    elif _search_result:
                        for result in _search_result:
                            search_result.add(result)
        return search_result if search_result else None

    for item in jdata:
        metadatelink=item['metadata_url']
        response=urlopen(metadatelink)
        metadata=response.read().decode("utf-8")
        jdata2=json.loads(metadata)

        link=(pretty_search(jdata2,'privacy_policy_url'))
        if link is not None:
            linklist.append(link)

    return linklist

# returns only working privacy policy links
def check_links(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    try:
        html = br.open(url).read().decode('utf-8')
    except:
        return False #"HTTP Error 404: Not Found"

    return True


pplinks = read_JSON_local_db("scratch.json") # db contains Playdrone entries

print("\n There are %d privacy policy links" %len(pplinks))

linkset=set()

for link in pplinks:

    if check_links(link):
        linkset.add(link) # set removes duplicates

with open("pplinks.json", "w") as data_file:
    jobj=[{"link": str(line)} for line in linkset]
    json.dump(jobj, data_file,indent=2)             # Privcay policy links stored in JSON db

print("\n Finally %d privacy policy links stored" %len(linkset))
