import pygame  
import pymunk  
import pymunk.pygame_util  
import random  
  
# Pygameの初期化  
pygame.init()  
  
# ウィンドウの設定  
width, height = 600, 600  
screen = pygame.display.set_mode((width, height))  
pygame.display.set_caption("ボールフュージョン")  
  
# 物理空間の設定  
space = pymunk.Space()  
space.gravity = (0, 900)  # 重力を下向きに設定  
  
# 描画用のユーティリティを設定  
draw_options = pymunk.pygame_util.DrawOptions(screen)  

# 箱の作成  
floor = pymunk.Segment(space.static_body, (50, 550), (550, 550), 5)  
left_wall = pymunk.Segment(space.static_body, (50, 100), (50, 550), 5)  
right_wall = pymunk.Segment(space.static_body, (550, 100), (550, 550), 5)  
   
# 壁と床の反発係数  
floor.elasticity = 0.8  
left_wall.elasticity = 0.8  
right_wall.elasticity = 0.8  
   
# 壁と床を物理空間に追加  
space.add(floor, left_wall, right_wall)  
  
# ボールを生成して物理空間に追加する関数  
def create_ball(x, y, radius):  
    mass = 1  
    inertia = pymunk.moment_for_circle(mass, 0, radius)  
    body = pymunk.Body(mass, inertia)  
    body.position = x, y  
    shape = pymunk.Circle(body, radius)  
    shape.elasticity = 0.8  
    space.add(body, shape)  
    return shape  
  
# ゲームループ  
running = True  
clock = pygame.time.Clock()  
while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        # マウスクリックでボールを生成  
        if event.type == pygame.MOUSEBUTTONDOWN:  
            x, y = pygame.mouse.get_pos()  
            # 8種類の大きさのボールからランダムに選ぶ  
            sizes = [5, 10, 15, 20, 25, 30, 35, 40]  # ボールの半径の例  
            radius = random.choice(sizes)  # ランダムにサイズを選択  
            create_ball(x, y, radius)  
  
    # 物理シミュレーションを進める  
    space.step(1/50)  
  
    # 描画  
    screen.fill((255, 255, 255))  # 背景を白でクリア  
    space.debug_draw(draw_options)  # 物理オブジェクトを描画  
    pygame.display.flip()  
  
    # FPSを60に設定  
    clock.tick(60)  
  
pygame.quit() 