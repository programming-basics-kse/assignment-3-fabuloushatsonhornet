import argparse
import csv

# parser = argparse.ArgumentParser('Olympic data base')
# # parser.add_argument('data_base', type=str, default='data_base_olympic.tsv')
# parser.add_argument('medals', type=str)
# parser.add_argument('country', type=str)
# parser.add_argument('year', type=int)
# # parser.add_argument('-output', type=str, default='')
# # parser.add_argument('-total', type=int)
# # parser.add_argument('-overall', type=str)
# # parser.add_argument('-interactive', type=bool, default=False)
# args = parser.parse_args()
#
#
# medals = args.medals
# country = args.country
# year = args.year

# Temporary

def validation_number(value):
    try:
        value = float(value)
        return value
    except ValueError:
        return False

def get_medal_and_country(value, year):
    try:
        if (value[14].lower().capitalize().strip() == 'Gold' or value[14].lower().capitalize().strip() == 'Silver' or value[14].lower().capitalize().strip() == 'Bronze') and (value[9] == year) and ((value[6].lower() == country.lower()) or (value[7].lower() == country.lower())):
            value[14] = value[14][:-1]
            return value
        return False
    except ValueError:
        return False


def condition_checker(value):
    if len(value) == 0:
        return f"There was not any olympic games in this year."
    if len(value) < 10:
        return f"Ths country got less than 10 medals."
    else:
        return False


def get_list(filename, year):
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

year = '1998'
country = 'USA'

filtered_data_list = []
get_list('Olympic Athletes - athlete_events.tsv', year)

filtered_data_list = sorted(filtered_data_list, key=lambda x: int(x[0]), reverse=False)


print_result(filtered_data_list, country, year)