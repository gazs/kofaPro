unicharset_extractor csapi-regular.box csapi-bold.box csapi-bold-italic.box && 
tesseract csapi-regular.tif junk nobatch box.train.stderr &&
tesseract csapi-bold.tif junk nobatch box.train.stderr &&
tesseract csapi-bold-italic.tif junk nobatch box.train.stderr &&
mftraining csapi-regular.tr csapi-bold.tr csapi-bold-italic.tr && 
cntraining csapi-regular.tr csapi-bold.tr csapi-bold-italic.tr && 
wordlist2dawg frequent_words_list freq-dawg
wordlist2dawg words_list word-dawg
mv inttemp csapi.inttemp && 
mv pffmtable csapi.pffmtable && 
mv normproto csapi.normproto && 
mv unicharset csapi.unicharset && 
mv freq-dawg csapi.freq-dawg &&
mv word-dawg csapi.word-dawg
sudo cp csapi.inttemp csapi.pffmtable csapi.normproto csapi.unicharset csapi.freq-dawg csapi.word-dawg /usr/share/tesseract-ocr/tessdata/
sudo touch /usr/share/tesseract-ocr/tessdata/csapi.user-words
sudo cp /usr/share/tesseract-ocr/tessdata/eng.DangAmbigs /usr/share/tesseract-ocr/tessdata/csapi.DangAmbigs
