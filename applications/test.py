import requests

test_data = {
    'rows': [
        {
            'position': 1,
            'subject': "Блок чего-то 24ВЭВ",
            'count': 3,
            'price': 129000.00
        },
        {
            'position': 2,
            'subject': "Бензопила9",
            'count': 2,
            'price': 7501
        },
        {
            'position': 3,
            'subject': "шнур",
            'count': 9,
            'price': 48.4
        },

    ]
}


# ------------ ДЛЯ ТЕСТИРОВАНИЯ -------------------
def post_new_application(json_data):
    url = "http://192.168.0.11:5000/applications/stuff"
    response = requests.post(url, json=json_data)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)
# ------------ ДЛЯ ТЕСТИРОВАНИЯ -------------------


if __name__ == '__main__':
    post_new_application(test_data)
