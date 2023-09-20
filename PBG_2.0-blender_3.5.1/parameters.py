
#Defining parameters for the simulation 


# simulator option, valid options: 'rigidbody', 'radial_voidage'
Simulator_option = 'radial_voidage'

# defining particle type, valid types: 'sphere', 'cylinder', 'Raschig Ring', 'user_defined'
Particle_type = 'user_defined'
# If Particle_type = 'user_defined', the address of the off file must be provided. 
off_file_path = r'.\models\Cut01.off'
# Raduis of the container
container_radius = 5
# Length of the container
container_depth = 50
# Container projection shape, represented as a regular polygon
container_projection_shape = 4

## Particles Properties
#Number of Particles
number_of_particle = 100
#Particle radius !! in case of Rashig Ring this is outer radius
particle_radius = 0.5
#particle innter radius for extruded geometries
particle_inner_radius = 0.2
#Particle Length (for cylinders, in case of spheres leave it as default)
particle_length = 1


## Rigidbody Properties
#Collision Shape, valid types: 'MESH', 'CONVEX_HULL', 'SPHERE'
collision_shape = 'CONVEX_HULL'
#Surface Friction Factor ( 0 < friction_factor < 1 )
friction_factor = 0.1
#Surface Restitution Factor (0 < restitution_factor < 1)
restitution_factor = 0.0
#Usinig Coloision Margin: Yes (True), NO (False)
use_margin = True
#Colosion margin (lower value = more accuracy, 0 perfect value)
collision_margin = 0.0
#linear_deactivation(linear deactivation velocity)

#linear_damping(amount of linear velicity particle is lost over time)
linear_damping = 0.2
#rotational_dampin
rotational_damping = 0.1

#Do you want to remove the tube after simulation?
remove_the_tube = True

#Do you want to calculate the angle distribution of the particles after the bed is generated?
angle_dist = False
#Where do you want to save the angle_dist results?
file_name =r'D:\PBG\500_fh_N=6.txt'
#Where to save the blender working file? this file gives access to the packing with discrete particles
blender_file_path = r"D:\PBG\working_bed_X.blend"
## Stl Export properties
file_path = r"D:\PBG\Cut01.stl"
container_path = r"D:\PBG\container.stl"
## Stl Export for capped geometry in case of spherical particles
file_path_capped = r"D:\PBG\capped_bed.stl"
## Where do you want to save the radial voidage results?
file_path_2 = r"D:\PBG\500_fh_N=6.txt"
