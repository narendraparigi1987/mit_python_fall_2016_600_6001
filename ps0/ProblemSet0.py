#!/usr/bin/python2.7 ''' Unix representation '''
#_*_ Coding : utf-8 _*_
'''
created on 24-07-2017

@author : Narendra Parigi
'''

import math
import numpy
import pylab

def get_input(help_text='Enter value: '):
    return int(input(help_text))

def exponant(x,y):
    return x**y

def log(x):
    return numpy.log2(x)

def main():
    print 'Welcome to ProblemSet0'
    x = get_input('Enter value for value x: ')
    y = get_input('Enter value for value y: ')
    z = exponant(x,y)
    print 'x**y = {}'.format(z)
    print 'logx = {}'.format(log(x)) # with numpy
    print 'logx = {}'.format(pylab.log2(x)) # with pylab

if __name__ == '__main__':
    main()

