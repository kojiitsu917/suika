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

# ボールにIDを割り当てるためのグローバル変数  
ball_id_counter = 0  
  
def merge_balls(arbiter, space, data):  
    # 衝突した2つのボールを取得  
    ball_shape1, ball_shape2 = arbiter.shapes  
    if ball_shape1.radius == ball_shape2.radius:  
        # 合体して新しいボールを作成する  
        new_radius = size_to_next_size.get(ball_shape1.radius, ball_shape1.radius)  
        x = (ball_shape1.body.position.x + ball_shape2.body.position.x) / 2  
        y = (ball_shape1.body.position.y + ball_shape2.body.position.y) / 2  
          
        # 古いボールを削除する  
        space.remove(ball_shape1, ball_shape1.body)  
        space.remove(ball_shape2, ball_shape2.body)  
          
        # 新しいボールを作成し、物理空間に追加する  
        new_ball = create_ball(x, y, new_radius)  
        space.add(new_ball.body, new_ball)  
          
        return True  


  
# create_ball関数内でボールのサイズを管理するための辞書を作成  
sizes = [5, 10, 20, 30, 40, 50, 60, 80]  
size_to_next_size = {sizes[i]: sizes[i+1] for i in range(len(sizes)-1)}  
  
# ボールを生成して物理空間に追加する関数  
def create_ball(x, y, radius):  
    global ball_id_counter  
    # ボールが合体してサイズが大きくなった場合、次のサイズを決定する  
    if radius in size_to_next_size:  
        new_radius = size_to_next_size[radius]  
    else:  
        new_radius = radius  # 最大サイズの場合はそのままのサイズを使う  
  
    mass = 1  
    inertia = pymunk.moment_for_circle(mass, 0, new_radius)  
    body = pymunk.Body(mass, inertia)  
    body.position = x, y  
    shape = pymunk.Circle(body, new_radius)  
    shape.elasticity = 0.8  
    shape.collision_type = 1  
    shape.ball_id = ball_id_counter  
    ball_id_counter += 1  
    space.add(body, shape)  
    return shape  


  
# 衝突ハンドラーを設定  
collision_handler = space.add_collision_handler(1, 1)  
collision_handler.post_solve = merge_balls  
  
# ゲームループと他の部分は変更なし  


# ゲームループ  
running = True  
clock = pygame.time.Clock()  
while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
                # マウスクリックでボールを生成  
        # マウスクリックでボールを生成する部分の変更  
        if event.type == pygame.MOUSEBUTTONDOWN:  
            # 8種類の大きさのボールからランダムに選ぶ  
            sizes = [5, 10, 15, 20, 25, 30, 35, 40]  # ボールの半径の例  
            radius = random.choice(sizes)  # ランダムにサイズを選択  
            x, _ = pygame.mouse.get_pos()  # クリックした位置のX座標を取得  
            # クリックされたX座標が箱の範囲外の場合、範囲内に制限する  
            x = max(50 + radius, min(x, 550 - radius))  
            create_ball(x, 100, radius)  # Y座標は固定の値を使用  
  
                
    # 物理シミュレーションを進める  
    space.step(1/50)  
  
    # 描画  
    screen.fill((255, 255, 255))  # 背景を白でクリア  
    space.debug_draw(draw_options)  # 物理オブジェクトを描画  
    pygame.display.flip()  
  
    # FPSを60に設定  
    clock.tick(60)  
  
pygame.quit() 