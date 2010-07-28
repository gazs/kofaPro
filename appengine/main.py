#!/usr/bin/env python
# coding: utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from models import *
from termekek import termekek
import urllib
import re
import datetime 

def arcsik(result):
  arak = []
  for property in result.properties():
    if property.startswith("ar_"):
      arak.append( eval("result." + property) )
  return ",".join(arak)


class Api(webapp.RequestHandler):
  def get(self):
    path = self.request.path.split("/")[2:]
    path = [urllib.unquote(x) for x in path]
    termek = datum = helyszin = None

    piacok = ["korhazutca", "rakocziter", "fehervariut", "vamhazkrt", "bosnyakter"]
    for i in path:
      if i in termekek: termek = i
      if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", i): datum = i
      if i in piacok: helyszin = i

    # QUERY
    query = Ar.all()
    if termek:
      query.filter('aru =', termek)
    if datum:
      query.filter('datum =', datetime.datetime.strptime(datum, '%Y-%m-%d'))
    results = query.fetch(50)
    # MEGJELENÍTÉS
    self.response.headers["Content-Type"] = "text/plain"
   # self.response.out.write("%s %s %s\n" % (termek, datum, helyszin))
    for result in results:
      #refaktor!!!
      if termek and datum and helyszin:
        self.response.out.write( eval("result.ar_" +helyszin))
      elif not termek and datum and helyszin:
        self.response.out.write(result.aru+",")
        self.response.out.write(arcsik(result))
      elif termek and datum and not helyszin:
        self.response.out.write(arcsik(result))
      elif termek and not datum and helyszin:
        self.response.out.write(str(result.datum) + ",")
        self.response.out.write(arcsik(result))
      elif termek and not datum and not helyszin:
        self.response.out.write(str(result.datum) + ",")
        self.response.out.write(arcsik(result))
      elif not termek and datum and not helyszin:
        self.response.out.write(result.aru+",")
        self.response.out.write(arcsik(result))
      elif not termek and not datum and helyszin:
        self.response.out.write(result.aru+"," + str(result.datum) +",")
        for helyszin in piacok:
          self.response.out.write( eval("result.ar_" + helyszin)  )
      elif not termek and not datum and not helyszin:
        pass
      self.response.out.write("\n")
class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write('Hello world!')


def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/q/?.*', Api) 
                                       ],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
