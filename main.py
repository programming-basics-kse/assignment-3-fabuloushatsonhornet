import argparse
import pycountry

parser = argparse.ArgumentParser('Olympic data base')
parser.add_argument('data_base', type=str, default='data_base_olympic.tsv')
parser.add_argument('-medals', type=str, nargs='+')
# parser.add_argument('-output', type=str, default='')
parser.add_argument('-total', type=str, default=-1)
parser.add_argument('-overall', nargs='+', type=str)
parser.add_argument('-interactive', type=bool, default=False)
args = parser.parse_args()
data_base = args.data_base

if args.total == -1:
    total = False
    year = args.medals[1]
    country = args.medals[0]
else:
    total = True
    year = args.total

def get_medal_and_country(value, year):
    if not (value[14].lower().capitalize().strip() in ('Gold', 'Silver', 'Bronze') and value[9] == year):
        return False
    if total is False:
        if country.lower() not in (value[6].lower(), value[7].lower()):
            return False
    value[14] = value[14][:-1]
    return value

def condition_checker(value):
    value_l = len(value)
    if value_l == 0:
        return f"There wasn`t any olympic games in this year."
    elif value_l < 10:
        return f"Ths country got less than 10 medals."
    return False

def get_list(filename, year):
    filtered_data_list = []
    with open(filename, 'r') as file:
        next_line = file.readline()
        while next_line != '':
            data = next_line.split('\t')
            if get_medal_and_country(data, year):
                if total is False:
                    filtered_data_list.append([data[0], data[1], data[6], data[7], data[8], data[9], data[13], data[14]])
                if total is True:
                    filtered_data_list.append([data[6], data[14]])
            next_line = file.readline()
    if total is False:
        return sorted(filtered_data_list, key=lambda x: int(x[0]), reverse=False)
    return filtered_data_list

def print_with_total(data_list):
    data_dict = {}
    for country, medal in data_list:
        if country not in data_dict:
            data_dict[country] = {'gold': 0, 'silver': 0, 'bronze': 0}
        data_dict[country][medal.lower()] += 1
    for country, medal in data_dict.items():
        print(f"{country} - gold:{medal['gold']} - silver:{medal['silver']} - bronze:{medal['bronze']}")

def print_without_total(data_list):
    index = 1
    print(f"Data for {year} olympic games. Team:{country}.")
    for data in data_list:
        name = data[1]
        discipline = data[6]
        medal = data[7]
        print(f"{index}. {name} - {discipline} - {medal}")
        index += 1

def print_result(data_list):
    if not condition_checker(data_list):
        if total is False:
            print_without_total(data_list)
        if total is True:
            print_with_total(data_list)
    else:
        print(condition_checker(data_list))

def main():
    filtered_data_list = get_list(data_base, year)
    print_result(filtered_data_list)


def output_overall(arg_country):
    if arg_country is None:
        return
    for country in arg_country:
        country_o = Overall(country)
        if -1 == country_o.code:
            continue
        print(f"{country_o.code} - {country_o.top_y} : {country_o.top_m} medals")

class Overall:
    def __init__(self, country):
        self.code = self.get_country_code(country)
        if -1 != self.overall():
            self.top_y = self.overall()[0][0]
            self.top_m = self.overall()[0][1]

    def get_country_code(self, country_n):
        for country in pycountry.countries:
            if country.name.lower() == country_n.lower():
                return country.alpha_3
        country = pycountry.countries.get(alpha_3=country_n)
        if country:
            return country_n.upper()
        else:
            return -1

    def overall(self):
        with open(args.data_base, 'r') as file:
            line = file.readline()[:-1].split('\t')
            header = line #створив на всякий випадок, якщо доведеться діставати індекси
            i_year = 9
            i_medal = -1
            i_country = 7
            country_stats = {}
            while True:
                line = file.readline()[:-1].split('\t')
                if line == ['']:
                    break
                if self.code != line[i_country] or line[i_medal] == 'NA':
                    continue
                year = line[i_year]
                if year in country_stats:
                    country_stats[year] += 1
                else:
                    country_stats[year] = 1
        if country_stats == {}:
            return -1
        return sorted(country_stats.items(), key = lambda x: x[1], reverse = True)

class InteractiveMode:
    def __init__(self):
        # commands_i = {
        #     'medals': lambda: self.medals(),
        #     'total': lambda: self.total(),
        #     'overall': lambda: self.overall()
        # }
        country_i = input('Write a country (Exit - E/e)- ')
        while country_i.lower() not in ('e', 'exit'):
            self.validated = Overall.get_country_code(country_i)
            if self.validated == -1:
                country_i = input('Write a contry correctly (Exit - E/e)- ')
                continue
            # commands_i[self.validated]()

            country_i = input('Write a country (Exit - E/e)- ')

    def validation(self, com):
        lower_com = com.lower()
        if com not in commands:
            return False
        return lower_com

    def first_game(self):
        pass
    def best_game(self):
        pass
    def worst_game(self):
        countries = input('Write countries with comma separated - ').split(',')
        output_overall(tuple(countries))

print(args.__dict__)
commands = {
    'data_base': lambda: None,
    'medals': lambda: main(),
    'total': lambda: main(),
    'overall': lambda: output_overall(args.overall),
    'interactive': lambda: InteractiveMode()
}
for arg in args.__dict__:
    commands[arg]()