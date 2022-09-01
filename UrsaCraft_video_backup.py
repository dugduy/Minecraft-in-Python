from ursina import *
from json import load,dump
# from ast import literal_eval
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
texttures=(grass_texture,stone_texture,brick_texture,dirt_texture)
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 0
# last_model=
voxels=load(open('./checkpoint.json'))

# window.fps_counter.enabled = False
# window.exit_button.visible = False

def update():
	global block_pick

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 0
	if held_keys['2']: block_pick = 1
	if held_keys['3']: block_pick = 2
	if held_keys['4']: block_pick = 3

class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):

		voxels[str(position).replace('Vec3','')]=block_pick
		dump(voxels,open('./checkpoint.json','w'))
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)

	def input(self,key):
		if self.hovered:
			if key == 'left mouse down':
				punch_sound.play()
				# print(self.position)
				voxel = Voxel(position = self.position + mouse.normal, texture = texttures[block_pick])
				# print(voxel.position)
				# if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				# if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				# if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				# if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
				print(voxels)

			if key == 'right mouse down':
				punch_sound.play()
				# del voxels[self.position]
				print(voxels)
				destroy(self)

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))

	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)

# for z in range(10):
# 	for x in range(10):
# 		voxel = Voxel(position = (x,0,z))
for z in voxels:
	print(eval(z))
	Voxel(eval(z),texttures[voxels[z]])

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()