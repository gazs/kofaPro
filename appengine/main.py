#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


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
    # self.response.out.write("%s %s %s\n\n" % (termek, datum, helyszin))
    for result in results:
      if termek and datum and helyszin:
        self.response.out.write(arcsik(result))
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
          exec("self.response.out.write(result.ar_"+ helyszin +" + ',')")
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
