#!/bin/bash
# loop through all files in directory and process all 
# 1. tokenize input text
# 2. flookup morphological analysis
# 3. convert to required CG i/p format
# 4. vislcg3  disambiguation
# elaine oct 2012

cat $1 | iconv -f UTF-8 -t ISO-8859-1 | tr -sc "[:alnum:][:punct:]ÁÉÍÓÚáéíóú" "[\n*]" | iconv -f ISO-8859-1 -t UTF-8 | flookup -a bin/lexguess.fst | perl dis/lookup2cg3.prl | vislcg3 -g dis/gael-dis.rle > $1.fst
