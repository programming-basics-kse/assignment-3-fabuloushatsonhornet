import argparse
import csv
import pycountry
from pycountry import countries

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
    counter = 0
    for country in arg_country:
        country_code = Overall.get_country_code(country)
        if country_code == None:
            continue
        print(f"{country_code} - {Overall.overall(country_code)[0][0]} : {Overall.overall(country_code)[0][1]} medals")
        counter += 1

    if counter == 0:
        print("No information available...")


class Overall:
    def get_country_code(country_n):
        for country in pycountry.countries:
            if country.name.lower() == country_n.lower():
                return country.alpha_3
        country = pycountry.countries.get(alpha_3=country_n)
        if country:
            return country_n.upper()
        else:
            return None

    def overall(code):
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
                if code != line[i_country] or line[i_medal] == 'NA':
                    continue
                year = line[i_year]
                if year in country_stats:
                    country_stats[year] += 1
                else:
                    country_stats[year] = 1
        return sorted(country_stats.items(), key = lambda x: x[1], reverse = True)


args.overall = tuple(args.overall)
output_console(args.overall)