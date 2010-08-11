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

  sortetejek = []
  for sor in xrange(2, height*width, width): # sorhatár: fekete csík / fekete pötty ott ahol nem szokott lenni
    if img.getdata()[sor] is 0:
      sortetejek.append(sor/width)
  soraljak = sortetejek[1:]
  sorok = zip(sortetejek, soraljak)
  arlista_sorok = [img.crop((0,teteje,width,alja)) for teteje, alja in sorok]
  kockak = []
  for sor in arlista_sorok:
    width, height = sor.size
    balszelek = [0]
    for i in xrange((height-1)*width, height*width):
      if sor.getdata()[i] is 0:
        balszelek.append(i - (height-1)*width)
    jobbszelek = balszelek[1:]
    oszlopok =  zip(balszelek, jobbszelek)
    kockak.append([sor.crop((bal,0,jobb, height)) for bal, jobb in oszlopok])
  return kockak

def process_arlista(href):
  img = Image.open(StringIO.StringIO(download(href)))
  img = img.point(threshold)
  img = img.convert("1")
  csikok = arlista_darabol(img) 
  for csik in csikok:
    for kocka in csik:
      kocka = kocka.resize((kocka.size[0]*2, kocka.size[1]*2), Image.NEAREST)
      print tesseract.image_to_string(kocka, lang='csapi').replace("@", "").replace("$","")

def main():
  process_arlista(get_arlistak()[0])

if __name__ == '__main__':
  main()
