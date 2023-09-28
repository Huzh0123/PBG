
#Rigid-body generator module
import bpy
import bmesh
import random
import parameters

def part_generation(pellet_key,x_y_range,phi_range,z_range):

    from Rashig_ring import Rashig_ring
    from user_defined import user_defined

    numb = 5
    x = random.sample(x_y_range,numb)
    y = random.sample(x_y_range,numb)
    z = random.sample(z_range,numb)
    x_r = random.sample(phi_range, numb)
    y_r = random.sample(phi_range, numb)
    z_r = random.sample(phi_range, numb)
    
    for i in range(numb):
        if pellet_key == 0:
            
            bpy.ops.mesh.primitive_uv_sphere_add(segments=28,
                                             ring_count=28,
                                             radius = parameters.particle_radius,
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
                path=parameters.off_file_path,
                location=(x[i], y[i], z[i]),
                rotation=(x_r[i], y_r[i], z_r[i]))

        bpy.ops.rigidbody.object_add(type='ACTIVE')
        obj = bpy.context.object.rigid_body
        obj.enabled = True
        obj.collision_shape = parameters.collision_shape
        obj.mass = 1
        obj.friction = parameters.friction_factor
        obj.restitution = parameters.restitution_factor
        obj.mesh_source = 'BASE'
        obj.use_margin = parameters.use_margin
        obj.collision_margin = parameters.collision_margin
        obj.linear_damping = parameters.linear_damping
        obj.angular_damping = parameters.rotational_damping

def container_generation(container_radius, container_depth):

    container_projection_shape = parameters.container_projection_shape
    bpy.ops.mesh.primitive_cylinder_add(location = (0,0,0),
                                        vertices = container_projection_shape,
                                        radius = container_radius,
                                        depth = container_depth)
    bpy.ops.object.select_by_type( type = 'MESH')
    bpy.ops.export_mesh.stl(filepath=parameters.container_path,
                            check_existing=True,
                            axis_forward='Y',
                            axis_up='Z',
                            filter_glob= ".STL",
                            global_scale=0.01,
                            ascii=False,
                            use_mesh_modifiers=True)
    obj = bpy.ops.object
    obj.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'TOGGLE')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.faces.ensure_lookup_table()
    bm.faces[(container_projection_shape-2)].select = True
    bpy.ops.mesh.delete(type = 'FACE')
    obj_new = bpy.ops.object
    obj_new.mode_set(mode = 'OBJECT')
    obj_new.modifier_add( type = 'SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness  = 0.01
    obj_new.modifier_apply(modifier = "Solidify")
    bpy.ops.rigidbody.objects_add(type = 'PASSIVE')
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
