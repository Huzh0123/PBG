def Rashig_ring(outer_radius, inner_radius, depth, location, rotation):
    import numpy as np
    import math
    import bpy
    import bmesh
    # z_range = [-1.0, 1.0]
    # phi_range = list(np.arange(0,2*math.pi,math.pi/32))
    # x_range = [(outer_radius*round(math.cos(phi),4)) for phi in phi_range]
    # x_range_2 = [(inner_radius*round(math.cos(phi),4)) for phi in phi_range]
    # x_range = x_range + x_range_2
    # y_range = [(outer_radius*round(math.sin(phi),4)) for phi in phi_range]
    # y_range_2 = [(inner_radius*round(math.sin(phi),4)) for phi in phi_range]
    # y_range = y_range + y_range_2
    # size = len(x_range)
    # x_y_range = list(zip(x_range, y_range))
    # verts = [(x,y,z) for (x,y) in x_y_range for z in z_range]
    edges = []
    # faces = []
    #
    # for i in range(size):
    #     if i < size-2:
    #         faces.append([i,i+1,i+2])
    #     elif i == (size-2):
    #         faces.append([i,i+1,0])
    #     elif i == (size-1):
    #         faces.append([i,0,1])
    # for i in range(size,size*2):
    #     if i < size*2-2:
    #         faces.append([i,i+1,i+2])
    #     elif i == (size*2-2):
    #         faces.append([i,i+1,size])
    #     elif i == (size*2-1):
    #         faces.append([i,size,size+1])
    # u = int(size)
    # for i in range(u):
    #     if i < u-2:
    #         faces.append([i,i+2,i+u])
    #         faces.append([i+2,i+u,i+u+2])
    #     elif i == u-2:
    #         faces.append([i,0,i+u])
    #         faces.append([i+u,u,0])
    #     elif i == u-1:
    #         faces.append([i,1,i+u])
    #         faces.append([i+u,u+1,1])


    path = './Tube.off'

    def read_off(filename):
        points = []
        faces = []
        edges = []
        with open(filename, 'r') as f:
            first = f.readline()
            n, m, c = f.readline().rstrip().split(' ')[:]

            n = int(n)
            m = int(m)
            for i in range(n):
                value = f.readline().rstrip().split(' ')
                points.append([float(x) * 0.1 for x in value[:3]])
            for i in range(m):
                value = f.readline().rstrip().split(' ')
                faces.append([int(x) for x in value[1:]])

            for face in faces:
                for num in range(len(face)):
                    if [face[num - 1], face[num]] not in edges:
                        edges.append([face[num - 1], face[num]])

        return points, edges, faces

    verts,edges, faces = read_off(path)
    mesh = bpy.data.meshes.new(name="RR")
    mesh.from_pydata(verts, edges, faces)
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("Rashig", mesh)  
    scene = bpy.context.scene    
    scene.objects.link(obj)    
    obj.select = True
    bpy.context.scene.objects.active =obj
    bpy.context.object.location = location
    bpy.context.object.scale[2] = depth/2
    bpy.context.object.rotation_euler = rotation

