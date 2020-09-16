import requests
import json

def gitHubPost(text, mode='markdown'):
	payload = {'text': text, 'mode':mode}
	r = requests.post('https://api.github.com/markdown', data=json.dumps(payload))
	if r.status_code == 200:
		return r.content
	else:
		return None
md = "# Hello World\n# Hello Dev"
html = str(gitHubPost(md).decode('utf-8'))
x = html.replace('\n', '')
print(x)
