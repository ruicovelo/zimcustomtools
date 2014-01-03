'''
Created on Jan 3, 2014

@author: ruicovelo
'''
import argparse

class ArgumentParser(argparse.ArgumentParser):
    ''' 
    For using with Zim custom tool scripts that are started like this:
    script.py --notebook %n --temppage %f --attachment %d --realpage %s --root %D --seltext %t --seltextwiki %T
    '''
    def __init__(self):
        super(ArgumentParser,self).__init__()
        self.add_argument('--temppage')
        self.add_argument('--attachment')
        self.add_argument('--realpage')
        self.add_argument('--notebook')
        self.add_argument('--root')
        self.add_argument('--seltext')
        self.add_argument('--seltextwiki')

