

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
            points.append([float(x) for x in value[:3]])
        for i in range(m):
            value = f.readline().rstrip().split(' ')
            faces.append([int(x) for x in value[1:]])

        for face in faces:
            for num in range(len(face)):
                if [face[num - 1], face[num]] not in edges:
                    edges.append([face[num - 1], face[num]])

    return points, edges, faces


def user_defined(path, location, rotation):
    import bpy
    import bmesh

    verts, edges, faces = read_off(path)
    mesh = bpy.data.meshes.new(name="RR")
    mesh.from_pydata(verts, edges, faces)
    mesh.validate()
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("Particle", mesh)
    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.context.object.location = location
    bpy.context.object.rotation_euler = rotation
