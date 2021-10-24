import os

import requests as requests

ACCESS_TOKEN = '*ENTER VK ACCESS TOKEN*'


def get_friends(user_id):
    resp = requests.get(
        'https://api.vk.com/method/friends.get?access_token={}&v=5.131&user_id={}'.format(ACCESS_TOKEN, user_id)).json()
    if 'error' in resp:
        return []
    return resp['response']['items']


def parse_friends(user_id):
    edge_list = []
    q = []
    q.extend(get_friends(user_id))
    while len(q) > 0:
        user_id = q[-1]
        q.pop(-1)
        friends = get_friends(user_id)
        for friend in friends:
            print('Processing', friend)
            s = {user_id, friend}
            if s not in edge_list:
                edge_list.append(s)
    return edge_list


def save_to_csv(user_id, egde_list):
    filename = 'users/' + user_id + '.csv'
    with open(filename, 'w') as csvfile:
        csvfile.write('Source,Target,Type,Weight\n')
        for edge in egde_list:
            current = list(map(str, list(edge)))
            csvfile.write(','.join([current[0], current[1], 'undirected', '1']) + '\n')


if __name__ == '__main__':
    user_id = input('Enter vk user_id:')
    # user_id = '230486741'
    if user_id + '.csv' not in os.listdir('users'):
        el = parse_friends(user_id)
        save_to_csv(user_id, el)
    else:
        print('User is already parsed. Check "users/{}"'.format(user_id + '.csv'))
