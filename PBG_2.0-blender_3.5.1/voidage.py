import bpy  
from mathutils import Vector  
from mathutils.bvhtree import BVHTree  
import numpy as np
import math
import os
import parameters 
# import matplotlib.pyplot as plt

###### function q_inside checks if a point is inside the "solid" packing based on ray-casting algorithm ###
###### ray casting algorithm can be mathematically proved by Jordan curve theorm #########
def q_inside(obj, point_in_object_space):  
    direction = Vector((1,0,0))
    epsilon = direction * 1e-6
    count = 0
    result, point_in_object_space, normal, index = obj.ray_cast(point_in_object_space, direction)
    while result:
        result, point_in_object_space, normal, index = obj.ray_cast(point_in_object_space + epsilon, direction)
        count += 1
    return (count % 2) == 1


def voidage():
    bpy.ops.object.delete()
    bpy.ops.import_mesh.stl(filepath= parameters.container_path, 
                            axis_forward='Y', 
                            axis_up='Z', 
                            filter_glob="*.stl",  
                            global_scale=1.0, 
                            use_scene_unit=True, 
                            use_facet_normal=False)
    
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob

    for obj in bpy.data.objects:
        obj.name = 'bed'


    # renaming the stl file
    obj = bpy.data.objects["bed"]
    # changing to edit mode to make all the face normals consistant and facing outwards
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside = False)
    bpy.ops.object.editmode_toggle()
    #setting the origin to the geometry and to the space origin
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.object.location = 0,0,0
    p_l = obj.matrix_world.translation
    u = bpy.context.object.dimensions

    delta_l = 0.01
    probes_number = int(max(u[0], u[1]) / delta_l)
    probes_list = []
    for i in range(probes_number * 2):
        for j in range(probes_number * 2):
            x = -max(u[0], u[1]) + delta_l * i
            y = -max(u[0], u[1])+1e-6 + delta_l * j
            point_in_object_space = Vector((x, y, 0))
            d = q_inside(obj, point_in_object_space)
            if d:
                probes_list.append([x,y])
    bpy.ops.object.delete()
    bpy.ops.import_mesh.stl(filepath= parameters.file_path, 
                            axis_forward='Y', 
                            axis_up='Z', 
                            filter_glob="*.stl",  
                            global_scale=1.0, 
                            use_scene_unit=True, 
                            use_facet_normal=False)
    
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob

    for obj in bpy.data.objects:
        obj.name = 'bed'


    # renaming the stl file
    obj = bpy.data.objects["bed"]
    # changing to edit mode to make all the face normals consistant and facing outwards
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside = False)
    bpy.ops.object.editmode_toggle()
    #setting the origin to the geometry and to the space origin
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.object.location = 0,0,0
    p_l = obj.matrix_world.translation
    u = bpy.context.object.dimensions

    print("The bed dimensions (X,Y,Z) are:", u[0], u[1], u[2])

    # setting max and min height of the radial surface
    # generating a cylindrical surface mesh 
    bed_volume = []
    container_volume = []
    Area_face = pow(delta_l,2)
    save_list = []
    list_z = [z for z in np.arange(-u[2]/2, u[2]/2/2, delta_l)]
    for z in list_z:

        point_co =[(x,y,z) for (x,y) in probes_list]
        point_nu = len(point_co)
        count = 0
        d = False
        for p in range(0,point_nu):
            point_in_object_space = Vector((point_co[p]))
            d = q_inside(obj, point_in_object_space)
            if d:
                count += 1

        ring_area = Area_face * len(probes_list) 
        packed_area = Area_face * count
        bed_volume.append(packed_area * delta_l)
        container_volume.append(ring_area * delta_l)
        eplison = 1 - (packed_area / ring_area)
        save_list.append([z, eplison])
        print('zi: {:.6f}, eplison_zi: {:.6f}, '.format(z, eplison))

    np.savetxt('data.csv', np.array(save_list), delimiter=',')
    print('writing the data...')
    print('Done! :)')


def radial_voidage():
    bpy.ops.object.delete()
    bpy.ops.import_mesh.stl(filepath= parameters.file_path, 
                        axis_forward='Y', 
                        axis_up='Z', 
                        filter_glob="*.stl",  
                        global_scale=1.0, 
                        use_scene_unit=True, 
                        use_facet_normal=False)
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob

    for obj in bpy.data.objects:
        obj.name = 'bed'


    # renaming the stl file
    obj = bpy.data.objects["bed"]
    # changing to edit mode to make all the face normals consistant and facing outwards
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside = False)
    bpy.ops.object.editmode_toggle()
    #setting the origin to the geometry and to the space origin
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.object.location = 0,0,0
    p_l = obj.matrix_world.translation
    u = bpy.context.object.dimensions

    print("The bed dimensions (X,Y,Z) are:", u[0], u[1], u[2])
    R_tube = (max(u[0],u[1]))/2.0
    d = u[2] - 8 * parameters.particle_radius * 0.01
    r_p = [0]*99
    w_d = [0]*99

    j=1
    dp= 2*parameters.particle_radius * 0.01
    # setting max and min height of the radial surface
    Lmin = -d/2
    Lmax = d/2
    # generating a cylindrical surface mesh 
    w = 2*math.pi
    r_p = [0]*99
    w_d = [0]*99
    for i in range(0,99):
        #print('loop number is', i)
        R = j*R_tube
        step = 2*math.asin(dp/20/2/R)
        list_t = [t for t in np.arange(0,w,step)] 
        L_face = dp/20
        #print(L_face)
        Area_face = pow(L_face,2)
        list_x_y = [(R*math.cos(x_y),R*math.sin(x_y)) for x_y  in list_t]
        list_z = [z for z in np.arange(Lmin,Lmax,L_face)]
        point_co =[(x,y,z) for (x,y) in list_x_y for z in list_z]
        point_nu = len(point_co)
        count = 0
        #print('number of points',point_nu)
        d = False
        for p in range(0,point_nu):
            point_in_object_space = Vector((point_co[p]))
            d = q_inside(obj, point_in_object_space)
            if d:
                count += 1

        ring_area = Area_face * point_nu 
        packed_area = Area_face * count
        r_p[i] = 1-(count/point_nu)   
        #print('eps', r_p[i])
        w_d[i] = j
        j = j - 0.01
        if i%10 == 0:
            print((i),'% progress...')
        
    print('100% progress...Radial voidage calculation is finished!')
    print('writing the data...')
    w_d[0] = 1.0
    Distance = [(R_tube*(1-x))/(2*parameters.particle_radius * 0.01) for x in w_d]
    file_name = parameters.file_path_2

    np.savetxt(file_name, 
               np.column_stack((np.array(Distance), np.array(r_p))),
               delimiter=','
               )

    print('Done! :)')






