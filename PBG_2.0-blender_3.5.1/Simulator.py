##Packed-Bed generation module (Version-BAeta)
##BPartopour, AG Dixon†
##Heat and Mass Transfer Lab
##Worcester Polytechnic Institute

#Simulator module

import bpy
import math
import numpy as np
import parameters

def rigidbody_simulation(Particle_type, frames):
    from Rigidbody_generator import part_generation
    import numpy as np
    co = parameters.container_radius / 3
    top = int(parameters.container_depth / 4) - 10
    z_range = list(np.linspace(top, top+10, 8))
    x_y_range = list(np.linspace(-co, co, 8))
    phi_range = list(np.arange(0.0, 6.28, 0.5))

    pellet = {'sphere' : 0, 'cylinder' : 1, 'Raschig Ring':2, 'user_defined':3}
    pellet_key = pellet[Particle_type]

    simulation_current_frame = 1
#    scene = bpy.context.scene
#    fp = scene.render.filepath
    i = 0
    for i in range(frames):
        if (simulation_current_frame % 10) == 0.0:
            print('Frame: ', str(simulation_current_frame) + ' of ' + str(frames))

            part_generation(pellet_key,x_y_range,phi_range,z_range)


        bpy.context.scene.frame_set(frame = simulation_current_frame)
#        scene.render.filepath = fp + str(i+1)
#        bpy.ops.render.render(write_still=True)
        simulation_current_frame += 1

    return(simulation_current_frame)
    
def steady_state(simulation_current_frame):
    
    size= len(bpy.context.selected_objects)
    x = [0]*size
    y = [0]*size
    z = [0]*size
    x_prev = [0]*size
    y_prev = [0]*size
    z_prev = [0]*size
    d = [1]*size
    Stop = False
    count = 0
 #   scene = bpy.context.scene
 #   fp = scene.render.filepath
 #   i = simulation_current_frame
    while ( Stop == False and count <= 500 ):

        i = 0
        for obj in bpy.context.selected_objects:
            current_obj = obj
            x[i],y[i],z[i] = obj.matrix_world.translation
            d[i]=(((((x[i]-x_prev[i])**2))+(((y[i]-y_prev[i])**2))+(((z[i]-z_prev[i])**22)))**0.5)
            x_prev[i],y_prev[i],z_prev[i] = x[i],y[i],z[i]
            i = i+1
        print('steady_state: ', count, 'max(d): ', max(d))
        if max(d) < 0.01:
            Stop = True

        bpy.context.scene.frame_set(frame = simulation_current_frame)
#        scene.render.filepath = fp + str(simulation_current_frame)
#        bpy.ops.render.render(write_still=True)
        simulation_current_frame += 1
        count = count + 1
    return(d)

