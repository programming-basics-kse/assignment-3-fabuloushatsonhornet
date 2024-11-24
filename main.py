import argparse
import csv

parser = argparse.ArgumentParser('Olympic data base')
parser.add_argument('data_base', type=str, default='Olympic Athletes - athlete_events.tsv')
parser.add_argument('-medals', type=str)
# # parser.add_argument('-output', type=str, default='')
parser.add_argument('-total', type=int, default=-1)
# # parser.add_argument('-overall', type=str)
# # parser.add_argument('-interactive', type=bool, default=False)
args = parser.parse_args()
#
#
data_base = args.data_base
# country = args.country
'''if not args.total:
    year = args.total
    total = True
else:
    year = args.year
    total = False'''
year = args.total # Тут просто с тотала достаеться сразу год, Дефолтом Я тебя запутал, теперь если тотала нету то по умолчанию стоит -1, это для проверки можно юзать
# и аргумента со страной нету, это мой тупняк добавлять его, надо посмотреть откуда ты его должен доставать
# Temporary

def validation_number(value):
    try:
        value = float(value)
        return value
    except ValueError:
        return False

def get_medal_and_country(value, year):
        try:
            if total is False:
                if (value[14].lower().capitalize().strip() == 'Gold' or value[14].lower().capitalize().strip() == 'Silver' or value[14].lower().capitalize().strip() == 'Bronze') and (value[9] == year) and ((value[6].lower() == country.lower()) or (value[7].lower() == country.lower())):
                    value[14] = value[14][:-1]
                    return value
            if total is True:
                if (value[14].lower().capitalize().strip() == 'Gold' or value[14].lower().capitalize().strip() == 'Silver' or value[14].lower().capitalize().strip() == 'Bronze') and (value[9] == year):
                    value[14] = value[14][:-1]
                    return value
            return False
        except ValueError:
            return False



def condition_checker(value):
    if len(value) == 0:
        return f"There wasn`t any olympic games in this year."
    if len(value) < 10:
        return f"Ths country got less than 10 medals."
    else:
        return False


def get_list(filename, year):
    filtered_data_list = []
    with open(f"{filename}", 'r') as file:
        next_line = file.readline()
        while next_line:
            next_line = file.readline()
            data = next_line.split('\t')
            try:
                if get_medal_and_country(data, year):
                    filtered_data_list.append([data[0], data[1], data[6], data[7], data[8], data[9], data[13], data[14]])
            except IndexError:
                break
    return filtered_data_list

def print_result(data_list, country, year):
    if not condition_checker(data_list):
        index = 1
        print(f"Data for {year} olympic games. Team:{country}.")
        for data in data_list:
            name = data[1]
            discipline = data[6]
            medal = data[7]
            print(f"{index}. {name} - {discipline} - {medal}")
            index += 1
    else:
        print(condition_checker(data_list))

def main():
    filtered_data_list = sorted(get_list(f"{data_base}", year), key=lambda x: int(x[0]), reverse=False)
    print_result(filtered_data_list, country, year)
main()