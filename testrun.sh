#!/usr/bin/env bash

cd tomita
cat ../article.txt | ./tomita config.proto 1>../out.xml
