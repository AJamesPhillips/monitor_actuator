"""
Manually copy this onto the node.
Parse the data by running this file.
Then delete this file
"""

with open('./temperature.log-to-recover', 'r') as log_file:
    with open('./recovered-temp-data', 'a') as output:
        for (i, line) in enumerate(log_file):
            if (i % 1000 == 0):
                print('recovering data from line: {}'.format(i))
            if (line.startswith('data: ')):
                output.write(line.replace('data: ', ''))
