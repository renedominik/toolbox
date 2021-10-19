from math import *
from graphics import *
from molecule import *


id=new('mol')
load('graphics', name(id) )

nr_res=12
i=1
while i <= nr_res:
	a=8.0*cos(i*100*pi/180)
	b=8.0*sin(i*100*pi/180)		
	c=12.0*cos(i*100*pi/180)
	d=12.0*sin(i*100*pi/180)
	k=i*3
	cylinder(id,(0.0,0.0,i),(a,b,i),resolution=12)
	cone(id,(a,b,i),(c,d,i),radius=1.5,resolution=12)
	i=i+1


color(id,'magenta')
cylinder(id,(0.0,0.0,-0.5),(0.0,0.0,3*nr_res+4.0),resolution=12)
cone(id,(0.0,0.0,3*nr_res+4.0),(0.0,0.0,3*nr_res+8.0),radius=1.5,resolution=12)
