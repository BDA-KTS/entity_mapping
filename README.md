# Entity Mapping

## Description
The entity mapping method anonymize identifiable entities in text—such as URLs, hashtags, mentions, and other structured patterns. It applies MD5 hashing to each instance of the target entity that is identified via regular expressions (regex). It scans the input data for predefined entity types, capturing all matching patterns using efficient regex rules. Each unique entity is then transformed into a consistent hash value using the MD5 algorithm, ensuring irreversible anonymization while preserving referential integrity i.e., the same entity will always map to the same hash. This approach allows researchers to maintain the semantic and relational structure of the data (e.g., user mentions, domain references, or recurring tags) without exposing sensitive or personally identifiable information. Such a hashing-based mapping mechanism is particularly useful in privacy-preserving computational social science studies.

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
| Just discovered the best coffee spot in town ☕ Check it out → <hashed_entity><url_hash>f3442bcf31cfdd30065901ff60d5927a</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_entity>	| res:f3442bcf31cfdd30065901ff60d5927a net_loc5ababd603b22780302dd8d83498e5172 |
|	When life gets blurry, adjust your focus 📸 <hashed_entity><url_hash>77b3526cf5c25974e176acf187ad6734</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_entity>	| res:77b3526cf5c25974e176acf187ad6734 net_loc5ababd603b22780302dd8d83498e5172 |
|	Can’t believe it’s already Friday again 😅 <hashed_entity><url_hash>0c235f77f6aa8ce10e838742faa5373e</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_entity>	| res:0c235f77f6aa8ce10e838742faa5373e net_loc5ababd603b22780302dd8d83498e5172 |
|	AI is cool until it starts correcting your jokes 😂 <hashed_entity><url_hash>ca3dbccf917c0ecf35ce4b821e2a1789</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_entity>	| res:ca3dbccf917c0ecf35ce4b821e2a1789 net_loc5ababd603b22780302dd8d83498e5172 |
|	That moment when your code finally runs without errors 🎉 <hashed_entity><url_hash>b77144869e3b53ce256778068d32e0a4</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_entity>	| res:b77144869e3b53ce256778068d32e0a4 net_loc5ababd603b22780302dd8d83498e5172 |
|	Long walks + good music = therapy 🚶‍♂️🎶 <hashed_entity><url_hash>e66e778b0173f1c232aebcf9fa3898c1</url_hash><pld_hash>5ababd603b22780302dd8d83498e5172</pld_hash></hashed_entity>	| res:e66e778b0173f1c232aebcf9fa3898c1 net_loc5ababd603b22780302dd8d83498e5172 |

## Hardware Requirements

The method runs on a small virtual machine provided by a cloud computing company (2 x86 CPU cores, 4 GB RAM, 40 GB HDD).

## Environment Setup

Install dependencies, using

`conda env create -f environment.yml`

## How to Use

The the method `hash_entity(input_data, entity_type = "url")` by providing input text as a list and choose  a predefined regex for the type of entity to hash. A sample call is provided in the same file as;

```
if __name__ == "__main__":
    with open("data/input_data.txt", "r", encoding="utf-8") as file:
        posts = file.read().split('\n')
    df = hash_entity(posts, "url")
    df.to_csv("data/output_data.tsv", sep = "\t", encoding = "utf-8")
```
For additional entities, update the `entity_regex` dictionary with newer entries.

## Contact

For further queries, please contact <stephan.linzbach@gesis.org>
