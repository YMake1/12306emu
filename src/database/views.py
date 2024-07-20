import csv

from src.database.models import db, Station

def initdb(station):
    if station:
        try:
            with open('./public/source/stations.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                batch_size = 1000
                count = 0
                db.session.begin()
                for row in reader:
                    if row:
                        station_name = row[0]
                        station_city = row[1]
                        station = Station(name=station_name, city=station_city)
                        db.session.add(station)
                        count += 1
                        if count % batch_size == 0:
                            db.session.commit()
                            db.session.begin()
                db.session.commit()
        except:
            db.session.rollback()