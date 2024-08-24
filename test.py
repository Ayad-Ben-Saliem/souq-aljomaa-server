import os
import requests


def get_token():
    result = ''
    if os.path.exists('token.jwt'):
        with open('token.jwt', 'r') as f:
            result = f.read()
    return result


def login(username: str, password: str):
    response = requests.post(
        'http://localhost:5000/login',
        json={
            'username': username,
            'password': password,
        }
    )

    print('Login Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()


    if response.status_code == 200:
        with open('token.jwt', 'w') as f:
            f.write(response.json().get('access_token'))


def auto_login():
    response = requests.post(
        'http://localhost:5000/auto_login',
        headers={'Authorization': f'Bearer {get_token()}'}
    )

    print('Auto Login Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    if response.status_code == 200:
        with open('token.jwt', 'w') as f:
            f.write(response.json().get('access_token'))


def logout() :
    response = requests.post(
        'http://localhost:5000/logout',
        headers={'Authorization': f'Bearer {get_token()}'},
    )

    print('Logout Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    if response.status_code == 200:
        if os.path.exists('token.jwt'):
            os.remove('token.jwt')


def get_models(modelsIds: dict[str, list[int]] = None) -> requests.Response:
    if not modelsIds:
        modelsIds = {
                'Model1': [1, 2, 3],
                'Model2': [4, 5, 6],
                'Model3': [7, 8, 9],
            }
    response = requests.get(
        'http://localhost:5000/models',
        headers={'Authorization': f'Bearer {get_token()}'},
        json={'modelsIds': modelsIds}
    )

    print('Get Models Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    return response


def search(search_text: str, limit: int = 10, offset: int = 0) -> requests.Response:
    response = requests.get(
        'http://localhost:5000/search',
        headers={'Authorization': f'Bearer {get_token()}'},
        params={'search_text': search_text, 'limit': limit, 'offset': offset}
    )

    print('Search Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    return response


def create_user(data: dict[str, any] = None) -> requests.Response:
    if not data:
        data = {
            'name': 'Admin',
            'username': 'admin',
            'password': '1234',
        }
    response = requests.post(
        'http://localhost:5000/users',
        headers={'Authorization': f'Bearer {get_token()}'},
        json=data
    )
    
    print('Create User Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    return response



def get_user(id: int) -> requests.Response:
    response = requests.get(
        f'http://localhost:5000/users/{id}',
        headers={'Authorization': f'Bearer {get_token()}'},
    )
    
    print('Get User Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    return response


def get_users(ids: list[int] = None) -> requests.Response:
    response = requests.get(
        'http://localhost:5000/users',
        headers={'Authorization': f'Bearer {get_token()}'},
        json={'ids': ids}
    )
    
    print('Get Users Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    return response


def update_user(id: int = None, data: dict[str, any] = None) -> requests.Response:
    if id is None: id = 1

    if data is None:
        data = {
            'name': 'Admin',
            'username': 'admin',
            'password': '1234',
        }
    
    response = requests.put(
        f'http://localhost:5000/users/{id}',
        headers={'Authorization': f'Bearer {get_token()}'},
        json=data
    )
    
    print('Update User Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    return response


def delete_user(id: int) -> requests.Response:
    response = requests.delete(
        f'http://localhost:5000/users/{id}',
        headers={'Authorization': f'Bearer {get_token()}'}
    )
    
    print('Delete User Test ', end='')
    if 300 > response.status_code >= 200:
        print('Passed.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    else:
        print('Fails.')
        print(f'StatusCode ({response.status_code})')
        print(response.json())
    print()

    return response


if __name__ == '__main__':
    login(username='admin', password='1234')
    auto_login()
    # logout()
    get_models()
    search(search_text='123')
    create_user(
        data={
            'name': 'Ayad Ben',
            'username': 'ayad',
            'password': '1234',
        }
    )
    get_user(1)
    get_users(ids=[])
    update_user()
    delete_user(2)