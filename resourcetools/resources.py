'''
Created on 22/08/2013

@author: Jesper
'''

class Resources(object):
    '''
    A representation of resources inside an Android project.
    
    Each resource type is a dictionary, where the resource name is the key, and the value is
    a list of qualifiers where this resource occurs
    '''
    
    property_animations = {}
    tween_animations = {}
    colors = {}
    drawables = {}
    layouts = {}
    menus = {}
    raw = {}
    
    arrays = {}
    dimensions = {}
    strings = {}
    plurals = {}
    styles = {}
    
    xml = {}

    def __init__(self, property_animations={}, tween_animations={}, colors={},
                       drawables={}, layouts={}, menus={}, raw={}, arrays={},
                       dimensions={}, strings={}, plurals={}, styles={}, xml={}):
        self.property_animations = property_animations
        self.tween_animations = tween_animations
        self.colors = colors
        self.drawables = drawables
        self.layouts = layouts
        self.menus = menus
        self.raw = raw
        self.arrays = arrays
        self.dimensions = dimensions
        self.strings = strings
        self.plurals = plurals
        self.styles = styles
        self.xml = xml
    
    def dump(self):
        print "Resources"
        print "---------"
        print "Colors: %s" % self.colors
        print "Drawables: %s" % self.drawables
        print "Layouts: %s" % self.layouts
        
    def dump_count(self):
        print "Property animations: %d" % len( self.property_animations.keys() )
        print "Tween animations: %d" % len( self.tween_animations.keys() )
        print "Colors: %d" % len( self.colors.keys() )
        print "Drawables: %d" % len( self.drawables.keys() )
        print "Layouts: %d" % len( self.layouts.keys() )
        print "Menus: %d" % len( self.menus.keys() )
        print "Raw: %d" % len( self.raw.keys() )
        print "Arrays: %d" % len( self.arrays.keys() )
        print "Dimensions: %d" % len( self.dimensions.keys() )
        print "Strings: %d" % len( self.strings.keys() )
        print "Plurals: %d" % len( self.plurals.keys() )
        print "Styles: %d" % len( self.styles.keys() )
        print "XML: %d" % len( self.xml.keys() )
        
    def __str__(self):
        return "Resources: colors(%s)" % ( self.colors )

    def add(self, restype, name, value):
        if not hasattr( self, restype ):
            raise ValueError( "Invalid resource type: %s" % ( restype ) )
        res = getattr(self, restype)
        if not isinstance( res, dict ):
            raise ValueError( "Invalid resource type: %s" % ( restype ) )

        if not res.has_key( name ):
            res[name] = []
            
        res[name].append( value )