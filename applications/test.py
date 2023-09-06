import requests

test_data = {
    'rows': [
        {
            'position': 1,
            'subject': "TV",
            'count': 3,
            'price': 50400
        },
        {
            'position': 2,
            'subject': "SomeThing",
            'count': 2,
            'price': 12090
        },
        {
            'position': 3,
            'subject': "omg",
            'count': 9,
            'price': 458
        },

    ]
}

test_money = {
    'is_report_not_need': False,
    'subject': 'Car',
    'amount': 34000.40
}


def post_new_application(json_data):
    url = "http://192.168.0.11:5000/applications/stuff"
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
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)


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


if __name__ == '__main__':
    post_money(test_money)
