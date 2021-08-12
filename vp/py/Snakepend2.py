orientation = vec(0,0,0)
def Orientation_O(data):
    global orientation
    if data != None:
        orientation.x = data[0]
        orientation.y = data[1]
        orientation.z = data[2]

def setup():
    profile = {
        'dm_name' : 'Snakepend2',
        'odf_list' : [Orientation_O],
    }
    dai(profile)

setup()


animateSpeed = 1.0
g = 9.8             # 重力加速度
Tpw = 30            # 蛇擺的週期
N = 15              # 週期最長的單擺在蛇擺的1個週期內擺動的次數
Tmax = Tpw / N      # 週期最長的單擺擺動週期
Lmax = Tmax ** 2 * g / (4 * pi ** 2)   # 週期最長的單擺擺長 
num = 20            # 單擺的個數
width = Lmax        # 將畫面邊長設定為最長的單擺擺長
m = 1               # 小球質量
size = width / (2 * num)           # 小球半徑
theta0 = radians(30)# 起始擺角, 用 radians 將單位換成 rad
i = 0               # 小球經過週期次數
t = 0               # 時間
dt = 0.001          # 時間間隔
animateSpeed = 0.2
old_orientation = vec(0, 0, 0)
oldOrientationGamma = None

# 新增類別 Pendulum, 輸入週期T, 懸掛位置loc, 編號idx, 自動產生小球及對應的繩子
# 設定方法 update, 輸入經過的時間dt, 更新單擺狀態
class Pendulum:
    def __init__(self, T, loc, idx):
        self.T = T
        self.loc = loc
        self.idx = idx
        self.L = self.T ** 2 * g / (4 * pi ** 2)
        self.I = m * self.L ** 2
        self.alpha = 0
        self.omega = 0
        self.theta = theta0
        self.ball = sphere(pos=vector(self.loc, width / 2 - self.L * cos(theta0), self.L * sin(theta0)),
                           radius=size, color=vector(1 - self.idx / num, 0, self.idx / num))
        self.rope = cylinder(pos=vector(self.loc, width / 2, 0),
                             axis=self.ball.pos - vector(self.loc, width / 2, 0), radius=0.1 * size,
                             color=vector(0.7, 0.7, 0.7))
    def update(self, dt):
        self.dt = dt
        self.alpha = -m * g * self.ball.pos.z / self.I
        self.omega += self.alpha * self.dt
        self.theta += self.omega * self.dt
        self.ball.pos = vector(self.loc, width / 2 - self.L * cos(self.theta), self.L * sin(self.theta))
        self.rope.axis = self.ball.pos - vector(self.loc, width / 2, 0)

# 初始化場景
def scene_init():
    global timer, pendulums, scene
    global t
    # 產生動畫視窗、天花板
#    scene = canvas(width=600, height=600, x=0, y=0, 
#                   background=vector(0.1, 0.5, 0.1))

    scene = canvas(width=600, height=600, x=0, y=0, 
                   background=color.white)
    scene.camera.pos = vector(-1.5 * width, 0.5 * width, width)
    scene.camera.axis = vector(1.5 * width, -0.5 * width, -width)
    roof = box(pos=vector(0, (width + size) / 2, 0), length=width, height=size, width = width / 2,
               color = color.cyan)
    timer = label(pos=vector(0.9 * width, 0.9 * width, 0), text="t =  s", space=50, height=24, border=4, font="monospace")
    # 利用自訂類別 Pendulum 產生 num 個單擺
    pendulums = []
    for i in range(num):
        T = Tpw / (N + i)
        loc = width * (-0.5 + (i / (num - 1)))
        pendulum = Pendulum(T, loc, i)
        pendulums.append(pendulum)

scene_init()
    
while True:
    rate(animateSpeed / dt)
    if orientation.x is not old_orientation.x or orientation.y is not old_orientation.y or orientation.z is not old_orientation.z:
        old_orientation.x = orientation.x        
        old_orientation.y = orientation.y       
        old_orientation.z = orientation.z      
        if not oldOrientationGamma:
            oldOrientationGamma = orientation.z
        else:
            variant = orientation.z - oldOrientationGamma
            oldOrientationGamma = orientation.z
            if abs(variant) > 4:
                animateSpeed = min(animateSpeed + 0.02, 3.0)
            else:
                animateSpeed = max(animateSpeed - 0.02, 0.3) 

    scene.background = vector(animateSpeed / 3, 0.5, 0.1)
    for pendulum in pendulums:
        pendulum.update(dt)
    # timer.text = "t = {:.f} s".format(t)
    timer.text = "speed = {:.2f}x".format(animateSpeed)
    t += dt

