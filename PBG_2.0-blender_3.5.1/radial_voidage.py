import bpy  
from mathutils import Vector  
from mathutils.bvhtree import BVHTree  
import numpy as np
import math
import os
import parameters 
import matplotlib.pyplot as plt

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


def radial_voidage():
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

    delta_l = 5e-4
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

    r_incircle_bed = max(u[0], u[1]) / 2
    length_bed = u[2]
    # setting max and min height of the radial surface

    # generating a cylindrical surface mesh 
    loop_num = 99
    r_p = [0] * loop_num
    w_d = [0] * loop_num
    Area_face = pow(delta_l,2)
    list_z = [z for z in np.arange(-u[2]/2, u[2]/2/2, delta_l)]
    list_z_eps = []
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
        eplison = 1 - (packed_area / ring_area)
        print('zi: {:.6f}, eplison_zi: {:.6f}, '.format(z, eplison))
        list_z_eps.append([z, eplison])
        
    print('100% progress...Radial voidage calculation is finished!')
    print('writing the data...')
    print('Done! :)')
