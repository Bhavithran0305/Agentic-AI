import numpy as np
 
 
box = [1, 2, 3] * 2
# print(box)
 
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(my_list[0:5])
 
# my_list_1 = np.array([1, 2, 3]) * 2
 
# print(my_list_1)
 
box1 = np.array(['a', 1])
# print(box1.ndim)
 
arr = np.array([[1, 'a',2], [3, 'b', 4],
[5, 'c', 6], [7, 'd', 8]])
# print(arr[1][2]) #chain indexing
# print(arr.ndim)
 
 
 
ar = np.array([[[1, 2, 3], [4,5,6], [7,8,9]],
               [[10, 11, 12], [13,14,15], [16,17,18]],
               [[19, 20,21], [22, 23,24], [25,26,27]]])
 
# print(ar[-1])
# #ar(rows, column, [start:end:step])
# print(ar[0, 1, 1]) #multidimension indexing
print(ar[::-1,::-1,::-1])
 
# print(ar.shape)
# print(arr.shape)















