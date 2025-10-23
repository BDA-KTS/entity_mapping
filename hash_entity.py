import hashlib
import json
import ijson
import re
from urllib.parse import urlsplit
from glob import glob
from tqdm import tqdm

def hash_entity(input_dir_path, output_dir_path, regex):
    for _id in tqdm(glob("/data_ssd/linzbasn/raw_data/*.json")):
        _id = _id.split("/")[-1][:-5]
        with open(f"/data_ssd/linzbasn/raw_data/{_id}.json") as f:
            d = json.load(f)
        replaced_data = []
        comment_new = []
        net_loc = []
        j = 0
        url_regex = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
        tmp = d
        for i, p in enumerate(d['posts']):
            if not p.get('com'):
                continue
            tmp['posts'][i]['com'] = p['com'].replace('<wbr>', '').replace('<br>', ' ')
            _match = re.findall(url_regex,  tmp['posts'][i]['com'])
            tmp['posts'][i]['url_hash'] = []
            tmp['posts'][i]['pld_hash'] = []
            for url in _match:
                url_f = url[:40]
                try:
                    url_e = urlsplit(url_f).netloc
                except:
                    url_e = 'unkown'
                net_loc = hashlib.md5(url_e.encode()).hexdigest()
                res = hashlib.md5(url.encode()).hexdigest()
                tmp['posts'][i]['com'] = tmp['posts'][i]['com'].replace(url, "<link><url_hash>"+ res +"</url_hash>" + "<pld_hash>"+ net_loc + "</pld_hash></link>")
                tmp['posts'][i]['url_hash'].append(res)  
                tmp['posts'][i]['pld_hash'].append(net_loc)  
                j += 1

        with open(f"/data_ssd/linzbasn/raw_data/hashed/{_id}_thread.json", "w") as f:
            json.dump(tmp, f)
        del tmp, d
