import requests


project = "apache/openmeetings"
per_page = 100

base_url = "https://api.github.com/repos/"f"{project}" 
headers = {'Accept': 'application/json', 'Authorization': 'token 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'}

result = []

page = 1
while True:
    pulls = requests.get(base_url+ "/pulls?state=closed&per_page="f"{per_page}&page="f"{page}", headers=headers).json()
    for pull in pulls:
        ## TODO: If number of reviews get big a loop through pages should be added for the reviews as well
        reviews = requests.get(base_url + "/pulls/"f"{pull['number']}/reviews?state=closed&per_page="f"{per_page}", headers=headers).json()
        if reviews:
            for review in reviews:
                # Check that there is a natural language review that is done than a different user than the author of the pull request                
                if review['body'] and pull['user']['login'] != review['user']['login']:
                    ## TODO: Understand how to add code before and after the review
                    commit = requests.get(base_url + "/commits/"f"{review['commit_id']}", headers=headers).json()
                    print(commit)
                    result.append({'project': project, 'url': pull['url'], 'number': pull['number'], 'id': pull['id'], "body": review['body'], "commit": review['commit_id']})
                
    page+=1

    if len(pulls) < per_page:
        break

print(len(result))
print(result)
