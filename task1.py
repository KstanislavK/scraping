# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

import requests
import json

def get_rep(user):
    url = 'http://api.github.com/users/' + user + '/repos'
    return requests.get(url).json()

def create_file(path, repo):
    with open(path, 'w') as file:
        json.dump(repo, file, indent=2)

def repo_list(path):
    with open(path, 'r') as file:
        repos = json.load(file)
    return repos

if __name__ == "__main__":
    user = 'KstanislavK'
    file_name = 'repos_' + user + '.json'
    create_file(file_name, get_rep(user))
    print('List of ' + user + '\'s repos on GitHUB: ')
    for i in repo_list(file_name):
        print(i['name'])
