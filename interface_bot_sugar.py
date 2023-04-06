import telebot
import config # импортируем config.py где хранится токен бота

bot = telebot.TeleBot(config.token)

feedstock = 0.0
margin = 0.0
grace_period = 0.0


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "Введите стоимость сахара(цена за 1 кг с НДС)")
    bot.register_next_step_handler(message, reg_feedstock)

def reg_feedstock(message):
    global feedstock
    feedstock = float(message.text)
    bot.send_message(message.from_user.id, "Введите маржу(в рублях на 1 кг)")
    bot.register_next_step_handler(message, reg_margin)

def reg_margin(message):
    global margin
    margin = float(message.text)
    bot.send_message(message.from_user.id, "Введите отсрочку платежа в днях")
    bot.register_next_step_handler(message, reg_grace_period)

def reg_grace_period(message):
    global grace_period
    grace_period = float(message.text)
    bot.register_next_step_handler(message, action)

@bot.message_handler(commands=['action'])
def action(message):
    calculation_sugar(feedstock, margin, grace_period)
    bot.send_document(message.chat.id, open('out.txt'))

def calculation_sugar(feedstock, margin, grace_period):
    logistics = {}
    packing_weight_1 = 1
    packing_weight_5 = 5

    with open('logist_data.txt') as log_data:
        for line in log_data:
            key, value = line.split()
            logistics[key] = int(value) / 20000
    with open('out.txt', 'w') as out:
        for key, value in logistics.items():
            # рассчитываем значение "финансирования", параметр используется для расчета стоимости
            financing = round(((feedstock + logistics[key] / 1.18 + 2.95) * 0.12 / 365 * grace_period), 2)
            # рассчитывает стоимость сахара весом 1 кг для каждого направления
            result_data = (financing + logistics[key] / 1.18 + feedstock / 1.1 * packing_weight_1 + 2.90 + margin) * 1.1
            # рассчитывает стоимость сахара весом 5 кг для каждого направления
            result_data2 = (financing + logistics[
                key] / 1.18 + feedstock / 1.1 + 2.65 + margin) * packing_weight_5 * 1.1
            # записываем результаты в файл
            out.write(f'{key}: {result_data:.2f}р. / {result_data2:.2f}р. \n')
        # строка разделитель
        out.write(f'------------------------ \n')
        # строка выводит входящую стоимость сахара, а также маржу
        out.write(f'вход: {feedstock}р., маржа: {margin}р. \n')
        out.write(f'------------------------ \n')

bot.infinity_polling()
