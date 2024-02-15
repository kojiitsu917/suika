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
wall_color = (0, 0, 0,255) 

# 背景画像の読み込み  
background_image = pygame.image.load("background.png")  
background_image = pygame.transform.scale(background_image, (width, height))  

# 箱の作成  
# Create walls and set their color  
floor = pymunk.Segment(space.static_body, (50, 500), (550, 500), 5)  
floor.color = wall_color  
  
left_wall = pymunk.Segment(space.static_body, (50, 100), (50, 500), 5)  
left_wall.color = wall_color  
  
right_wall = pymunk.Segment(space.static_body, (550, 100), (550, 500), 5)  
right_wall.color = wall_color  

# 壁と床の反発係数  
floor.elasticity = 0.8  
left_wall.elasticity = 0.8  
right_wall.elasticity = 0.8  
   
# 壁と床を物理空間に追加  
space.add(floor, left_wall, right_wall)  

# ボールにIDを割り当てるためのグローバル変数  
ball_id_counter = 0  
# スコアを保持するグローバル変数  
score = 0  

def merge_balls(arbiter, space, data):  
    # 衝突した2つのボールを取得  
    ball_shape1, ball_shape2 = arbiter.shapes  
    global score  # スコアのグローバル変数を使用 

    size_to_score = {  5: 10, 10: 20, 20: 30, 30: 50, 40: 80, 50: 100, 75: 200, 90: 400 }   
 
    # 最大サイズのボールかどうか確認  
    if ball_shape1.radius == sizes[-1] and ball_shape2.radius == sizes[-1]:  
        # 両方のボールを物理空間から削除する  
        space.remove(ball_shape1, ball_shape1.body)  
        space.remove(ball_shape2, ball_shape2.body)  
        return False  # これ以上の処理は行わない  

    if ball_shape1.radius == ball_shape2.radius:  
        # 合体して新しいボールを作成する  
        score += size_to_score.get(ball_shape1.radius, 0) 
        new_radius = size_to_next_size.get(ball_shape1.radius, ball_shape1.radius)  
        x = (ball_shape1.body.position.x + ball_shape2.body.position.x) / 2  
        y = (ball_shape1.body.position.y + ball_shape2.body.position.y) / 2  
          
        # 古いボールを削除する  
        space.remove(ball_shape1, ball_shape1.body)  
        space.remove(ball_shape2, ball_shape2.body)  
  
        # 新しいボールを作成する際の反発威力を、ボールの大きさに比例させる  
        impulse_base = 1000  # 基本となる反発威力  
        impulse_multiplier = new_radius / sizes[0]  # ボールの大きさに比例する係数  
        impulse = impulse_base * impulse_multiplier  # 最終的な反発威力  
  
        # 新しいボールを作成し、物理空間に追加する  
        new_ball = create_ball(x, y, new_radius)  
        space.add(new_ball.body, new_ball)  
  
        # 周囲のボールを反発させる  
        for shape in space.shapes:  
            if shape != new_ball:  
                dx = shape.body.position.x - x  
                dy = shape.body.position.y - y  
                distance = (dx**2 + dy**2)**0.5  
                if distance < new_radius * 5:  # 反発する範囲を設定  
                    # 反発する威力をボールの大きさに比例させる  
                    impulse = impulse_base * impulse_multiplier * (1 - distance / (new_radius * 5))  
                    shape.body.apply_impulse_at_local_point((impulse * dx / distance, impulse * dy / distance))  
  
        return True  




  
# create_ball関数内でボールのサイズを管理するための辞書を作成  
sizes = [5, 10, 20, 30, 40, 50, 75, 90]  
size_to_next_size = {sizes[i]: sizes[i+1] for i in range(len(sizes)-1)}  
  
# ボールを生成して物理空間に追加する関数  
def create_ball(x, y, radius):  
    global ball_id_counter 
    global sizes  # Make sure to use the global 'sizes' list
      # 果物を参考にした色のリスト  
    fruit_colors = [  
        (255, 0, 0, 255),    # りんご（赤）  
        (255, 165, 0, 255),  # オレンジ  
        (255, 255, 0, 255),  # バナナ（黄色）  
        (0, 128, 0, 255),    # キウイ（緑）  
        (255, 20, 147, 255), # イチゴ（ピンク）  
        (0, 255, 255, 255),  # ブルーベリー（シアン）  
        (128, 0, 128, 255),  # ブドウ（紫）  
        (255, 140, 0, 255)   # パパイア（橙）
    ]  
  
    # サイズに応じた色を設定  
    color = fruit_colors[sizes.index(radius) % len(fruit_colors)]  
  
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
    shape.color = color   # ボールの色を設定  
    shape.elasticity = 0.8  
    shape.collision_type = 1  
    shape.ball_id = ball_id_counter  
    ball_id_counter += 1  
    space.add(body, shape)  
    return shape  

