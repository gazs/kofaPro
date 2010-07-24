from google.appengine.ext import db

class Ar(db.Model):
#  datum          = db.DateProperty()
  aru            = db.TextProperty()
  ar_vamhazkrt   = db.TextProperty()
  ar_fehervariut = db.TextProperty()
  ar_korhazutca  = db.TextProperty()
  ar_rakocziter  = db.TextProperty()
  ar_bosnyakter  = db.TextProperty()

