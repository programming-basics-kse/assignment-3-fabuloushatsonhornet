import argparse

parser = argparse.ArgumentParser('Olympic data base')
parser.add_argument('data_base', type=str, default='data.csv')
parser.add_argument('-medals', type=str)
parser.add_argument('-output', type=str, default='output.txt')
parser.add_argument('-total', type=int)
parser.add_argument('-overall', type=str)
parser.add_argument('-interactive', type=bool, default=False)
args = parser.parse_args()