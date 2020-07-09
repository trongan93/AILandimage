import pandas as pd
import csv
inputf = '../input_281_560.csv'

data = pd.read_csv(inputf)
print(len(data))

with open(inputf, 'r') as f:
    input_csv = csv.DictReader(f, delimiter=',')
    inputs = list(input_csv)

print(len(inputs))