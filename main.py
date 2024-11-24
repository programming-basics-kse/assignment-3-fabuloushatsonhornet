import argparse
import csv
import pycountry
from pycountry import countries
from pyparsing import empty

parser = argparse.ArgumentParser('Olympic data base')
# parser.add_argument('input file', default='main.py')
parser.add_argument('data_base', type=str)
# parser.add_argument('-medals', type=str)
# parser.add_argument('-output', type=str, default='')
# parser.add_argument('-total', type=int)
parser.add_argument('-overall', nargs='+', type=str)
# parser.add_argument('-interactive', type=bool, default=False)
args = parser.parse_args()

def output_console(arg_country):
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
        command = input('Write a command (Exit - E/e)- ')
        while command.lower() not in ('e', 'exit'):
            self.validated = self.validation(command)
            if not self.validated:
                command = input('Write a command correctly (Exit - E/e)- ')
                continue


    def validation(self, com):
        lower_com = com.lower()
        if com not in commands:
            return False
        return lower_com

    def medals(self):
        pass
    def total(self):
        pass
    def overall(self):
        pass

commands = {
    'data_base': lambda: None,
    'overall': lambda: output_console(tuple(args.overall)),
    'interactive': InteractiveMode()
}
for arg in args.__dict__:
    commands[arg]()