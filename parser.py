import csv

output = {}

with open('congress.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        output[row[0]] = row[1].replace(u'\xa0', u' ')

print(output)

print(output['Maria Cantl'])