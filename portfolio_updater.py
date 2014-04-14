#!/usr/bin/python
# A small python script that pulls my repo summaries using the GitHub API
# 2014 Aleksi Blinnikka
import json, shutil, sys
from urllib.request import Request, urlopen

# Repos are ordered by latest push
REPOS_URL = "https://api.github.com/users/Morgus/repos?sort=pushed"

# HTML to generate for each project
HTML_STRING = """
        <h3>{0} - {1}</h3>
        <p><a href="{2}">{2}</a><br />
        {3}</p>"""

# Specifically get v3 API response
req = Request(REPOS_URL, headers={"Accept": "application/vnd.github.v3+json"})

try:
    received_bytes = urlopen(req).read()
except URLError:
    print("Couldn't download repository information.")
    sys.exit(0)

# The API sends JSON
repos = json.loads(received_bytes.decode("utf-8"))

with open("./github_projects.html", "w") as file:
    for repo in repos:
        if not repo["fork"]:
            file.write(HTML_STRING.format(
                            repo["name"], repo["pushed_at"][:4],
                            repo["html_url"], repo["description"])
                            )

# Combine the page
with open("./sivut/portfolio.html", "w") as portfolio:
    shutil.copyfileobj(open("./top.html","r"), portfolio)
    shutil.copyfileobj(open("./github_projects.html","r"), portfolio)
    shutil.copyfileobj(open("./bottom.html","r"), portfolio)
