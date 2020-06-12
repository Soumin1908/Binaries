import bpy
import numpy as np
from scipy.integrate import odeint
for o in bpy.context.scene.objects:
    if o.type in ['MESH','FONT','EMPTY']:
        o.select_set(True)
    else:
        o.select_set(False)
bpy.ops.object.delete()   

def sim(m1,m2,par0,t):
    t=t*365*24*3600
    G=6.67*10**(-11)
    ms=1.98*10**30
    m1=m1*ms
    m2=m2*ms
    au=149.6*10**9
    M=m1+m2
    def equation_sim(par,t,G,M):
        au=149.6*10**9
        x=par[0]*au
        y=par[1]*au
        z=par[2]*au
        xd=par[3]
        yd=par[4]
        zd=par[5]
        xdd=-(G*M*x)/((x**2+y**2+z**2))**(3/2)
        ydd=-(G*M*y)/((x**2+y**2+z**2))**(3/2)
        zdd=-(G*M*z)/((x**2+y**2+z**2))**(3/2)
        return [xd/au,yd/au,zd/au,xdd,ydd,zdd]
    ar=odeint(equation_sim,par0,t,args=(G,M))
    return ar

G=6.67*10**(-11)
ms=1.98*10**30
au=149.6*10**9
t=np.linspace(0,1.5486,77)
m1=12.8
m2=11.9
mew=G*(m1+m2)*ms
a=3.859
e=0.7
v=((mew/(a*au))*((1-e)/(1+e)))**0.5
par0=np.array([a*(1+e),0,0,0,v,0])
M=m1+m2

a=sim(m1,m2,par0,t)


bpy.ops.mesh.primitive_uv_sphere_add(radius=m1/10,enter_editmode=False, location=(m2/M*par0[0]*5,m2/M*par0[1]*5,m2/M*par0[2]*5))
sun1=bpy.data.objects['Sphere']
sun1.name='Star1'
sun1.keyframe_insert('location',frame=1)

bpy.ops.mesh.primitive_uv_sphere_add(radius=m2/10,enter_editmode=False, location=(-m1/M*par0[0]*5,-m1/M*par0[1]*5,-m1/M*par0[2]*5))
sun2=bpy.data.objects['Sphere']
sun2.name='Star2'
sun2.keyframe_insert('location',frame=1)

for m in bpy.data.materials:
    bpy.data.materials.remove(m)
    
mat1=bpy.data.materials.new('Star1')
mat1.use_nodes=True
sun1.data.materials.append(mat1)
bsdf=mat1.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value=(0.8,0.661312,0.00799073,1)
bsdf.inputs[17].default_value=(0.8,0.661312,0.00799073,1)

mat2=bpy.data.materials.new('Star2')
mat2.use_nodes=True
sun2.data.materials.append(mat2)
bsdf=mat2.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value=(0.8,0.661312,0.00799073,1)
bsdf.inputs[17].default_value=(0.8,0.661312,0.00799073,1)

for m in bpy.data.particles:
    bpy.data.particles.remove(m)
    
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(-10,0,-15))
bg=bpy.data.objects["Plane"]
bg.name='Background'
bg.scale=(35,35,35)
part1=bg.modifiers.new('backg',type='PARTICLE_SYSTEM')
bpy.data.particles["backg"].type='HAIR'

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4,enter_editmode=False, location=(30,30,30))
star1=bpy.data.objects['Sphere']
star1.name='Star12'

bpy.data.particles["backg"].render_type="OBJECT"
bpy.data.particles["backg"].instance_object=star1
bpy.data.particles["backg"].size_random=1

mat=bpy.data.materials.new('sfield')
mat.use_nodes=True
star1.data.materials.append(mat)
bsdf0=mat.node_tree.nodes["Principled BSDF"]
bsdf0.inputs[17].default_value=(1,0.9,0.65,1)

mat0=bpy.data.materials.new('bac')
mat0.use_nodes=True
bg.data.materials.append(mat0)
bsdf1=mat0.node_tree.nodes["Principled BSDF"]
bsdf1.inputs[0].default_value=(0,0,0,1)

