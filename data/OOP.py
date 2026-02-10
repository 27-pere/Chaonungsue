import pandas as pd

class complete_list:
    def __init__(self, path, header=None):
        self.data = path
        self.header = header

    def read(self):
        with open(self.data, 'r') as f:
            data = [x.split(',') for x in f.readlines()]
            return data
    def printer(self):
        if self.header:
            a, b, c, d = self.header
            yield(f'{a:^10} {b:^15} {c:^20} {d:^20}')
        for i in self.read():
            yield f'{i[0]:^10} | {i[1]:^10} | {i[2]:^10} | {i[3]:^10}'

headers = ['title', 'category', 'tags', 'rating']

data_frame = complete_list('books.csv', header=headers).printer()

for record in data_frame:
    print(record)