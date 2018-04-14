import requests
import json


url = 'https://api.github.com/graphql'
api_token = 'a68f7ffae3ee31dd86209dcc5e56be49e9cd974a'
headers = {'Authorization': f'token {api_token}'}


def query(q):
    payload = { "query": q }
    r = requests.post(url=url, json=payload, headers=headers)
    data = json.loads(r.text)['data']
    return data


def author_rank(username):
    return rank_followers(followers) + rank_following(following)


def rank_followers(followers):
    return 0


def rank_following(following):
    return 0


def user_rank(user1,user2):
    queryBody = '''
        followers {
          totalCount
        }
        following {
          totalCount
        }
        issuesOpen:issues(states:OPEN) {
          totalCount
        }
        issuesClosed:issues(states:CLOSED) {
          totalCount
        }
        organizations {
          totalCount
        }
        pinnedRepositories(privacy:PUBLIC) {
          totalCount
        }
        pullOpen:pullRequests(states:OPEN) {
          totalCount
        }
        pullClosed:pullRequests(states:CLOSED) {
          totalCount
        }
        pullMerged:pullRequests(states:MERGED) {
          totalCount
        }
        repositories(privacy: PUBLIC) {
          totalCount
        }
        repositoriesContributedTo(privacy: PUBLIC) {
          totalCount
        }
        starredRepositories {
          totalCount
        }
        watching(privacy: PUBLIC) {
          totalCount
        }
        bio
        location
        company
        createdAt
        avatarUrl'''

    q = '''
    {
        user1:user(login: "%s"){
            %s
        },
        user2:user(login: "%s"){
            %s
        }
    }''' % (user1, queryBody, user2, queryBody)

    return parse_user_rank(query(q))


def repository_rank(user1, repo1, user2, repo2):
    queryBody = '''
        createdAt
        stargazers {
          totalCount
        }
        watchers {
          totalCount
        }
        forkCount
        refs(refPrefix: "refs/") {
          totalCount
        }
        master: ref(qualifiedName: "master") {
          commit: target {
            ... on Commit {
              history(first:0){
                totalCount
              }
            }
          }
        }
        pushedAt
        diskUsage
        deployments {
          totalCount
        }
        releases {
          totalCount
        }
        issuesOpen: issues(states: OPEN) {
          totalCount
        }
        issuesClosed: issues(states: CLOSED) {
          totalCount
        }
        pullOpen: pullRequests(states: OPEN) {
          totalCount
        }
        pullClosed: pullRequests(states: CLOSED) {
          totalCount
        }
        pullMerged: pullRequests(states: MERGED) {
          totalCount
        }
        mileOpen: milestones(states: OPEN) {
          totalCount
        }
        mileClosed: milestones(states: CLOSED) {
          totalCount
        }
        languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            node {
              name
            }
          }
        }
        isArchived
        isFork'''

    q = '''
    {
      repo1:repository(owner: "%s", name: "%s") {
        %s
      },
      repo2:repository(owner: "%s", name: "%s") {
        %s
      }
    }''' % (user1, repo1, queryBody, user2, repo2, queryBody)

    return parse_repo_rank(query(q))


# Function that parse the data from the users request to be easier to digest
def parse_user_rank(data):
    parsed_data = {
                    "user1":
                      {
                         "followers"  : data['user1']['followers']['totalCount'],
                         "following"  : data['user1']['following']['totalCount'],
                         "issuesOpen" : data['user1']['issuesOpen']['totalCount'],
                         "issuesClosed" : data['user1']['issuesClosed']['totalCount'],
                         "organizations" : data['user1']['organizations']['totalCount'],
                         "pinnedRepositories" : data['user1']['pinnedRepositories']['totalCount'],
                         "pullOpen" : data['user1']['pullOpen']['totalCount'],
                         "pullClosed" : data['user1']['pullClosed']['totalCount'],
                         "pullMerged" : data['user1']['pullMerged']['totalCount'],
                         "repositories" : data['user1']['repositories']['totalCount'],
                         "repositoriesContributedTo" :
                         data['user1']['repositoriesContributedTo']['totalCount'],
                         "starredRepositories" : data['user1']['starredRepositories']['totalCount'],
                         "watching" : data['user1']['watching']['totalCount'],
                         "bio" : data['user1']['bio'] != '',
                         "location" : data['user1']['location'] != None,
                         "company"  : data['user1']['company'] != "",
                         "createdAt": data['user1']['createdAt'],
                         "avatarUrl": data['user1']['avatarUrl']
                     },
                    "user2":
                      {
                         "followers"  : data['user2']['followers']['totalCount'],
                         "following"  : data['user2']['following']['totalCount'],
                         "issuesOpen" : data['user2']['issuesOpen']['totalCount'],
                         "issuesClosed" : data['user2']['issuesClosed']['totalCount'],
                         "organizations" : data['user2']['organizations']['totalCount'],
                         "pinnedRepositories" : data['user2']['pinnedRepositories']['totalCount'],
                         "pullOpen" : data['user2']['pullOpen']['totalCount'],
                         "pullClosed" : data['user2']['pullClosed']['totalCount'],
                         "pullMerged" : data['user2']['pullMerged']['totalCount'],
                         "repositories" : data['user2']['repositories']['totalCount'],
                         "repositoriesContributedTo" :
                         data['user2']['repositoriesContributedTo']['totalCount'],
                         "starredRepositories" : data['user2']['starredRepositories']['totalCount'],
                         "watching" : data['user2']['watching']['totalCount'],
                         "bio" : data['user2']['bio'] != '',
                         "location" : data['user2']['location'] != None,
                         "company"  : data['user2']['company'] != "",
                         "createdAt": data['user2']['createdAt'],
                         "avatarUrl": data['user2']['avatarUrl']
                     }
                  }

    return parsed_data


