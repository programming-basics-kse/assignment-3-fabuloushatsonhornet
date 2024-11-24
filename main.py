import argparse

parser = argparse.ArgumentParser('Olympic data base')
parser.add_argument('data_base', type=str, default='Olympic Athletes - athlete_events.tsv')
parser.add_argument('-medals', type=str, nargs='+')
# # parser.add_argument('-output', type=str, default='')
parser.add_argument('-total', type=str, default=-1)
# # parser.add_argument('-overall', type=str)
# # parser.add_argument('-interactive', type=bool, default=False)
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
    value_l = len(value)
    if value_l == 0:
        return f"There wasn`t any olympic games in this year."
    elif value_l < 10:
        return f"Ths country got less than 10 medals."
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
                    if total is False:
                        filtered_data_list.append([data[0], data[1], data[6], data[7], data[8], data[9], data[13], data[14]])
                    if total is True:
                        filtered_data_list.append([data[6], data[14]])
            except IndexError:
                break
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
    if total is False:
        filtered_data_list = sorted(get_list(f"{data_base}", year), key=lambda x: int(x[0]), reverse=False)
        print_result(filtered_data_list)
    if total is True:
        filtered_data_list = get_list(f"{data_base}", year)
        print_result(filtered_data_list)
main()