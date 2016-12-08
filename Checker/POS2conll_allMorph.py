# -*- coding: utf-8 -*-

import csv

def main():
	"""
	Function to take (tagged) irish corpus and convert to CoNLL format
	This version extracts the lemma form of the word, additional POS info for some words and morphological features where available.
	"""
	#*****Input the file direction here that you want to input*******
        irishfile = open('irish1.txt.pos', 'r')
        
        #*****Name the output file here*********
	writer = csv.writer(open('test.txt.conll','w'), dialect=csv.excel_tab)

	
       # Some POS taglists vary. For example, Noun+Masc+Com+Sg+Ecl  vs Verb+VT+PastInd+Len
       # IN the case of nouns, there is no relevant fine-grained tag, so we just repeat the coarse grained tag in the 5th column.
       # The rest (listed below) have relevant fine-grained tags we can use in the 5th column
	masterPosList = ["Verbal", "Verb", "Prop", "Conj", "Adv", "Prep", "Part", "Pron"]
	sents = []

        for line in irishfile:
		# Each sentence is a string. Convert into list of words (tokens)
		sent = line.split()
		sents.append(sent)

	# counter for conll print out
	index = 1
        
        for sent in sents:
	    sentenceIndex = -1
	    for word in sent:
		 sentenceIndex = sentenceIndex + 1
                 if '+' in word:
			 # Punct+Fin indicates end of sentence. Restart counter and separate each sentence block with newline
			 if "Punct+Fin" in word:
				 EndWord = word.find('+')
				 word = word[0:EndWord]
				 writer.writerow((index,word,word, word, word, "_", "_", "punctuation", "_", "_"))
				 writer.writerow((""))
				 index = 1    # reset the index after each sentence

			 else:
                                 morphlist = word.split('+') 
				 # for example: word 'An' = is+Cop+Pres+Q+@COP_WH
				 lexword = morphlist[0]

				 # Pull out POS info from 2nd slot (as long as it wasn't a guessed result)
                                 if morphlist[1] != "Guess":
                                     realpos = morphlist[1]

				     # Get additional POS info. 
				     if realpos in masterPosList:
					 print morphlist[0], realpos    
				         posExtra = morphlist[2]
					 morphFeats = morphlist[3:]
					 
				     # Otherwise leave the same as POS slot. Some POS (e.g. Noun) only have coarse-grained POS
				     else:
				         posExtra = realpos

				         morphFeats = morphlist[2:]
                                 else:
                                 # Wagner+Guess+Prop+Noun+Masc+Com+Sg or Dialects+Guess+Foreign
                                     realpos = morphlist[2]
				     
				     if realpos in masterPosList:
				       	 posExtra = morphlist[3]
				     else:
					 posExtra = realpos
					 

				     morphFeats = morphlist[3:]
				 
				 feats = "+".join(morphFeats)

				 # Some words don't have features. Therefore, need to avoid deleting the _ in the feats column.
				 if feats == "":
					 feats = "_"

				 
				 # token is previous word
				 surfaceForm = sent[sentenceIndex-1]

				 # displaying lexical form. Can easily remove this for experiments later - but harder to reintroduce!
				 writer.writerow((index,surfaceForm,lexword, realpos, posExtra, feats, "_", "_", "_", "_"))
				 index = index + 1
				 

if __name__ == '__main__':
	main()
