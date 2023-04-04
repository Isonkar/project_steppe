''' Скрипт выполняет расчет стоимости сахара в фасовки 1 кг и 5 кг для заданной географии поставкок.
    Условия поставки(стоимость логистики) содержится в файле logist_data.txt, вывод информации - выгрузка в файл.
    Данные в файл добавляются, т.е. он не затирается'''


def calculation(feedstock, margin, grace_period):

    logistics = {}
    packing_weight_1 = 1
    packing_weight_5 = 5

    with open('logist_data.txt') as log_data:
        for line in log_data:
            key, value = line.split()
            logistics[key] = int(value) / 20000

    with open('out.txt', 'a') as out:
        for key,value in logistics.items():
      # рассчитываем значение "финансирования", параметр используется для расчета стоимости
            financing = round(((feedstock + logistics[key] / 1.18 + 2.95) * 0.12 / 365 * grace_period), 2)
      # рассчитывает стоимость сахара весом 1 кг для каждого направления
            result_data = (financing + logistics[key] / 1.18 + feedstock / 1.1 * packing_weight_1 + 2.90 + margin) * 1.1 
      # рассчитывает стоимость сахара весом 5 кг для каждого направления
            result_data2 = (financing + logistics[key] / 1.18 + feedstock / 1.1 + 2.65 + margin) * packing_weight_5 * 1.1
      # записываем результаты в файл
            out.write(f'{key}: {result_data:.2f}р. / {result_data2:.2f}р. \n')
      # строка разделитель
        out.write(f'------------------------ \n')
      # строка выводит входящую стоимость сахара, а также маржу
        out.write(f'вход: {feedstock}р., маржа: {margin}р. \n')
        out.write(f'------------------------ \n')


calculation(float(input('Введите стоимость сырья: ')), float(input('Введите маржу: ')), float(input('Введите отсрочку платежа в днях: ')))
