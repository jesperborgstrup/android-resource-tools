'''
Created on 22/08/2013

@author: Jesper
'''

from resourcetools.analyzer import ResourceAnalyzer

if __name__ == '__main__':
    analyzer = ResourceAnalyzer( r"C:\mi\FOF\App", debug=True )
    result = analyzer.read( )
    result.dump_count()
    pass