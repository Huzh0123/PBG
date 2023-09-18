##Packed-Bed generation module (Version-Beta)
##BPartopour, AG Dixon†
##Heat and Mass Transfer Lab
##Worcester Polytechnic Institute

#Rigid-body generator module
import bpy
import bmesh
import math 
import random
import parameters
import numpy as np

x=[]
y=[]
z=[]

def part_generation(pellet_key,x_y_range,phi_range,top,flag):

    from Rashig_ring import Rashig_ring
    from user_defined import user_defined

    if len(x_y_range) < 5:
        pop_2 = list(np.arange(-1,1,0.3))
        x = random.sample(pop_2,5)
        y = random.sample(pop_2,5)
        numb = 5
    else:
        x = random.sample(x_y_range, 5)
        y = random.sample(x_y_range, 5)
        numb = 5
    z = random.sample(range(top, top + 8),5)
    x_r = random.sample(phi_range, 5)
    y_r = random.sample(phi_range, 5)
    z_r = random.sample(phi_range, 5)


    for i in range(numb):
        if pellet_key == 0:
            
            bpy.ops.mesh.primitive_uv_sphere_add(segments=28,
                                             ring_count=28,
                                             size = parameters.particle_radius,
                                             location = (x[i],y[i],z[i]))
                                             
        elif pellet_key == 1:

            bpy.ops.mesh.primitive_cylinder_add(vertices = 50,
                                                end_fill_type = 'TRIFAN',
                                                radius = parameters.particle_radius,
                                                depth = parameters.particle_length,
                                                location = (x[i], y[i],z[i]),
                                                rotation = (x_r[i], y_r[i], z_r[i]))
        elif pellet_key == 2:
            Rashig_ring(outer_radius = parameters.particle_radius,
                        inner_radius = parameters.particle_inner_radius,
                        depth = parameters.particle_length,
                        location = (x[i], y[i], z[i]),
                        rotation = (x_r[i], y_r[i], z_r[i]))
        elif pellet_key == 3:
            user_defined(
                path=parameters.off_path,
                location=(x[i], y[i], z[i]),
                rotation=(x_r[i], y_r[i], z_r[i]))

        bpy.ops.rigidbody.objects_add(type='ACTIVE')
        obj = bpy.context.object.rigid_body
        obj.enabled = True
        obj.collision_shape = parameters.collision_shape
        #obj.mass = 1
        obj.friction = parameters.friction_factor
        obj.restitution = parameters.restitution_factor
        obj.mesh_source = 'BASE'
        obj.use_margin = parameters.use_margin
        obj.collision_margin = parameters.collision_margin
        obj.linear_damping = parameters.linear_damping
        obj.angular_damping = parameters.rotational_damping

def tube_generation(cyl_radius, cyl_depth):

    cyl_vertices = 4
    bpy.ops.mesh.primitive_cylinder_add(location = (0,0,0),
                                        vertices = cyl_vertices,
                                        radius = cyl_radius,
                                        depth = cyl_depth)

    obj = bpy.ops.object
    obj.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'TOGGLE')

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.faces.ensure_lookup_table()
    bm.faces[(cyl_vertices-2)].select = True
    bpy.ops.mesh.delete(type = 'FACE')
    obj_new = bpy.ops.object
    obj_new.mode_set(mode = 'OBJECT')
    obj_new.modifier_add( type = 'SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness  = 0.02
    obj_new.modifier_apply(modifier = "Solidify")
    bpy.ops.rigidbody.object_add(type = 'PASSIVE')
    obj = bpy.context.object.rigid_body
    obj.collision_shape = 'MESH'
    obj.friction = 0.1
    obj.restitution = 0.1
    obj.use_margin = parameters.use_margin
    obj.collision_margin = parameters.collision_margin
    #activating split impulse
    bpy.context.scene.rigidbody_world.enabled = True
    bpy.context.scene.rigidbody_world.use_split_impulse = True
    bpy.context.scene.rigidbody_world.substeps_per_frame = 200
    bpy.context.scene.rigidbody_world.solver_iterations = 200
    
