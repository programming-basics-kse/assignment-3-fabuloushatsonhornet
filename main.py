import argparse
import pycountry

parser = argparse.ArgumentParser('Olympic data base')
parser.add_argument('data_base', type=str, default='data_base_olympic.tsv')
parser.add_argument('-medals', type=str, nargs='+')
parser.add_argument('-output', type=str, default=False)
parser.add_argument('-total', type=str, default=-1)
parser.add_argument('-overall', nargs='+', type=str)
parser.add_argument('-interactive', type=bool, default=False)
args = parser.parse_args()
data_base = args.data_base

def output(valid):
    if valid:
        pass

def main():
    object = OlympicDataBase(args.medals, args.total)
    if args.total != -1 and args.medals is not None:
        filtered_data_list = object.get_list()
        object.print_result(filtered_data_list)

class OlympicDataBase:
    def __init__(self, medals=None, total=-1):
        self.data_base = data_base
        if total != -1:
            self.total = True
            self.year = total
            self.country = None
        elif medals is not None:
            self.total = False
            self.year = medals[1]
            self.country = medals[0]

    def get_medal_and_country(self, value):
        if not (value[14].lower().capitalize().strip() in ('Gold', 'Silver', 'Bronze') and value[9] == self.year):
            return False
        if not self.total and self.country.lower() not in (value[6].lower(), value[7].lower()):
            return False
        value[14] = value[14][:-1]
        return value

    def condition_checker(self, value):
        value_l = len(value)
        if value_l == 0:
            return f"There wasn`t any olympic games in this year."
        elif value_l < 10:
            return f"Ths country got less than 10 medals."
        return False

    def get_list(self):
        filtered_data_list = []
        with open(self.data_base, 'r') as file:
            next_line = file.readline()
            while next_line != '':
                data = next_line.split('\t')
                if self.get_medal_and_country(data):
                    if not self.total:
                        filtered_data_list.append([data[0], data[1], data[6], data[7], data[8], data[9], data[13], data[14]])
                    else:
                        filtered_data_list.append([data[6], data[14]])
                next_line = file.readline()

        if not self.total:
            return sorted(filtered_data_list, key=lambda x: int(x[0]), reverse=False)
        return filtered_data_list

    def print_with_total(self, data_list):
        data_dict = {}
        for country, medal in data_list:
            if country not in data_dict:
                data_dict[country] = {'gold': 0, 'silver': 0, 'bronze': 0}
            data_dict[country][medal.lower()] += 1
        for country, medal in data_dict.items():
            print(f"{country} - gold:{medal['gold']} - silver:{medal['silver']} - bronze:{medal['bronze']}")

    def print_without_total(self, data_list):
        index = 1
        print(f"Data for {self.year} olympic games. Team:{self.country}.")
        for data in data_list:
            name = data[1]
            discipline = data[6]
            medal = data[7]
            print(f"{index}. {name} - {discipline} - {medal}")
            index += 1

    def print_result(self, data_list):
        condition = self.condition_checker(data_list)
        if not condition:
            if not self.total:
                self.print_without_total(data_list)
            else:
                self.print_with_total(data_list)
        else:
            print(condition)

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
            # header = line #створив на всякий випадок, якщо доведеться діставати індекси
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
        self.data_base = data_base
        country_i = input('Write a country (Exit - E/e)- ')
        while country_i.lower() not in ('e', 'exit'):
            self.validated = self.validation_country(country_i)
            if self.validated == -1:
                country_i = input('Write a contry correctly (Exit - E/e)- ')
                continue
            # commands_i[self.validated]()
            with open(self.data_base, 'r') as file:
                line = file.readline()[:-1].split('\t')
                while line != '':
                    line = file.readline()[:-1].split('\t')
                    i_country = 7
                    i_year = 9
                    i_place = 11
                    first_game = [self.validated, 100000]
                    self.first_game(line, i_country, i_year, i_place, first_game)
                    # self.best_game(line, i_country, i_year)
                    # self.worst_game(line, i_country, i_year)

            country_i = input('Write a country (Exit - E/e)- ')

    def validation(self, com):
        lower_com = com.lower()
        if com not in commands:
            return False
        return lower_com

    def first_game(self, line, con, year, place, fir_game):
        if line[con] == self.validated and line[year] < fir_game[1]:
            fir_game[0:2] = place, year
    def best_game(self, line, con, year):
        pass
    def worst_game(self, line, con, year):
        pass

    def validation_country(self, country_n):
        for country in pycountry.countries:
            if country.name.lower() == country_n.lower():
                return country.alpha_3
        country = pycountry.countries.get(alpha_3=country_n)
        if country:
            return country_n.upper()
        else:
            return -1

print(args.__dict__)
commands = {
    'data_base': lambda: None,
    'medals': lambda: main(),
    'total': lambda: main(),
    'overall': lambda: output_overall(args.overall),
    'interactive': lambda: InteractiveMode(),
    'output': lambda: output(args.output)
}
for arg in args.__dict__:
    commands[arg]()