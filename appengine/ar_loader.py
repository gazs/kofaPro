import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models

class ArLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Ar',
        [('aru', lambda x: x.decode('utf-8')),
          ('ar_vamhazkrt', lambda x: x.decode('utf-8')),
          ('ar_fehervariut', lambda x: x.decode('utf-8')),
          ('ar_korhazutca', lambda x: x.decode('utf-8')),
          ('ar_rakocziter', lambda x: x.decode('utf-8')),
          ('ar_bosnyakter', lambda x: x.decode('utf-8'))
          ])

loaders = [ArLoader]
