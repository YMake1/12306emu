import csv

path = './public/source'

def stations_process(filename):
    with open(f'{path}/stations/stations.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Station Name', 'Station City'])
        with open(filename, 'r', encoding='utf-8') as f:
            block_size = 1024 * 8
            remainder = ''
            while True:
                chunk = f.read(block_size)
                if not chunk:
                    break
                chunk = remainder + chunk
                sections = chunk.split('|||')
                remainder = sections.pop()
                for section in sections:
                    fields = section.split('|')
                    station_name = fields[1]
                    station_city = fields[7]
                    writer.writerow([station_name, station_city])
            if remainder:
                fields = remainder.split('|')
                station_name = fields[1]
                station_city = fields[7]
                writer.writerow([station_name, station_city])

# stations_process(f'{path}/stations/stations.txt')
