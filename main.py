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
def validation_medal(value, year):
    try:
        if (value[14].lower().capitalize().strip() == 'Gold' or value[14].lower().capitalize().strip() == 'Silver' or value[14].lower().capitalize().strip() == 'Bronze') and (data[9] == year) and:
            value[14] = value[14][:-1]
            return value
        return False
    except ValueError:
        return False

def sort_by_date(data):
    if data[9] == year:
        return data


year = '1998'
country = 'USA'

filtered_data_list = []

with open('Olympic Athletes - athlete_events.tsv', 'r') as file:
    next_line = file.readline()
    while next_line:
        next_line = file.readline()
        data = next_line.split('\t')
        try:
            if validation_medal(data, year):
                filtered_data_list.append(data)
        except IndexError:
            break
for data in filtered_data_list:
    print(data)