material_output = mat1.node_tree.nodes.get('Material Output')
emission=mat1.node_tree.nodes.new("ShaderNodeEmission")
emission.inputs['Strength'].default_value=10
emission.inputs[0].default_value=(0.9804,1,0.3246,1) 
blackbody = mat1.node_tree.nodes.new("ShaderNodeBlackbody")
blackbody.inputs['Temperature'].default_value=5000   
mat1.node_tree.links.new(emission.inputs[0],blackbody.outputs[0])    
mat1.node_tree.links.new(material_output.inputs[0],emission.outputs[0])

material_output = mat2.node_tree.nodes.get('Material Output')
emission=mat2.node_tree.nodes.new("ShaderNodeEmission")
emission.inputs['Strength'].default_value=3
emission.inputs[0].default_value=(0.9804,1,0.3246,1) 
blackbody = mat2.node_tree.nodes.new("ShaderNodeBlackbody")
blackbody.inputs['Temperature'].default_value=35000   
mat2.node_tree.links.new(emission.inputs[0],blackbody.outputs[0])    
mat2.node_tree.links.new(material_output.inputs[0],emission.outputs[0])

cam=bpy.data.objects["Camera"]
cam.rotation_euler=(1.040216,0,6.02138)
cam.location=(-15.343,-47.873,23.368)
cam.keyframe_insert('rotation_euler',frame=1)
cam.keyframe_insert('location',frame=1)

txt=bpy.ops.object.text_add(location=(8.3687,-4.6466,-1.8693))
txt=bpy.context.object
txt.data.body = "11.9 Msun"
txt.rotation_euler=(1.1938,0,0)
txt.scale=(2.6,2.6,2.6)
txt.keyframe_insert('location',frame=1)

txt1=bpy.ops.object.text_add(location=(-20.636,-3.4682,-2.9953))
txt1=bpy.context.object
txt1.data.body = "12.8 Msun"
txt1.rotation_euler=(1.1938,0,0)
txt1.scale=(2.6,2.6,2.6)
txt1.keyframe_insert('location',frame=1)



for i in range (1,77):
    sun1.scale=(1,1,1)
   ## if i<60:
    cam.rotation_euler=(1.040216,0,6.02138)
    cam.location=(-15.343,-47.873,23.368)
    cam.keyframe_insert('rotation_euler',frame=i)
    cam.keyframe_insert('location',frame=i)
    
    sun1.location=(m2/M*a[i][0]*5,m2/M*a[i][1]*5,m2/M*a[i][2]*5)
    sun1.keyframe_insert('location',frame=i+1)
    sun2.location=(-m1/M*a[i][0]*5,-m1/M*a[i][1]*5,-m1/M*a[i][2]*5)
    sun2.keyframe_insert('location',frame=i+1)

ref=bpy.ops.object.empty_add(type='SPHERE')
ref=bpy.data.objects['Empty']
sun1.parent=ref
sun2.parent=ref
ref.keyframe_insert('rotation_euler',frame=77)

sun1.keyframe_insert('scale',frame=77)
sun1.scale=(3,3,3)
a1=1.67
e1=0.0
v1=((mew/(a1*au))*((1-e1)/(1+e1)))**0.5
par1=np.array([a1*(1+e1),0,0,0,v1,0])
sun1.location=(m2/M*par1[0]*5,m2/M*par1[1]*5,m2/M*par1[2]*5)
sun2.location=(-m1/M*par1[0]*5,-m1/M*par1[1]*5,-m1/M*par1[2]*5)
ref.rotation_euler=(2*np.pi,2*np.pi,2*np.pi)
ref.keyframe_insert('rotation_euler',frame=85)
sun1.keyframe_insert('scale',frame=85)
sun2.keyframe_insert('scale',frame=85)
sun1.keyframe_insert('location',frame=85)
sun2.keyframe_insert('location',frame=85)

t1=np.linspace(0,0.871,45)
a1=sim(m1,m2,par1,t1)
for i in range (85,130):
    sun1.location=(m2/M*a1[i-85][0]*5,m2/M*a1[i-85][1]*5,m2/M*a1[i-85][2]*5)
    sun1.keyframe_insert('location',frame=i+1)
    sun2.location=(-m1/M*a1[i-85][0]*5,-m1/M*a1[i-85][1]*5,-m1/M*a1[i-85][2]*5)
    sun2.keyframe_insert('location',frame=i+1)
