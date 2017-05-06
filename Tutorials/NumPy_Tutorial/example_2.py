# Basic Operations

from numpy import *

a = array ([20,30,40,50]);
b = arange (4);

#Sum
result = a - b;
print (result);

#Multiplication by a scalar
result = 10*b;
print(result);

#Power in each element
result = b**2;
print (result);

C = array( [[1,1],
            [0,1]] );
D = array( [[2,0],
            [3,4]] );

#Elementwise product
print(C*D);

#Matrix product
print(dot(C,D));
