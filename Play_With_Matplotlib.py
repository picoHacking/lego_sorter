# import modules
import matplotlib.pyplot as plt
import random
import numpy as np
'''
# basic graph generator
x = [1, 2, 3, 4, 5]
y = [3, 4, 2, 5, 5]

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
'''
'''
# random graph generator

fig = plt.figure()
fig.patch.set_facecolor('xkcd:cocoa')
axe = fig.add_subplot(1,1,1) # rows, cols, index
axe.set_facecolor('xkcd:creme')
def graph():
    xs = []
    ys = []
    for i in range(30):
        xs.append(i)
        ran = random.randrange(10)
        ys.append(ran*ran)
    return xs, ys
plt.plot(graph())
'''
'''
# expression of feelings
y = np.linspace(2,24,12)
plt.xticks(12) # doesn't work!!
plt.yticks(24) # doesn't work!!

plt.plot(y, y**3, label='screen time in 2020')
plt.plot(y, y+1, label = 'screen time before 2020')

plt.xlabel('Month')
plt.ylabel('Screen Time')

plt.title("Screen Time Graph")
plt.legend()
'''

plt.ion()
plt.plot([2.0, 3.0])
plt.show()
