# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
x_scatter = [-7.0, -7.0, -4.301029995663981, -4.301029995663981]
y_scatter = [4.3979400086720375, 4.698970004336019, 4.3979400086720375, 4.698970004336019]
results = {(1e-07, 25000.0): (0.3746938775510204, 0.379), (1e-07, 50000.0): (0.3606734693877551, 0.383), (5e-05, 25000.0): (0.04593877551020408, 0.043), (5e-05, 50000.0): (0.10026530612244898, 0.087)}
# plot training accuracy
marker_size = 100
colors = [results[x][0] for x in results]

plt.subplot(2, 1, 1)
plt.scatter(x_scatter, y_scatter, marker_size, c=colors)
plt.colorbar()
plt.xlabel('log learning rate')
plt.ylabel('log regularization strength')
plt.title('CIFAR-10 training accuracy')

# plot validation accuracy
colors = [results[x][1] for x in results] # default size of markers is 20

plt.subplot(2, 1, 2)
plt.scatter(x_scatter, y_scatter, marker_size, c=colors)
plt.colorbar()
plt.xlabel('log learning rate')
plt.ylabel('log regularization strength')
plt.title('CIFAR-10 validation accuracy')
plt.show()