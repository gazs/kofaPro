from google.appengine.ext import db

class Ar(db.Model):
  datum          = db.DateProperty()
  aru            = db.StringProperty()
  ar_vamhazkrt   = db.StringProperty()
  ar_fehervariut = db.StringProperty()
  ar_korhazutca  = db.StringProperty()
  ar_rakocziter  = db.StringProperty()
  ar_bosnyakter  = db.StringProperty()
