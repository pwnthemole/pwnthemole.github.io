import os
import re
import yaml

POSTS_PATH = "../_posts"
TAGS_PATH = "../tags"
tags = []

for post in os.listdir(POSTS_PATH):
    content = open(os.path.join(POSTS_PATH, post), "r").read()
    match = re.search("^---[\s\S]+?---", content)
    if match:
        fmatter = dict(list(yaml.safe_load_all(match.group()))[0])
        if "tags" in fmatter:
            if isinstance(fmatter["tags"], list):
                tags += (fmatter["tags"])
            else:
                tags += (fmatter["tags"].split())


for tag in tags:
    if not os.path.isfile(os.path.join(TAGS_PATH, tag + ".html")):
        f = open(os.path.join(TAGS_PATH, tag + ".html"), "w")
        f.write("---\nlayout: tag\nsection-type: tag\ntitle: {}\n---\n## Tag".format(tag))
        f.close()
