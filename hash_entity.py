import os
import re
import json
import hashlib
import argparse
import pandas as pd

from glob import glob
from datetime import datetime
from urllib.parse import urlsplit



def parse_args():
    parser = argparse.ArgumentParser(description="Process input files with regex transformations and hashing.")
    entity_regex = {
    'url' : r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',       # urls
    'IBAN' : r'\b[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})?\b',
    'Mentions': r'(?<!\w)@[\w.\-]+(?:@[\w\.\-]+\.\w+)?',                                           # including both normal and mastodon mentions
    'Hashtags': r'#\w+',                                                                           # hashtags
    # add other regex 
    }

    # Required arguments
    parser.add_argument(
        "--input_data", "-i",
        type=str,
        default="./data/input_data.txt",
        help="Path to the input file or directory."
    )

    parser.add_argument(
        "--regex_dict", "-r",
        type=str,
        help="Path to JSON file containing regex dictionary."
    )

    parser.add_argument(
        "--entity_types", "-et",
        type=str,
        default="url",
        help="List of entity types to anonymize separated by comma."
    )

    parser.add_argument(
        "--hash_func", "-hf",
        type=str,
        default="md5",
        help="Hash function to use (e.g., sha256, md5) defaults to md5."
    )

    # Optional arguments
    parser.add_argument(
        "--salt", "-s",
        action="store_true",
        help="Whether to salt the hashes."
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./output",
        help="Directory to save output files (default: ./output)."
    )

    args = parser.parse_args()

    # Load regex dictionary
    if not args.regex_dict:
        args.regex_dict = entity_regex
    else:
        with open(args.regex_dict, 'r') as f:
            args.regex_dict = json.load(f)

    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)

    return args


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def select_hash_func(hash_name: str):
    hash_name = hash_name.lower()  # Normalize input
    if hash_name in hashlib.algorithms_guaranteed:
        return getattr(hashlib, hash_name)
    else:
        raise ValueError(f"Unsupported hash function '{hash_name}'. "
                         f"Supported algorithms: {', '.join(sorted(hashlib.algorithms_guaranteed))}")


def hash_entity(input_data, 
                entity_regex, 
                entities_to_anonymize = ["url"], 
                hash_fn=hashlib.md5,
                salt=None):

    rel_regex = {k: v for k, v in entity_regex.items() if k in entities_to_anonymize}

    hashed_entities = []
    input_with_hashed_entities = []
    for post in input_data:
        _matched_entities = {entity_type: re.findall(regex,  post) \
                                for entity_type, regex in rel_regex.items()}
        
        for entity_type, matches in _matched_entities.items():
            for entity in matches:
                if entity_type == "url":
                    entity_f = entity[:40]
                    if salt:
                        entity_f += salt
                    try:
                        entity_e = urlsplit(entity_f).netloc
                    except:
                        entity_e = 'unknown'
                    net_loc = hash_fn(entity_e.encode()).hexdigest()
                    res = hash_fn(entity.encode()).hexdigest()
                    input_with_hashed_entities.append(post.replace(entity, "<hashed_{entity_type}><url_hash>"+ res +"</url_hash>" + "<pld_hash>"+ net_loc + "</pld_hash></hashed_{entity_type}>"))
                    hashed_entities.append("url:" + res + "\tdomain:" + net_loc)  
                # for other entities (non URL)
                else:
                    hash_entity = hash_fn(entity.encode()).hexdigest()
                    input_with_hashed_entities.append(post.replace(entity, f"<hashed_{entity_type}>{hash_entity}</hashed_{entity_type}>"))
                    hashed_entities.append(hash_entity)  
    df = pd.DataFrame({'hashed_posts': input_with_hashed_entities, 'hashed_entities': hashed_entities})
    return df          


def save_config(args):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    config_path = f"{args.output}/config/"
    ensure_dir(config_path)
    config_path += f"config_{timestamp}.json"
    # Convert args namespace to dict, excluding non-serializable objects
    args_dict = vars(args).copy()
    # regex_dict is already loaded as dict, keep as is

    with open(config_path, "w") as f:
        json.dump(args_dict, f, indent=4)

    print(f"Configuration saved to {config_path}")
    return timestamp


if __name__ == "__main__":
    args = parse_args()
    print("Parsed arguments:")
    print(args)
    timestamp = save_config(args)

    with open("data/input_data.txt", "r", encoding="utf-8") as file:
        posts = file.read().split('\n')

    hash_fn = select_hash_func(args.hash_func)

    df = hash_entity(input_data=posts, 
                     entity_regex=args.regex_dict, 
                     hash_fn=hash_fn, 
                     entities_to_anonymize=args.entity_types.split(","),
                     salt=timestamp if args.salt else None)
    output_path = f"{args.output}/data/"
    ensure_dir(output_path)
    df.to_csv(f"{output_path}/output_data_{timestamp}.tsv", sep = "\t", encoding = "utf-8")
