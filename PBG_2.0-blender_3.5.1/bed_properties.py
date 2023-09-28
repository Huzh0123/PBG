import math
import bpy
import math
import parameters

def angle_distribution(file_name):

    size = len(bpy.context.selected_objects)
    cos_t = [None]*size
    t = [None]*size
    deg = [None]*size
    j = size -1 

    for obj in bpy.context.selected_objects: 
        current_obj = obj
        z_coor=[0,0,1] 
        face = current_obj.data.polygons[30]
        mat = current_obj.matrix_world  
        normal = face.normal*mat

        cos_t[j] = normal[2]/pow(((pow(normal[0],2))+(pow(normal[1],2))+(pow(normal[2],2))),0.5)
        t[j] = math.acos(cos_t[j])
        deg[j] = math.degrees(t[j])
        
        if deg[j]>90:
          deg[j]=180-deg[j]

        j=j-1 
          
    ang_dist = [None] * 9
    for i in range(9):
        low_bound = 10*i
        up_bound = low_bound+10
        ang_dist[i] = len([x for x in deg if low_bound < x < up_bound])

    sum_ang_dist = sum(ang_dist)
    if sum_ang_dist == size:
        print("check = True")

    ang_dist_per = [None]*9
    print(file_name)
    f=open(file_name,'w')
    for k in range(9):
        low_bound = 10*k
        up_bound = low_bound+10
        ang_dist_per[k] = ang_dist[k]/sum_ang_dist
        per = ang_dist_per[k]
        f.write("Frequency of the particles in the range of %d-%d is: %s \n"%(low_bound, up_bound, per))  
    f.close()
    print(ang_dist_per)    
    



# def voidage():    
#     bpy.ops.object.delete()
#     bpy.ops.import_mesh.stl(filepath= parameters.file_path, 
#                             axis_forward='Y', 
#                             axis_up='Z', 
#                             filter_glob="*.stl",  
#                             global_scale=1.0, 
#                             use_scene_unit=True, 
#                             use_facet_normal=False)
    
#     for ob in bpy.context.scene.objects:
#         if ob.type == 'MESH':
#             ob.select_set(True)
#             bpy.context.view_layer.objects.active = ob

#     for obj in bpy.data.objects:
#         obj.name = 'bed'
    
#     bpy.ops.object.select_all(action = 'TOGGLE')
#     # renaming the stl file
#     obj = bpy.data.objects["bed"]
#     # changing to edit mode to make all the face normals consistant and facing outwards
#     bpy.ops.object.editmode_toggle()
#     bpy.ops.mesh.normals_make_consistent(inside = False)
#     bpy.ops.object.editmode_toggle()
#     #setting the origin to the geometry and to the space origin
#     bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
#     bpy.context.object.location = 0,0,0
#     p_l = obj.matrix_world.translation
#     u = bpy.context.object.dimensions

#     print("The bed dimensions (X,Y,Z) are:", u[0], u[1], u[2])
#     j = 1
#     for i in range(48):
#         R = R*j
#         bpy.ops.surface.primitive_nurbs_surface_cylinder_add(location = [0, 0 ,z_co], radius = R)
#         bpy.ops.object.convert( target = 'MESH')
#         bpy.context.object.scale[2] = L/2
#         bpy.ops.object.modifier_add(type='SOLIDIFY')
#         bpy.ops.object.modifier_apply(apply_as='DATA', modifier = "Solidify")
#         slice = bpy.context.active_object.data
#         bm = bmesh.new()
#         bm.from_mesh(slice)
#         slice_volume = bm.calc_volume()
#         bpy.ops.object.modifier_add(type='BOOLEAN')
#         bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
#         bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["bed"]
#         bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
#         intersect = bpy.context.active_object.data
#         bm_intersect = bmesh.new()
#         bm_intersect.from_mesh(intersect)
#         intersect_volume = bm_intersect.calc_volume()
#         r_p[i] = 1-(intersect_volume/slice_volume)
#         j = j-0.02
#         bpy.ops.object.delete(use_global = False)
#     return(r_p)  
