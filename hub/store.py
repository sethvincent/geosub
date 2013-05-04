import sqlite3
import json

class Store:
  """ Creates & maintains a location-filterable storage of items. """
  def __init__(self, db):
    if isinstance(db, str):
      db = sqlite3.connect(db)
    self.db = db;
    self.ensureSchema()

  def ensureSchema(self):
    sql = 'create table if not exists items (id INTEGER PRIMARY KEY AUTOINCREMENT, category integer, lat real, lon real, when integer, data BLOB)'
    self.db.execute(sql)
    sql = 'create table if not exists categories (id INTEGER PRIMARY KEY AUTOINCREMENT, label text)'
    self.db.execute(sql)

  def getItems(self, area, since):
    sql = 'select * from items where when > (?) and '
    values = (since, )
    areaInfo = [descriptor.toSql() for descriptor in area]
    sql += ' and '.join([itm[0] for itm in areaInfo])
    values += tuple([itm[1] for itm in areaInfo])

    c = self.db.cursor()
    c.execute(sql, values)
    return c
      

  def addItem(self, category, location, time, item):
    c = self.db.cursor()
    sql = 'insert into items values (?, ?, ?, ?, ?)'
    c.execute(sql, (category, location.lat, location.lon, time, json.dumps(item)))