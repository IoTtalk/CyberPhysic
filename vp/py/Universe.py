def Gravity(data):
    global gravity
    if data != None:
        gravity = data[0]


def Speed(data):
    global speed
    if data != None:
        speed = data[0]


# 設定
def setup():
    profile = {
        'dm_name' : 'Universe',
        'odf_list' : [Gravity, Speed],
    }
    dai(profile)

setup()

earth_radius = 0.8 # 球半徑(m)
height = 12.0     # 初始高度(m)
speed = 25.0        # 初始速度
gravity = 25.0          # 萬有引力常數
direction = vec(1,0,0) # 初始方向

# 模擬實驗參數區
freq = 120        # 更新頻率(Hz)
dt = 1.0 / freq   # 更新間隔(second)

# 事件旗標區
reset_flag = False

axis = []
labels = []

# 重置
def reset_earth():
    global earth, reset_flag
    # 復位
    earth.pos = vec(0, height, 0)
    # 速度歸零
    earth.velocity = speed*norm(direction)
    # 洗去旗標
    reset_flag = False

# 初始化場景
def scene_init():
    global scene, earth, sun, height, earth_radius, label_gravity, axis, labels
    scene = display(width=800, height=700, center = vec(0, 0, 0), background=vec(0, 0, 0), autoscale = False, range=height)
#    scene = display(width=800, height=700, center = vec(0, 0, 0), background=color.white)
    label_gravity = label( pos=vec(0.8*height,0.8*height,0), height=25, text='Gravity: {:.3f}\nSpeed: {:.3f}'.format(gravity,speed))
    
    sun_light = local_light(pos = vec(0,0,0),color=color.white)
    more_sun_light = local_light(pos = vec(0,0,0),color=color.white)

    for radius in range(2, 15):
        axis.append(ring(pos=vec(0,0,-5), axis=vec(0,0,1), radius=radius*2, thickness=0.1, color=color.gray(0.1)))
        
    for radius in range(2, 15):
        labels.append(label(pos=vec(0, radius*2 + 0.5, -5), text=str(radius*2), height=20, border=12, font='monospace', color=color.white, box=False, opacity=0))

    sun = sphere(
        pos = vec(0, 0, 0), 
        radius = 2*earth_radius,
        velocity = vec(0, 0, 0),
        texture = {'file': "/images/sun.jpg"},
        emissive = True,
        opacity = 0.8,

    )
    earth = sphere(
        pos = vec(0, height, 0), 
        radius = earth_radius,
        texture = {'file': "/images/earth.jpg"},
        flipx = False,
        velocity = speed*norm(direction),
    )

    scene.autoscale = False

scene_init()

#用來判斷萬有引力常數、速度是否改變
prev_state = (gravity, speed)
while True:
    rate(freq)
    label_gravity.text = 'Gravity: {:.3f}\nSpeed: {:.3f}'.format(gravity,speed)
    # 模擬天體運動
    # 模擬天體運動
    if (earth.pos-sun.pos).mag > sun.radius+earth_radius:
        earth.pos = earth.pos + earth.velocity * dt
        if earth.pos.mag > height*2 :
            label_gravity.text = 'Gravity: {:.3f}\nSpeed: {:.3f}\nout of screen'.format(gravity,speed)
    
    earth.velocity = earth.velocity - gravity * norm(earth.pos - sun.pos) / (earth.pos - sun.pos).mag2
    #如果萬有引力常數、速度已改變，重置畫面
    if prev_state != (gravity, speed):
        reset_flag = True
    if reset_flag == True:
        reset_earth()
    prev_state = (gravity, speed)
