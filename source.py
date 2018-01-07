import requests
import json
import telebot

bot = telebot.TeleBot('399404158:AAHJ1NZnFFWDNkqPEEnrkB-KdKGEmV1Nogo')
token = "4255d1c7a587af987de363d795416419"
login = '79058333879'

s = requests.Session()
s.headers['authorization'] = 'Bearer ' + token


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("Баланс", "Последняя транзакция", "/start")
    bot.send_message(message.from_user.id, 'Добро пожаловать..', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Баланс':
        h = s.get('https://edge.qiwi.com/funding-sources/v1/accounts/current')
         ecoded = json.loads(h.text)
        bot.send_message(message.from_user.id, 'Баланс: ' + str(decoded['accounts'][0]['balance']['amount']))


    if message.text == 'Последняя транзакция':
        parameters = {'rows': '10', 'operation': 'IN'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + login + '/payments', params=parameters)
        decoded = json.loads(h.text)
        print(decoded)
        parameters1 = {'type': decoded['data'][0]['type']}
        ID = decoded['data'][0]['txnId']
        h1 = s.get("https://edge.qiwi.com/payment-history/v1/transactions/" + str(ID), params=parameters1)
        decoded = json.loads(h1.text)
        bot.send_message(message.from_user.id, 'Статус: ' + str(decoded['status']) + ' Сумма: ' + str(
            decoded['sum']['amount']) + ' Тип: ' + str(decoded['type']) + ' Комментарий: ' + str(decoded['comment']))


bot.polling(none_stop=True, interval=0)
