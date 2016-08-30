#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
from kfasta import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs):
        self.data = {}
        for pair in pairs:
            self.put(pair[0], pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        if self.data.has_key(k):
            self.data[k].append(v)
        else:
            self.data[k] = []
            self.data[k].append(v)
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if self.data.has_key(k):
            return self.data[k]
        else:
            result = []
            return result

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    subseq = ''
    count = 0
    h = RollingHash(subseq)
    try:
        while True:
            if count == 0:            
                while len(subseq) < k:
                    subseq += seq.next()
                h = RollingHash(subseq)
                yield (subseq, h.current_hash)
            else:
                next_char = seq.next()
                new_hash = h.slide(subseq[0], next_char)
                subseq = subseq[1:]
                subseq += next_char
                yield(subseq, new_hash)
            count += 1
    except StopIteration:
        return


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    raise Exception("Not implemented!")

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    raise Exception("Not implemented!")

#if __name__ == '__main__':
#    if len(sys.argv) != 4:
#        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
#        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
#   compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
la = subsequenceHashes(FastaSequence('data/fchimp0.fa'), 2)
dictionary = Multidict(la)
print("")
for na in la:
    dictionary.put(na[1], na[0])
print(dictionary.data)
print(dictionary.get('TA'))