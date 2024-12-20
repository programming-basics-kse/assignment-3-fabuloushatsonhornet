import argparse
import pycountry

parser = argparse.ArgumentParser('Olympic data base')
parser.add_argument('data_base', type=str, default='data_base_olympic.tsv')
parser.add_argument('-medals', type=str, nargs='+')
parser.add_argument('-output', type=str, default=None)
parser.add_argument('-total', type=str, default=-1)
parser.add_argument('-overall', nargs='+', type=str)
parser.add_argument('-interactive', type=str, default=False)
args = parser.parse_args()
data_base = args.data_base
counter_main = [0]

def output(valid, out):
    print(out)
    if valid is not None:
        with open(valid, 'a') as f:
            f.write(out + '\n\n')

def main():
    if counter_main[0] == 0:
        object = OlympicDataBase(args.medals, args.total)
        if args.total != -1 or args.medals is not None:
            filtered_data_list = object.get_list()
            object.print_result(filtered_data_list)
    counter_main[0] += 1

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
            output(args.output, f"{country} - gold:{medal['gold']} - silver:{medal['silver']} - bronze:{medal['bronze']}")

    def print_without_total(self, data_list):
        index = 1
        output_ = f"Data for {self.year} olympic games. Team:{self.country}.\n"
        for data in data_list:
            name = data[1]
            discipline = data[6]
            medal = data[7]
            output_ += f"{index}. {name} - {discipline} - {medal}\n"
            index += 1
        output(args.output, output_)

    def print_result(self, data_list):
        condition = self.condition_checker(data_list)
        if not condition:
            if not self.total:
                self.print_without_total(data_list)
            else:
                self.print_with_total(data_list)
        else:
            output(args.output, condition)

def output_overall(arg_country):
    output_ = ''
    if arg_country is None:
        return
    for country in arg_country:
        country_o = Overall(country)
        if -1 == country_o.code:
            continue
        output_ += f"{country_o.code} - {country_o.top_y} : {country_o.top_m} medals\n"
    output(args.output, output_)

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
        if not args.interactive:
            return
        self.data_base = data_base
        country_i = input('Write a country (Exit - E/e)- ')
        while country_i.lower() not in ('e', 'exit'):
            self.validated = self.validation_country(country_i)
            if self.validated == -1:
                country_i = input('Write a contry correctly (Exit - E/e)- ')
                continue
            # commands_i[self.validated]()
            with open(self.data_base, 'r') as file:
                file.readline()
                line = file.readline()[:-1].split('\t')
                self.first_game_l = [self.validated, 100000]
                self.best_game_l = {}
                self.average_game_d = {}

                while line != ['']:
                    i_country = 7
                    i_year = 9
                    i_place = 11
                    i_medal = -1

                    COUNTRY = line[i_country]
                    YEAR = int(line[i_year])
                    PLACE = line[i_place]
                    MEDAL = line[i_medal]

                    test = self.first_game(COUNTRY, YEAR, PLACE, self.first_game_l[1])
                    if test is not None:
                        self.first_game_l = test
                    self.best_game(COUNTRY, MEDAL, YEAR, self.best_game_l)
                    self.average_game(COUNTRY, MEDAL, YEAR, self.average_game_d)


                    line = file.readline()[:-1].split('\t')
                self.worst_game_l = sorted(self.best_game_l.items(), key=lambda x: x[1], reverse=False)[0]
                self.best_game_l = sorted(self.best_game_l.items(), key=lambda x: x[1], reverse=True)[0]
                average_gold = 0
                average_silver = 0
                average_bronze = 0
                dict_len = len(self.average_game_d)
                for year_m in self.average_game_d.items():
                    average_gold += year_m[1]['gold']
                    average_silver += year_m[1]['gold']
                    average_bronze += year_m[1]['bronze']
                self.average_game_l = {'gold': average_gold / dict_len, 'silver': average_silver / dict_len, 'bronze': average_bronze / dict_len}
                self.output_ = ''
                self.output_ += f"City:{self.first_game_l[0]} year:{self.first_game_l[1]}\n"
                self.output_ += f"Best year medals: {self.best_game_l[1]}\n"
                self.output_ += f"Worst year medals: {self.worst_game_l[1]}\n"
                self.output_ += f"Average year medals, gold: {self.average_game_l['gold']}; silver: {self.average_game_l['silver']}; bronze: {self.average_game_l['bronze']}"
                output(args.output, self.output_)
            country_i = input('Write a country (Exit - E/e)- ')

    def validation(self, com):
        lower_com = com.lower()
        if com not in commands:
            return False
        return lower_com

    def first_game(self, con, year, place, fir_game):
        if con == self.validated and year < fir_game:
            return place, year
    def best_game(self, con, medal, year, dict_):
        if con != self.validated or medal == 'NA':
            return
        if year in dict_:
            dict_[year] += 1
        else:
            dict_[year] = 1
        if dict_ == {}:
            return
    def average_game(self, con, medal, year, dict_):
        if con != self.validated:
            return
        if year not in dict_:
            dict_[year] = {'gold': 0, 'silver': 0, 'bronze': 0}
        if len(medal) > 3:
            dict_[year][medal.lower()] += 1

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
    'output': lambda: None
}
for arg in args.__dict__:
    commands[arg]()