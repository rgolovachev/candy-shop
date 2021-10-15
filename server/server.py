'''
Использование server.py:
Либо в терминале написать:
curl -X POST -d 'username=*имя*' -d 'item=*товар*' -d 'count=*количество*' http://127.0.0.1:8000/api/reserve
Либо в интерпретаторе питона написать:
import requests
res = requests.post('http://127.0.0.1:8000/api/reserve', data={'username':'*имя*', 'item':'*товар*', 'count':'*количество'})
print(res.text)

Чтобы посмотреть статистику надо зайти на сайт http://127.0.0.1:8000/api/stats

Все данные о покупках хрантся в userdata.yml
'''

from flask import Flask, make_response, request
import yaml

app = Flask(__name__)

data = yaml.safe_load(open('../data/data.yml', 'r'))
users = {}


@app.route("/api/reserve", methods=['POST'])
def reserve():
    user, item, cnt = request.form.get('username'), request.form.get('item'), int(request.form.get('count'))
    if not user:
        return 'залогинься'
    if not item:
        return 'выбери что будешь покупать'
    if not cnt:
        return 'выбери количество продукта'
    if cnt <= 0:
        return 'выбери нормальное количество продукта'
    if item not in data:
        return 'я такого не продаю'
    if cnt > data[item][1]:
        return 'у меня нет столько товара ' + item + ' в наличии(('
    print(user, item, cnt)
    data[item][1] -= cnt
    if user not in users:
        users[user] = dict()
    users[user][item] = users[user].get(item, 0) + cnt
    with open('../data/data.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
    with open('userdata.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(users, outfile, default_flow_style=False, allow_unicode=True)
    return 'ты успешно забронил ' + str(cnt) + ' товара:' + item


@app.route("/api/stats", methods=['GET'])
def stats():
    text = ''
    for key in users:
        text += '<p><font face="Courier New">Пользователь ' + key + '\n</font></p>'
        text += '<p style="margin-left: 50px;"><font face="Courier New">Забронил товары:\n</font></p>'
        for item in users[key]:
            text += '<p style="margin-left: 100px;"><font face="Courier New">' + item + ' в количестве ' + str(users[key][item]) + ' штук\n</font></p>'
    return text


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000', debug=True)