import requests
from gh_conf import GitHubApiConf
import json
import base64


project = "apache/openmeetings"
per_page = 100
commits = []

base_url = "https://api.github.com/repos/"f"{project}" 

pull_86 = requests.get(base_url + "/pulls/86", headers=GitHubApiConf.GITHUB_API_HEADER).json()
pull_86_user = pull_86['user']['login']
print(pull_86_user)

info = []
comments_86 = requests.get(base_url + "/pulls/86/comments", headers=GitHubApiConf.GITHUB_API_HEADER).json()

for id, comment in enumerate(comments_86):
    if comment['user']['login'] != pull_86_user:
        # TODO: Understand if is the code before or adter the changes
        original_content_file = base64.b64decode(requests.get(base_url + "/contents/"f"{comment['path']}?ref="f"{comment['original_commit_id']}", headers=GitHubApiConf.GITHUB_API_HEADER).json()['content'])
        info.append({'original_content': original_content_file, 'comment': comment['body'], 'diff_hunk': comment['diff_hunk'], 'file': comment['path']})


print(info)


"""
file_while = requests.get("https://api.github.com/repos/apache/openmeetings/pulls/56/commits", headers=GitHubApiConf.GITHUB_API_HEADER).json()[0]
print(file_while)
"""

"""
result = []

page = 1
while True:
    pulls = requests.get(base_url+ "/pulls?state=closed&per_page="f"{per_page}&page="f"{page}", headers=GitHubApiConf.GITHUB_API_HEADER).json()
    for pull in pulls:
        print(pull)
        ## TODO: If number of reviews get big a loop through pages should be added for the reviews as well
        reviews = requests.get(base_url + "/pulls/"f"{pull['number']}/reviews?state=closed&per_page="f"{per_page}", headers=GitHubApiConf.GITHUB_API_HEADER).json()
        if reviews:
            for review in reviews:
                # Check that there is a natural language review that is done than a different user than the author of the pull request                
                if review['body'] and pull['user']['login'] != review['user']['login']:
                    ## TODO: Understand how to add code before and after the review
                    print(review)
                    commit = requests.get(base_url + "/commits/"f"{review['commit_id']}", headers=GitHubApiConf.GITHUB_API_HEADER).json()
                    print(commit)
                    result.append({'project': project, 'url': pull['url'], 'number': pull['number'], 'id': pull['id'], "body": review['body'], "commit": review['commit_id']})
                
    page+=1

    if len(pulls) < per_page:
        break

print(len(result))
print(result)
"""