# (Entities) Pseudo Anonymization

## Description
The pseudo anonymization method helps to anonymize different types of entities that may have privacy risks e.g., user mentions, or security risks e.g., URLs or identity risks e.g., hashtags.
For this, the method uses Regular Expressions (RegEx) that match patterns such as URLs, hashtags, IBANs, and more. 
Each recognized pattern is hashed with a configurable hashing function (A hashing function is an algorithm that can map any input to an unique irreversible hash-value). It offers a nice mechanism to anonymize sensitive information while preserving their referential integrity i.e., the same entity will always map to the same hash. 

The method scans the input data for predefined patterns relevant for anonmyzation. For the matched patterns that are found in the input text, the method uses current timestamp as 'salt' for each pattern, which increases the security of the anonymization against online available lookup tables. Finally, the matched and salted patterns are hashed using md5 hash function and are replaced with their hashed values.
This approach allows researchers to maintain the semantic and relational structure of the data (e.g., user mentions, domain references, or recurring tags) without exposing sensitive or personally identifiable information. 
Therefore, hashing-based anonymization mechanisms are particularly useful in privacy-preserving computational social science studies.

## Use Cases

Analyzing political discourse on Twitter hashing URLs and user mentions to study the interaction patterns and link-sharing behavior without exposing the identifiable informatin.

In analyzing highly explicit content e.g., for gender based studies on 4chan data, the offensive, racism, vulgar keywords can be hashed representing their nature and frequency without revealing the actual keywords. 

## Input Data

The method reads input data from [`data/input_data.txt`](data/input_data.txt) having social media posts per line.

| Input Data |
|:----------:|
| Just discovered the best coffee spot in town ☕ Check it out → https://example.com/coffee1 |
| When life gets blurry, adjust your focus 📸 https://example.com/focus |
| Can’t believe it’s already Friday again 😅 https://example.com/fridayvibes |
| AI is cool until it starts correcting your jokes 😂 https://example.com/ai |
| That moment when your code finally runs without errors 🎉 https://example.com/codewin |

## Output Data

The output data is written into [data/output_data.tsv](data/output_data.tsv) where the target entities are replaced with their hash in the input text, while also providing the hash as separate column.

| hashed_posts	| hashed_entities |
|:-------------:|:---------------:|
| Just discovered the best coffee spot in town ☕ Check it out → <hashed_url><url_hash>f3442bcf31cfdd30065901ff60d5927a</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_url>	| url:f3442bcf31cfdd30065901ff60d5927a domain:5ababd603b22780302dd8d83498e5172 |
|	When life gets blurry, adjust your focus 📸 <hashed_url><url_hash>77b3526cf5c25974e176acf187ad6734</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_url>	| url:77b3526cf5c25974e176acf187ad6734 domain:5ababd603b22780302dd8d83498e5172 |
|	Can’t believe it’s already Friday again 😅 <hashed_url><url_hash>0c235f77f6aa8ce10e838742faa5373e</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_url>	| url:0c235f77f6aa8ce10e838742faa5373e domain:5ababd603b22780302dd8d83498e5172 |
|	AI is cool until it starts correcting your jokes 😂 <hashed_url><url_hash>ca3dbccf917c0ecf35ce4b821e2a1789</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_url>	| url:ca3dbccf917c0ecf35ce4b821e2a1789 domain:5ababd603b22780302dd8d83498e5172 |
|	That moment when your code finally runs without errors 🎉 <hashed_url><url_hash>b77144869e3b53ce256778068d32e0a4</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_url>	| url:b77144869e3b53ce256778068d32e0a4 domain:5ababd603b22780302dd8d83498e5172 |
|	Long walks + good music = therapy 🚶‍♂️🎶 <hashed_url><url_hash>e66e778b0173f1c232aebcf9fa3898c1</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_url>	| url:e66e778b0173f1c232aebcf9fa3898c1 domain:5ababd603b22780302dd8d83498e5172 |

## Hardware Requirements

The method runs on a small virtual machine provided by a cloud computing company (2 x86 CPU cores, 4 GB RAM, 40 GB HDD).

## Environment Setup

Install dependencies, using

`conda env create -f environment.yml`

## How to Use

The method offers a CLI-tool that makes it easy to run and adapt the code to your current needs.

### Example Commands

#### 1) Anonymize url and Hashtags in tweets.txt file
```
python hash_entity.py -i ./data/tweets.txt -et url,Hashtags
```

#### 2) Using a custom regex dictionary that contain Mentions and IBAN regex
```
python hash_entity.py -i ./data/posts.txt -r ./config/custom_regex.json -et Mentions,IBAN
```

#### 3) Different hash function + salt, custom output dir
```
python hash_entity.py -i ./data/sample.txt -hf sha256 -s -o ./cleaned_output
```

### Parameter Overview
| Argument &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;    &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;   | Short | Type   | Default                 | Description                                                                                                            |
| ------------------ | ----- | ------ | ----------------------- | -------------------------------------------------------------------------- |
| `--input_data`     | `-i`  | `str`  | `./data/input_data.txt` | Path to input file or directory to process.                                                                            |
| `--regex_dict`     | `-r`  | `str`  | `None`                  | Path to a JSON file containing custom regex patterns. If not provided, defaults to built-in `entity_regex` dictionary. |
| `--entity_types`   | `-et` | `str`  | `"url"`                 | Comma-separated list of entity types to anonymize (e.g. `IBAN,Hashtags`).                                          |
| `--hash_func`      | `-hf` | `str`  | `"md5"`                 | Hashing algorithm to use (`md5`, `sha256`, etc.).                                                                      |
| `--salt`           | `-s`  | `flag` | `False`                 | If provided, enables salting of hashes for extra security.                                                             |
| `--output`         | `-o`  | `str`  | `./output`              | Directory path for saving processed output files.                                                                      |

## Contact

For further queries, please contact <stephan.linzbach@gesis.org>
