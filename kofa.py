#!/usr/bin/python
# coding=utf-8

import Image
import ImageChops
import StringIO
import tesseract
import urllib2
from BeautifulSoup import BeautifulSoup
import re

def download(url):
  f = urllib2.urlopen(url)
  data = f.read()
  f.close()
  return data

def get_arlistak():
  data = download('http://www.csapi.hu/parts/upload/arlistak/')
  soup = BeautifulSoup(data)
  hrefs = ["http://csapi.hu/parts/upload/arlistak/" + x['href'] for x in soup.findAll('a', href=re.compile("^\d{10}\.jpg"))]
  return hrefs

def threshold(i):
  if i > 125: return 255
  else: return 0

def arlista_darabol(img):
  width, height = img.size
  for sor in xrange(2, 100*width + 2, width): # keressük meg az első sort, ahol a legszélén van fekete
    if img.getdata()[sor] is 0:
      vizsgalt_sor = sor/width + 1 # az ezutáni sor alapján fogjuk vizsgálni, hol vannak az oszlophatárok
      #print vizsgalt_sor
      break
  jobbszelek = []
  for pixel in xrange( vizsgalt_sor * width, vizsgalt_sor * width + width): # oszlophatár: az itt átmenő vonalak mentén vágjuk ketté.
    if img.getdata()[pixel] is 0:
      jobbszelek.append(pixel % width )
  balszelek = [0] + jobbszelek
  oszlopok = zip(balszelek,jobbszelek)
  arlista_oszlopok = [img.crop((x[0],vizsgalt_sor,x[1],height)) for x in oszlopok]
  for csik in arlista_oszlopok:
    csik.show()
  return arlista_oszlopok

def process_arlista(href):
  img = Image.open(StringIO.StringIO(download(href)))
  img = img.point(threshold)
  img = img.convert("1")
  csikok = arlista_darabol(img) 
  ize = []
  for csik in csikok:
    csik = csik.resize((csik.size[0] *2, csik.size[1]*2), Image.NEAREST)
    kesz_darab =  tesseract.image_to_string(csik, lang='csapi').split("\n")
    print kesz_darab
    #print len(kesz_darab)
    ize.append(kesz_darab)
  kesz_arlista = zip(*ize)
  #for sor in kesz_arlista:
    #print sor

def main():
  process_arlista(get_arlistak()[0])

if __name__ == '__main__':
  main()
