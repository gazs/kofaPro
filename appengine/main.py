#!/usr/bin/env python
# coding: utf8
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import urllib
import re
import datetime
import models

def get_helyek():
  properties = models.Csapi._properties
  helyek = []
  for property in properties:
    if property.endswith("_min"):
      helyek.append(property.replace("_min",""))
  return helyek

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("helloworld")

class QHandler(webapp.RequestHandler):
  def get(self):
    path = self.request.path.split("/")[2:]
    try:
      extension = path[-1].split(".")[1]
    except IndexError:
      extension = "html"
    path = [urllib.unquote(x) for x in path]
    datum = hely = aru = None
    helyek = get_helyek()
    for i in path:
      if i in helyek: hely = i
      if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", i): datum = datetime.datetime.strptime(i, '%Y-%m-%d').date()
    dbg = ""
    if datum or aru or hely:
      limit = 50
      q = models.Csapi.all()
      if datum:
        q.filter('datum', datum)
      if aru:
        q.filter('aru', aru)
      sorok = q.fetch(limit)
      dbg = str(sorok)
    template_values = {
        'extension': extension,
        'path': path,
        'datum': datum,
        'hely': hely,
        'aru': aru,
        'headers': ["egy", "két", "há"],
        'rows': [[1,2,3],[4,5,6]]
        }
    if extension is "html":
      templatepath = os.path.join(os.path.dirname(__file__), 'templates/index.html')
      self.response.out.write(template.render(templatepath, template_values))
    else:
      self.response.out.write("plaintext,mi?")

def main():
  application = webapp.WSGIApplication([
                                        ('/', MainHandler),
                                        ('/q/?.*', QHandler),
                                       ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
