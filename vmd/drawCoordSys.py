from graphics import *
from molecule import *
id=new('mol')
load('graphics', name(id) )
cylinder(id,(0.0,0.0,0.0),(8.0,0.0,0.0),resolution=12)
cone(id,(8.0,0.0,0.0),(12.0,0.0,0.0),radius=1.5,resolution=12)
cylinder(id,(0.0,0.0,0.0),(0.0,8.0,0.0),resolution=12)
cone(id,(0.0,8.0,0.0),(0.0,12.0,0.0),radius=1.5,resolution=12)
cylinder(id,(0.0,0.0,-0.5),(0.0,0.0,8.0),resolution=12)
cone(id,(0.0,0.0,8.0),(0.0,0.0,12.0),radius=1.5,resolution=12)
