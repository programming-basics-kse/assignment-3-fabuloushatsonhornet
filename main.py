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
    return country_stats


countries_overall = {}
args.overall = tuple(args.overall)
for country in args.overall:
    country_code = get_country_code(country)
    print(country_code)
    print(overall(country_code))
    # countries_overall[country_code] = {'year':None, 'count':0}