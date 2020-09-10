
sample = 'today is a good day'

for word in sample.split(' '):
    if word[-3:] == 'day':
        print(word)

print('this appends to file if exists')
