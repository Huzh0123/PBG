


import numpy as np
import re


path = './Tube (Meshed).stl'

faces = []
edges = []
vertexs = []
count = 0
with open(path, 'r') as f:
    reader = f.readlines()
    for line in reader:
        if 'vertex' in line:
            vertex = re.findall(r'vertex (.*?) (.*?) (.*?)\n', line)[0]
            vertex = [float(x) for x in vertex]
            vertexs.append(vertex)
            edges.append([count, count+1])
            count += 1





# def read_off(filename):
#     points = []
#     faces = []
#     edges = []
#     with open(filename, 'r') as f:
#         first = f.readline()
#         n, m, c = f.readline().rstrip().split(' ')[:]
#
#         n = int(n)
#         m = int(m)
#         for i in range(n):
#             value = f.readline().rstrip().split(' ')
#             points.append([float(x) * 0.1 for x in value[:3]])
#         for i in range(m):
#             value = f.readline().rstrip().split(' ')
#             faces.append([int(x) for x in value])
#
#         for face in faces:
#             for num in range(len(face)):
#                 if [face[num-1], face[num]] not in edges:
#                     edges.append([face[num-1], face[num]])
#
#     return points, edges, faces








