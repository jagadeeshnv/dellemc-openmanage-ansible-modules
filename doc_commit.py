import base64
import tempfile
import os
import requests
import urllib3
from mycreds import gitpat
import subprocess
from pprint import pprint

def get_files_from_commit(commit):
    files = []
    print(commit.get('commit').get('message'))
    # print(commit.get('url'))
    file_resp = requests.get(f"{commit.get('url')}", headers=headers, verify=False)
    file_cont = file_resp.json()
    # pprint(file_cont)
    for f in file_cont.get('files'):
        # print(f.get('filename'))
        files.append(f.get('filename'))
    return files


def download_the_files(modules, branch_name):
    tmp_dir = tempfile.mkdtemp()
    print(tmp_dir)
    temp_docs_dir = f"{tmp_dir}/docs"
    os.mkdir(temp_docs_dir)
    for mod in modules:
        mod_url = f"{repo_url}/contents/{mod}"
        mod_resp = requests.get(mod_url, params={'ref': branch_name},  headers=headers, verify=False)
        mod_cont = mod_resp.json()
        decoded_data = base64.b64decode(mod_cont.get('content')).decode('utf-8')
        fpath = f"{tmp_dir}/{mod.split('/')[-1]}"
        with open(fpath, 'w') as f:
            f.write(decoded_data)
        result = subprocess.run(["ansible-doc-extractor", temp_docs_dir, fpath], capture_output=True, text=True)
        print(result.stdout)
    files = os.listdir(temp_docs_dir)
    full_paths = []
    for file in files:
        file_path = os.path.join(temp_docs_dir, file)
        if os.path.isfile(file_path):
            full_paths.append(file_path)
    return full_paths

urllib3.disable_warnings()
headers = {'Authorization': 'bearer {}'.format(gitpat),
        'Accept': 'application/vnd.github+json'}

repo_url = 'https://api.github.com/repos/jagadeeshnv/dellemc-openmanage-ansible-modules'

tag_url = f"{repo_url}/commits"
# tag_url = 'https://api.github.com/repos/jagadeeshnv/dellemc-openmanage-ansible-modules/branches/poc/doc_commit'
branch_name = 'poc/doc_commit'

response = requests.get(tag_url, params={'sha': branch_name} ,headers=headers, verify=False)
content_data = response.json()
# pprint(content_data)
# for commit in content_data:
#     files = get_files_from_commit(commit)
#     print(files)
files = get_files_from_commit(content_data[0])
pprint(files)
modified_modules = []
for f in files:
    if f.startswith('plugins/modules/') and f.endswith('.py'):
        modified_modules.append(f)

rst_full_paths = download_the_files(modified_modules, branch_name)


# import requests

# # Set the URL of the GitHub repository
# url = "https://api.github.com/repos/{username}/{repository}/contents/{filename}"

# # Set the username and repository name
# username = "your-username"
# repository = "your-repository"

# # Set the filename
# filename = "README.md"

# # Set the branch name
# branch_name = "main"

# # Set the commit message
# commit_message = "My commit message"

# # Set the authentication token
# auth_token = "your-auth-token"

# # Read the contents of the file
# with open(filename, "r") as file:
#     file_contents = file.read()

# # Base64 encode the file contents
# base64_contents = base64.b64encode(file_contents.encode("utf-8")).decode("utf-8")

# # Set the commit data
# commit_data = {
#     "message": commit_message,
#     "content": base64_contents,
#     "branch": branch_name
# }


# # Make the GET request to get the current file data
# response = requests.get(url, auth=(auth_token, ""))

# # Check the response status code
# if response.status_code == 200:
#     # Get the SHA of the current file data
#     current_data = response.json()
#     current_sha = current_data["sha"]

#     # Set the SHA of the current file data in the commit data
#     commit_data["sha"] = current_sha

#     # Make the PUT request to update the file
#     response = requests.put(url, json=commit_data, auth=(auth_token, ""))

#     # Check the response status code
#     if response.status_code == 200:
#         print("File updated and committed successfully!")
#     else:
#         print("Failed to update and commit file:", response.text)
# else:
#     print("Failed to get current file data:", response.text)
