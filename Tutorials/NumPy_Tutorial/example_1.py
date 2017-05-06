#Array Creation

from numpy  import *

a = arange(15).reshape(3, 5)
print ("a:");
print(a);

#Getting the dimension of the array
print(a.shape);

#Getting the rank of the array
print(a.ndim);

print(a.dtype.name);

print(a.itemsize);

print(a.size);

print(type(a));

#Creating an array
b = array([6, 7, 8]);
print ("b:");
print(b);

c = arange(12).reshape(4,3);

print ("c:");
print (c);

d = arange(24).reshape(2,3,4);
print ("d:");
print (d);
