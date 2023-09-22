
import sys
import os
CurrentDir = os.getcwd()	
sys.path.append(CurrentDir) 
print(CurrentDir, "added to system path.") 

import parameters
if parameters.Simulator_option == 'rigidbody':
    import bpy 
    from Rigidbody_generator import container_generation
    from Simulator import steady_state, rigidbody_simulation
    print("Welcome to the generator")   
    print("Initializing the parameters ...")
    #Geometry input parameters
    Particle_type = parameters.Particle_type
    container_radius = parameters.container_radius # circumcircle radius 
    container_depth = parameters.container_depth
    number_of_particle = parameters.number_of_particle

    #Generating the container
    container_generation(container_radius, container_depth)
    bpy.context.scene.frame_end = 50000
    bpy.context.scene.rigidbody_world.point_cache.frame_end = 50000

    if parameters.number_of_particle <= 500:
        frames = int(number_of_particle * 10 / 5) 
    else:
        frames = int(number_of_particle * 2 / 5) 


    #generating the particles and filling up the tube
    print("Filling up the bed....")
    print("Solver iterations per step: ",bpy.context.scene.rigidbody_world.solver_iterations)
    simulation_current_frame = rigidbody_simulation(Particle_type, frames)

    bpy.ops.object.select_by_type( type = 'MESH')
    #continuing the simulation till steady-state (condition: max particle velocity < 0.01)
    print("Reaching the steady_state condition")
    distance=steady_state(simulation_current_frame)
    bpy.ops.object.select_all(action = 'TOGGLE')#removing the container
    if parameters.remove_the_tube == True:
        bpy.data.objects['Cylinder'].select_set(True)
        bpy.ops.object.delete(use_global = False)

    #Saving the blender file to have the packing with separated particles
    print("Saving a copy of the packing...")
    bpy.ops.wm.save_as_mainfile(filepath = parameters.blender_file_path)
        
    #to export the bed uncomment the next 2 lines: 
    #bpy.ops.object.select_all(action = 'TOGGLE')
    print("Exporting the geometry as a STL file...")
    bpy.ops.export_mesh.stl(filepath=parameters.file_path,
                            check_existing=True,
                            axis_forward='Y',
                            axis_up='Z',
                            filter_glob= ".STL",
                            global_scale=0.01,
                            ascii=False,
                            use_mesh_modifiers=True)

elif parameters.Simulator_option == 'radial_voidage':
    import radial_voidage
    radial_voidage.radial_voidage()

print("Done!")
print("Goodbye!")
