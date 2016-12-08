#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import re

# Get text, replicate with "FIN" at the end of every line"

#Changed from LINEBREAK to FIN

def FIN(myfile):
    myfile = myfile
    infile = open(myfile)
    outfile = open(myfile+'.line', 'w')

    linein = infile.readline()
    while linein:
        outfile.write(linein.strip()+" FIN\n")
        linein = infile.readline()

# Normal POS identifier output text goes in,
# normal corpus-y text file with POS instead of tokens comes out
def posCorpus(myfile):    
    infile = open(myfile)
    outfile = open(myfile[:-8]+'pos','w')

    linein = infile.readline()
    newline = " "
    
    tok = re.compile(ur"<(.+)>")
    while linein:
        # Look for next token
        if '"<' in linein:
            # Token! Is it special?

            # Special tokens: don't just write
            if '"<FIN>"' in linein:
                # Add FIN to newline, write it,
                # and start building a new one.
                outfile.write(newline.strip()+'\n')
                newline = " "
            elif '"<&amp;>"' in linein: 
                newline = newline+' &amp;|Conj' #' &amp;'
            elif '"<&apos;>"' in linein:
                newline = newline+' &apos;|Punct' #' &apos;'
            elif '"<&quot;>"' in linein:
                newline = newline+' &quot;|Punct' #' &quot;'
            elif '"<&lt;>"' in linein:
                newline = newline+' &lt;|Punct'
            elif '"<&gt;>"' in linein:
                newline = newline+' &gt;|Punct'
            
            # Normal tokens: write their POS
            else:
                word = re.search(tok, linein).group(1)
                # Go to next line
                info = infile.readline()
                info = re.sub('\"', '', info.rstrip())
                toks = info.split()
                #if line contains guess - take second tag instead
                if "Guess" in info:
                  newline = newline + ' ' + word + " " + toks[0] + '+' + toks[2]+' '
                #verbal noun
                elif "Verbal" in info:
                  newline = newline + ' ' + word + " " + toks[0] + '+' + toks[1]  + "+" + toks[2]+' '
                else:
                  endline = "+".join(toks[0:])
                  newline = newline + " "+ word +" "+ endline

        linein = infile.readline()

def main():
    name = sys.argv[1]

    # 1) Add FIN
    print "Adding FIN..."
    FIN(name)


    # 2) Tag input
    current = name + '.line'
    print "Running the irishfst pipeline..."
    subprocess.call(['sh', '/home/apertium/Desktop/Tagger/Checker/runfst.sh', current])

    # 3) Get the POS-format corpus
    print "Putting together the POS version..."
    current = name + '.line.fst'
    posCorpus(current)

    print "Done!"
    print "Finished file: {a}.pos".format(a=name)

if __name__ == '__main__':
	main()