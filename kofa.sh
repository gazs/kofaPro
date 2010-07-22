#!/usr/bin/bash

# legfrissebb árlista a csapiról -> első nem-thumbnail kép a listán
# egy soron két találat van, <a href>fájlnév kiírva</a>; csak egyre van szükségünk
echo -n "Árlista letöltése... "
ARLISTA=$(curl -s "http://www.csapi.hu/parts/upload/arlistak/?M=D" | grep -o "[a-zA-Z0-9]*.jpg" -m 1 | head -n 1)

DATUM=$(date -d @$(echo $ARLISTA|sed 's/\.jpg//') +%F)

if [ -a arlistak/$DATUM.txt ] 
then
  echo "[ööö]"
  echo "! A legfrissebb árlistát ($DATUM) már feldolgoztuk."
  exit
fi

curl -s "http://csapi.hu/parts/upload/arlistak/$ARLISTA" -o arlista.jpg && echo "[ok]"

echo -n "kép előkészítése... "
# a tesseract egy kellően nagy TIFF fájlt vár.
convert arlista.jpg -depth 1 arlista.tif
# a rácsok teljesen összezavarják, úgyhogy kivonjuk az előkészített rácsokat a képből
composite -compose difference -negate racs.tif arlista.tif a.tif
# -- ha jól látom az is zavarja, ha fekete alapon fehér betűk vannak, fordítsuk hát vissza.
# és méretezzük át, hogy meglássa a betűket, egyúttal kicsit elmosva a betűk éleit, hogy *könnyítsük* a dolgát
# jameg 8-bit, hogy legyenek szürkék is, picit.
convert a.tif -depth 8 -resize 180% +negate nagy.tif && echo "[ok]"

echo -n "ocr... "
tesseract nagy.tif arlistak/$DATUM > /dev/null 2>&1 && echo "[ok]"

echo -e "\n"
cat arlistak/$DATUM.txt


rm arlista.jpg arlista.tif a.tif nagy.tif 
