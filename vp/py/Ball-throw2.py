
g=9.8
size = 0.7
scene = display(width=600, height=500, background=vector(0.6,0.3,0.2), center=vector(-9,7,0))
floor = box(length=24, height=0.5, width=4, color=color.green, pos=vector(-9,0,0))
box(length=8, height=0.5, width=4, color=color.red, pos= vector(7,0,0) )
box(length=8, height=0.5, width=4, color=color.green, pos= vector(15,0,0) )

axis = []
labels = []
axisInit()

scene.range=16
camera_x1=0.8
camera_x2=0.0
scene.forward=vector(camera_x1,camera_x2,-1)

preloadAudio('Startup.wav')
preloadAudio('chord.wav')
preloadAudio('gj.wav')

def axisInit():
    global axis, labels
    a = -21
    b = 0
    c = 40
    d = 10
    axis.append(arrow(pos=vec(a,b,-2), axis=vec(c+5,0,0), shaftwidth= 0.1, color = color.white))
    axis.append(arrow(pos=vec(a,b,-2), axis=vec(0,d+5,0), shaftwidth= 0.1, color = color.white))
    for t in range(0,20):
        axis.append(box(pos=vec(a + (t+1)*(c/20),b+d/2,-2), length=0.1, height=d, width=0.1))
    
    for j in range(0,10):
        axis.append(box(pos=vec(a + c/2,b + (j+1)*(d/10),-2), length=c, height=0.1, width=0.1,color=color.gray(0.8)))
    
    labels.append(label(pos=vec(a + 0*(c/5),b + d+ d/10,-1.5), text = str(0*(c/5)), height = 20, border = 12, font = 'monospace', color = color.white, box = False, opacity=0))
    for x in range(1,6):
        num = str(x*(c/5))
        labels.append(label(pos=vec(a + x*(c/5),b + d + d/10,-2), text = num, height = 20, border = 12, font = 'monospace', color = color.white, box = False, opacity=0))
    
    for y in range(0,6):
        num = str(b+y*(d/5))
        labels.append(label(pos=vec(a-2*c/40,b + y*(d/5),-2), text = num, height = 20, border = 12, font = 'monospace', color = color.white, box = False))
def balljump(spd):
    if (spd < 3): return 

    ball = sphere(pos=vector(-24.5, 10.0, 0.0), radius=size, color=color.white)
    ball.velocity = vector(spd, -1.0, 0.0)

    dt = 0.003
    gj_playFlag=1

    def resetScene():
        scene.background = vector(0.6, 0.3, 0.2)
        
    
    def jump():
        global gj_playFlag

        #console.log(ball.pos.x, ball.pos.y)
        if ball.pos.x < 15:
          rate(1000, jump)
        else:
          ball.visible = False
          gj_playFlag = 1 
          return

        if (ball.pos.x < 10 and ball.pos.x > 1.5) and ball.pos.y < 1 :
            scene.background = vector(0,0,0)
            if gj_playFlag: 
                playAudio('gj.wav') 
                gj_playFlag=0
            rate(4, resetScene)
		
        previous_x = ball.pos.x
        ball.pos = ball.pos + ball.velocity * dt

        if ball.pos.y < size and ball.velocity.y < 0:
            ball.velocity.y = - ball.velocity.y
            playAudio('chord.wav')
        else:
            ball.velocity.y = ball.velocity.y - g * dt
    
    jump()

def Speed(data):
    if data != None:
        balljump(data[0])

def setup():
    profile = {
        'dm_name': 'Ball-throw2',
        'odf_list': [Speed],
    }

    dai(profile)
    playAudio('Startup.wav')

setup()