# Function that parse the data from the repositories request to be easier to digest
def parse_repo_rank(data):
    languages1 = {t['node']['name'] for t in data['repo1']['languages']['edges']}
    languages2 = {t['node']['name'] for t in data['repo2']['languages']['edges']}

    parsed_data = {
                    "repo1":
                      {
                          "createdAt" : data['repo1']['createdAt'],
                          "stargazers": data['repo1']['stargazers']['totalCount'],
                          "watchers" : data['repo1']['watchers']['totalCount'],
                          "forkCount": data['repo1']['forkCount'],
                          "refs" : data['repo1']['refs']['totalCount'],
                          "totalCommits" :
                          data['repo1']['master']['commit']['history']['totalCount'],
                          "pushedAt" : data['repo1']['pushedAt'],
                          "diskUsage" : data['repo1']['diskUsage'],
                          "deployments":  data['repo1']['deployments']['totalCount'],
                          "releases" :  data['repo1']['releases']['totalCount'],
                          "issuesOpen":  data['repo1']['issuesOpen']['totalCount'],
                          "issuesClosed": data['repo1']['issuesClosed']['totalCount'],
                          "pullOpen":  data['repo1']['pullOpen']['totalCount'],
                          "pullClosed": data['repo1']['pullClosed']['totalCount'],
                          "pullMerged": data['repo1']['pullMerged']['totalCount'],
                          "mileOpen": data['repo1']['mileOpen']['totalCount'],
                          "mileClosed": data['repo1']['mileClosed']['totalCount'],
                          "languages" : languages1,
                          "isArchived" : data['repo1']['isArchived'],
                          "isFork" : data['repo1']['isFork']
                     },
                    "repo2":
                      {
                          "createdAt" : data['repo2']['createdAt'],
                          "stargazers": data['repo2']['stargazers']['totalCount'],
                          "watchers" : data['repo2']['watchers']['totalCount'],
                          "forkCount": data['repo2']['forkCount'],
                          "refs" : data['repo2']['refs']['totalCount'],
                          "totalCommits" :
                          data['repo2']['master']['commit']['history']['totalCount'],
                          "pushedAt" : data['repo2']['pushedAt'],
                          "diskUsage" : data['repo2']['diskUsage'],
                          "deployments":  data['repo2']['deployments']['totalCount'],
                          "releases" :  data['repo2']['releases']['totalCount'],
                          "issuesOpen":  data['repo2']['issuesOpen']['totalCount'],
                          "issuesClosed": data['repo2']['issuesClosed']['totalCount'],
                          "pullOpen":  data['repo2']['pullOpen']['totalCount'],
                          "pullClosed": data['repo2']['pullClosed']['totalCount'],
                          "pullMerged": data['repo2']['pullMerged']['totalCount'],
                          "mileOpen": data['repo2']['mileOpen']['totalCount'],
                          "mileClosed": data['repo2']['mileClosed']['totalCount'],
                          "languages" : languages2,
                          "isArchived" : data['repo2']['isArchived'],
                          "isFork" : data['repo2']['isFork']
                     }
                  }

    return parsed_data


if __name__ == '__main__':
    print(repository_rank("faviouz", "cantina", "makeorbreak-io", "peimi"))
    #print()
    #print(user_rank("faviouz", "dedukun"))