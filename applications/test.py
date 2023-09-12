import requests
import random

subjects = ['автомо', 'house', 'book', 'sofa', 'plane', 'gift', 'oskar', 'PC',
            'notebook', 'paper', 'router', 'pen', 'TV', 'phone', 'job',
            'lamp', 'cat', 'dog', 'eggs', 'test_item', 'milk', 'coffee']


def generete_data(subjects):
    test_data = {
        'rows': [
            {
                'position': 1,
                'subject': random.choice(subjects),
                'count': random.randint(1, 10),
                'price': random.randint(50, 100000) + random.randint(0, 99) * 0.01
            },
            {
                'position': 2,
                'subject': random.choice(subjects),
                'count': random.randint(1, 10),
                'price': random.randint(50, 100000) + random.randint(0, 99) * 0.01
            },
            {
                'position': 3,
                'subject': random.choice(subjects),
                'count': random.randint(1, 10),
                'price': random.randint(50, 100000) + random.randint(0, 99) * 0.01
            },

        ]
    }
    return test_data


test_row = {
        'rows': [
            {
                'position': 1,
                'subject': 'стул',
                'count': 3,
                'price': 5000.0
            },
            {
                'position': 2,
                'subject': 'дверь',
                'count': 1,
                'price': 7000.0
            },
            {
                'position': 3,
                'subject': 'окно',
                'count': 4,
                'price': 12000.0
            },

        ]
    }
test_money = {
    'is_report_not_need': False,
    'subject': 'Car',
    'amount': 34000.40
}
test_money1 = {
    'is_report_not_need': False,
    'subject': 'Bus',
    'amount': 5550000.40
}
test_money2 = {
    'is_report_not_need': False,
    'subject': 'House',
    'amount': 90349444.40
}
test_money3 = {
    'is_report_not_need': False,
    'subject': 'Chair',
    'amount': 900.40
}


def post_new_application(json_data):
    url = "http://192.168.0.10:5000/applications/stuff"
    response = requests.post(url, json=json_data)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)


def put_application(json_data):
    str_id = '4953029b-0c6a-4f61-9ae0-4da2f6043dce'
    url = "http://192.168.0.11:5000/applications/stuff/" + str_id
    response = requests.put(url, json=json_data)

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code, response.text)


def patch_application():
    str_id = '4953029b-0c6a-4f61-9ae0-4da2f6043dce'
    url = "http://192.168.0.11:5000/applications/stuff/" + str_id
    response = requests.patch(url)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)


def delete_application():
    str_id = '4953029b-0c6a-4f61-9ae0-4da2f6043dce'
    url = "http://192.168.0.11:5000/applications/stuff/" + str_id
    response = requests.delete(url)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)


def post_money(json_data):
    url = "http://192.168.0.11:5000/applications/money"
    response = requests.post(url, json=json_data)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)


def put_money_by_id(json_data):
    str_id = '5d05c792-9c8d-458f-b2ff-67c1aae28367'
    url = "http://192.168.0.11:5000/applications/money/" + str_id
    response = requests.put(url, json=json_data)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)


if __name__ == '__main__':
    post_new_application(test_row)
