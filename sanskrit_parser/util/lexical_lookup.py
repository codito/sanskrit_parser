'''
Base class + factory for lexical lookup classes

@author: avinashvarna
'''

from __future__ import print_function
import abc
import os
import inspect
from argparse import ArgumentParser
from sanskrit_parser.base.SanskritBase import SanskritObject, SLP1, SCHEMES
import logging

class LexicalLookup(object):
    
    __metaclass__  = abc.ABCMeta
    
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    folder = "data"
    base_dir = os.path.join(base_dir, folder)
    
    @abc.abstractmethod
    def valid(self, word):
        """ Return True if word is a valid pada """
        
    @abc.abstractmethod
    def get_tags(self, word):
        """ Return lexical tags of word """

    @staticmethod
    def getArgs():
        """
          Argparse routine. 
          Returns args variable
        """
        # Parser Setup
        parser = ArgumentParser(description='Interface to INRIA XML database')
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding', type=str, default=None)
        parser.add_argument('--loglevel', type=str, default="info",
                            help="logging level. Can be any level supported by logging module")

        parser.add_argument('word', nargs = '?', type=str, 
                            default=None, 
                            help="Word to look up")

        return parser.parse_args()
    
    def main(self, args):
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]
            
        word_in = SanskritObject(args.word, encoding=ie).transcoded(SLP1)
        print("Getting tags for", word_in)
        tags = self.get_tags(word_in)
        if tags != None:
            map(print, tags)