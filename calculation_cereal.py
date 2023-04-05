def calculation_cereal(margin, grace_period, packing_weight):
    
    price_cereal = {}
    logistics = {}
    
    with open('price_data.txt') as p_data:
        for line in p_data:
            key, value = line.split()
            price_cereal[key] = float(value)
    with open('logist_data.txt') as l_data:
        for line in l_data:
            k, v = line.split()
            logistics[k] = float(v)
    
    with open('out.txt', 'w') as out:

        for k, v in logistics.items():
            out.write(f'                         \n')
            out.write(f'{k}:\n')
            out.write(f'------------------------ \n')
            for key,value in price_cereal.items():
       # рассчитываем значение "финансирования", параметр используется для расчета стоимости
                financing = round(((price_cereal[key] + logistics[k] / 20000 + 2.95) * 0.12 / 365 * grace_period), 2)
       # рассчитывает стоимость крупы заданного веса
                result_data = ((financing + logistics[k]/20000 / 1.18 + price_cereal[key] / 1.1) * packing_weight + 3.00 + margin) * 1.1 

                out.write(f'{key}: {result_data:.2f}р.\n')                   

calculation_cereal(float(input('Введите маржу(формат: 1.0): ')), float(input('Введите отсрочку платежа(формат: 1.0): ')), float(input('Введите вес фасовки в кг(формат: 0.9): ')))
