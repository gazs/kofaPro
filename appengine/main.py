#!/usr/bin/env python
# coding: utf8
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import urllib
import re
import time
import datetime
import models

def vajon_datum(d):
  if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", d):
    return True
  else:
    return False

def get_tegnap(datum):
  datum = datetime.datetime.strptime(datum, '%Y-%m-%d')
  t = models.Csapi.all().filter("datum <", datum).filter("datum >", datum-datetime.timedelta(days=7)).order("-datum").fetch(1)[0].datum
  return t

def get_helyek():
  properties = models.Csapi._properties
  helyek = []
  for property in properties:
    if property.endswith("_min"):
      helyek.append(property.replace("_min",""))
  return helyek

def chart(cim, napok, adatsorok):
  """
  cim: string
  napok: [datetime, datetime]
  adatsorok: [150,..]
  """
  napok.reverse()
  for adatsor in adatsorok:
    adatsor.reverse()
  hezag = 50
  mini = 0
  maxi = max([max(adatsor) for adatsor in adatsorok]) + hezag
  inapok = [str((napok[0]-nap).days) for nap in napok]

  adatsorok = [[str(adat) for adat in adatsor] for adatsor in adatsorok]
  napcimkek = [str(napok[i]) for i in range(0, len(napok), len(napok) / 7)]
  chd = []
  chds = [] 
  for adatsor in adatsorok:
    a = "|".join(( ",".join(inapok), ",".join(adatsor) ))
    chd.append(a)
    chds.append("0,{0},0,{1}".format(inapok[-1], maxi))
  params = {
    "chtt" : cim, 
    "cht"  : "lxy",
    "chs"  : "600x300",
    "chxt" : "x,y",
    "chg"  : "{0},{1}".format(7, ((100.0/maxi)*50) ),
    "chxr" : "0,{0},{1}|1,{2},{3}".format(inapok[0], inapok[-1], mini, maxi), # id, min, max
    "chxl" : "0:|" + "|".join(napcimkek),
    "chm": "o,FF9900,0,-1,5.0|o,FF9900,1,-1,5.0", 
    "chd"  : "t:" + "|".join(chd), 
    "chds" : ",".join(chds)
  }
  #params["chd"] = "t:" + "|".join(chd)
  return "http://chart.apis.google.com/chart?{0}".format(urllib.urlencode(params))

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("helloworld")

class QHandler(webapp.RequestHandler):
  def get(self):
    path = self.request.path.split("/")[2:]
    path = [urllib.unquote(x) for x in path]
    sorrend = []
    for part in path:
      if part in get_helyek():
        sorrend.append("hely")
      if vajon_datum(part):
        sorrend.append("datum")
      if part not in get_helyek() and not vajon_datum(part) and not re.match("\d", part) and part is not "":
        sorrend.append("aru")
    q = models.Csapi.all()
    q.order("-datum")
    limit = 50
    if "datum" in sorrend:
      datum = path[sorrend.index("datum")]
      q.filter("datum =", datetime.datetime.strptime(datum, '%Y-%m-%d'))
      z = models.Csapi.all().order("-datum").filter("datum = ", get_tegnap(datum))
    if "aru" in sorrend:
      aru = path[sorrend.index("aru")]
      q.filter("aru =", aru)
      try:
        z.filter("aru =", aru)
      except UnboundLocalError:
        pass
    r = []
    try:
      zs = z.fetch(limit)
    except UnboundLocalError:
      pass
    fecs = q.fetch(limit)
    for sor in fecs:
      a = {"datum":str(sor.datum), "aru":sor.aru}
      for property in sor.properties():
        if "hely" in sorrend:
          if property.startswith(path[sorrend.index("hely")]):
            a[property] = eval("sor.{0}".format(property))
        else: # akkor viszont mindegyik kell. kicsit redundáns így írni, de hogy jobb?
          a[property] = eval("sor.{0}".format(property))
        if property.endswith("_min"): # hackish, hogy adom hozzá szépen?
          #a[property.replace('_min', '') + "_tegnap"] = "X" 
      r.append(a)
    template_values = {
        "info": path, 
        "sorok" : r
        }
    oszlopok = []
    if "datum" not in sorrend:
      oszlopok.append("dátum")
    elif "datum" in sorrend:
      template_values["datum"] = True
    if "hely" not in sorrend:
      oszlopok += get_helyek()
    elif "hely" in sorrend:
      oszlopok.append(path[sorrend.index("hely")])
      template_values["hely"] = path[sorrend.index("hely")]
    if "aru" in sorrend:
      template_values["aru"] = True
      napok = [s["datum"] for s in r]
      adatsorok = []
      adatsorok.append([s["vamhazkrt_min"] for s in r])
      adatsorok.append([s["vamhazkrt_max"] for s in r])
      template_values["chart"] = chart(aru, napok, adatsorok)
    template_values["oszlopok"] = oszlopok
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path,template_values))

def main():
  application = webapp.WSGIApplication([
                                        ('/', MainHandler),
                                        ('/q/?.*', QHandler),
                                       ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
