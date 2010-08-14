import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models

def numornone(x):
  try:
    return int(x)
  except ValueError:
    return None

class CsapiLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Csapi',
        [('datum', lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date()),
          ('aru', lambda x: x.decode('utf-8')),
          ('vamhazkrt_min',   numornone),
          ('vamhazkrt_med',   numornone),
          ('vamhazkrt_max',   numornone),
          ('vamhazkrt_msg',   lambda x: x.decode('utf-8')),
          ('fehervariut_min', numornone),
          ('fehervariut_med', numornone),
          ('fehervariut_max', numornone),
          ('fehervariut_msg', lambda x: x.decode('utf-8')),
          ('korhazutca_min',  numornone),
          ('korhazutca_med',  numornone),
          ('korhazutca_max',  numornone),
          ('korhazutca_msg',  lambda x: x.decode('utf-8')),
          ('rakocziter_min',  numornone),
          ('rakocziter_med',  numornone),
          ('rakocziter_max',  numornone),
          ('rakocziter_msg',  lambda x: x.decode('utf-8')),
          ('bosnyakter_min',   numornone),
          ('bosnyakter_med',   numornone),
          ('bosnyakter_max',   numornone),
          ('bosnyakter_msg',   lambda x: x.decode('utf-8')),
          ])

loaders = [CsapiLoader]
