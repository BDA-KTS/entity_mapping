import hashlib
import json
import re
from urllib.parse import urlsplit
from glob import glob
import pandas as pd

entity_regex = {
'url' : r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',       # urls
'Mentions': r'(?<!\w)@[\w.\-]+(?:@[\w\.\-]+\.\w+)?',                                           # including both normal and mastodon mentions
'Hashtags': r'#\w+',                                                                           # hashtags
'All_caps': r'\b(?:[A-Z]{2,})\b',                                                              # All caps words
'Emojis': r'[\U00010000-\U0010ffff]',                                                          # Basic Unicode emoji range   
# add other regex 
}
def hash_entity(input_data, entity_type = "url"):

    if entity_type == "url":
        regex = entity_regex[entity_type]

    hashed_entities = []
    input_with_hashed_entities = []
    for post in input_data:
        _matched_entities = re.findall(regex,  post)
        
        for entity in _matched_entities:
            if entity_type == "url":
                entity_f = entity[:40]
                try:
                    entity_e = urlsplit(entity_f).netloc
                except:
                    entity_e = 'unkown'
                net_loc = hashlib.md5(entity_e.encode()).hexdigest()
                res = hashlib.md5(entity.encode()).hexdigest()
                input_with_hashed_entities.append(post.replace(entity, "<hashed_entity><url_hash>"+ res +"</url_hash>" + "<pld_hash>"+ net_loc + "</pld_hash></hashed_entity>"))
                hashed_entities.append("res:" + res + "\tnet_loc" + net_loc)  
            # for other entities (non URL)
            else:
                hash_entity = hashlib.md5(entity.encode()).hexdigest()
                input_with_hashed_entities.append(post.replace(entity, "<hashed_entity>" + hash_entity + "</hashed_entity>"))
                hashed_entities.append(hash_entity)  
    df = pd.DataFrame({'hashed_posts': input_with_hashed_entities, 'hashed_entities': hashed_entities})
    return df          
    
if __name__ == "__main__":
    with open("data/input_data.txt", "r", encoding="utf-8") as file:
        posts = file.read().split('\n')
    df = hash_entity(posts, "url")
    df.to_csv("data/output_data.tsv", sep = "\t", encoding = "utf-8")
