#!/usr/bin/env bash

#putin
cat ruwiki-20140306-pages-articles1.xml | head -n 616052 | tail -n 1095 > putin.txt
#fradkov
cat ruwiki-20140306-pages-articles1.xml | head -n 408328 | tail -n 175 > fradkov.txt
#vasiliev
cat ruwiki-20140306-pages-articles1.xml | head -n 2435077 | tail -n 98 > vasiliev.txt
#zotov
cat ruwiki-20140306-pages-articles1.xml | head -n 4813967 | tail -n 63 > zotov.txt
