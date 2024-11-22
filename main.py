import argparse
import csv
import pycountry

parser = argparse.ArgumentParser('Olympic data base')
parser.add_argument('data_base', type=str, default='data_base_olympic.tsv')
parser.add_argument('-medals', type=str)
parser.add_argument('-output', type=str, default='')
parser.add_argument('-total', type=int)
parser.add_argument('-overall', type=str)
parser.add_argument('-interactive', type=bool, default=False)
args = parser.parse_args()

def get_country_code(country_n):
    for country in pycountry.countries:
        if country.name.lower() == country_n.lower():
            return country.alpha_3
    country = pycountry.countries.get(alpha_3=country_n)
    if country:
        return country_n.upper()

with open('data_base_olympic.tsv', 'r') as file:
    next_line = file.readline()
    header = next_line
    while next_line:
        next_line = file.readline()

    country_code = 'UKR'

    if country:
        print(f"Country: {country.name}")
    else:
        pass