# ゲームオーバーの状態を保持する変数  
game_over = False  
def check_game_over(space):  
    global game_over  
    for shape in space.shapes:  
        if isinstance(shape, pymunk.Circle):  
            # ボールが床より下にあるかチェック  
            if shape.body.position.y - shape.radius > height:  
                game_over = True  
                return True  # ゲームオーバー  
    return False  # ゲーム続行  

# ゲームオーバー画面の表示とエンターキー待機処理  
def show_game_over_screen(screen):  
    screen.fill((0, 0, 0))  # 画面を黒でクリア  
    font = pygame.font.Font(None, 72)  # ゲームオーバー表示用のフォント  
    game_over_text = font.render("Game Over", True, (255, 255, 255))  
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))  
    screen.blit(game_over_text, game_over_rect)  
    pygame.display.flip()  # 画面を更新  
  
    waiting = True  
    while waiting:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                waiting = False  
                pygame.quit()  
                exit()  # プログラムを終了  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_RETURN:  # エンターキーが押されたら  
                    waiting = False  


# 衝突ハンドラーを設定  
collision_handler = space.add_collision_handler(1, 1)  
collision_handler.post_solve = merge_balls  
  
# ゲームループ  
running = True  
clock = pygame.time.Clock()  
font = pygame.font.Font(None, 36)  # スコア表示用のフォント  
while running:
    if check_game_over(space):  
    # ゲームオーバーの場合、ループを抜ける  
         break  
    for event in pygame.event.get():  
    
        
        if event.type == pygame.QUIT:  
            running = False  
                # マウスクリックでボールを生成  
        # マウスクリックでボールを生成する部分の変更  
        if event.type == pygame.MOUSEBUTTONDOWN:    
            radius = random.choice(sizes)  # ランダムにサイズを選択  
            x, _ = pygame.mouse.get_pos()  # クリックした位置のX座標を取得  
            # クリックされたX座標が箱の範囲外の場合、範囲内に制限する  
            x = max(50 + radius, min(x, 550 - radius))  
            create_ball(x, 100, radius)  # Y座標は固定の値を使用  
    # ゲームループ後  
    if game_over:  
        show_game_over_screen(screen)  
        # ここにゲームをリスタートするか、終了するかの処理を追加する  
    # 描画    
    screen.blit(background_image, (0, 0))  # 背景画像を描画  
    space.debug_draw(draw_options)

    # スコアの表示位置を変更 (例: 画面の右上に表示)  
    
    # スコア表示用のテキストを生成  
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # 白色のテキスト  
    score_text_rect = score_text.get_rect(topright=(width - 10, 10))  # 右上に配置  
    
    # スコアの背景を描画 (半透明の黒色の長方形)  
    score_background = pygame.Surface((score_text_rect.width, score_text_rect.height))  
    score_background.set_alpha(0)  # 半透明度を設定 (0-255 の範囲、255 が不透明)  
    score_background.fill((0, 0, 0))  # 黒色で塗りつぶし  
    screen.blit(score_background, score_text_rect)  # スコアの背景を描画  
    
    # スコアのテキストを描画  
    screen.blit(score_text, score_text_rect)         
    # 物理シミュレーションを進める 
    space.step(1/50)  
  
   
    
    # 追加したボールの描画処理  
    for shape in space.shapes:  
        if isinstance(shape, pymunk.Circle):  
            # shape.colorが設定されていない場合はデフォルトの色を使用  
            color = getattr(shape, 'color', (0, 0, 0))  
            # Pygameは座標を整数で扱うため、intにキャスト  
            position = int(shape.body.position.x), int(shape.body.position.y)  
            pygame.draw.circle(screen, color, position, int(shape.radius))
    

    pygame.display.flip()  

  
    # FPSを60に設定  
    clock.tick(60)  
  
pygame.quit() 