import pygame as pg
import sys
from random import randint, choice
import cv2


pg.init()
pg.mixer.init()


font_xin = '04B_19.TTF'
screen = pg.display.set_mode((400, 600))
clock = pg.time.Clock()


def hieuung():
    # Thiết lập kích thước màn hình
    screen_width, screen_height = 400, 600
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Splash Screen Example")
# Màu sắc và thời gian
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    fade_duration = 20000  # thời gian hiệu ứng fade (tính bằng mili giây)


    # Tạo font và text cho màn hình mở đầu
    font = pg.font.Font(None, 74)
    text = font.render("Riot Games", True, WHITE)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))


    # Hàm hiệu ứng fade
    def fade_in_and_out(screen, fade_duration):
        fade_in_time = fade_out_time = fade_duration // 2
        clock = pg.time.Clock()


        # Hiệu ứng fade-in
        for alpha in range(0, 256):
            screen.fill(BLACK)
            text.set_alpha(alpha)
            screen.blit(text, text_rect)
            pg.display.flip()
            clock.tick(fade_in_time // 256)


        # Giữ màn hình trong 1 giây
        pg.time.delay(1000)


        # Hiệu ứng fade-out
        for alpha in range(255, -1, -1):
            screen.fill(BLACK)
            text.set_alpha(alpha)
            screen.blit(text, text_rect)
            pg.display.flip()
            clock.tick(fade_out_time // 256)


   # Chạy hiệu ứng fade-in và fade-out
    fade_in_and_out(screen, fade_duration)

def chon_nhac():
    selected_music = None
    # Load background image
    background_music = pg.image.load("Pic/background_music.png")
    background_music = pg.transform.scale(background_music, (screen.get_width(), screen.get_height()))

    

    # Danh sách bài nhạc
    music_files = ["Music/EDM1.mp3", "Music/EDM2.mp3", "Music/EDM3.mp3"]


    # Tọa độ và kích thước nút
    button_width = 200
    button_height = 50
    button_x = (screen.get_width() - button_width) // 2
    button_y_start = 200  # Vị trí nút đầu tiên
    button_spacing = 80  # Khoảng cách giữa các nút




    # Vòng lặp màn hình bắt đầu
    while True:
        # Vẽ màn hình nền
        screen.blit(background_music, (0, 0))

        # Tạo font chữ
        font = pg.font.Font(font_xin, 20)

        # Vẽ các nút chọn nhạc
        for i, music in enumerate(music_files):
            button_y = button_y_start + i * button_spacing
            button_rect = pg.Rect(button_x, button_y, button_width, button_height)
           
            # Tô màu nút
            pg.draw.rect(screen, (0, 128, 150), button_rect)
           
            # Hiển thị tên bài nhạc lên nút
            text_surface = font.render(music, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)




        # Kiểm tra sự kiện
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, music in enumerate(music_files):
                    button_y = button_y_start + i * button_spacing
                    button_rect = pg.Rect(button_x, button_y, button_width, button_height)
                    if button_rect.collidepoint(event.pos):
                        # Tải và phát nhạc tương ứng
                        selected_music = music
                        pg.mixer.music.load(selected_music)
                        pg.mixer.music.play(-1)
                        print(f"Đã chọn bài: {selected_music}")
                        return  # Thoát màn hình bắt đầu để sang màn hình game chính




        # Cập nhật màn hình
        pg.display.flip()
        clock.tick(30)


def reset_game():
    global score, lives, level, items, fireworks, particles, current_target_index
    global car_rect, fall_speed, game_over_flag, paused, game_started, wrong_hits, has_answered
    global car_speed  # Đảm bảo biến car_speed được khai báo là toàn cục

    # Reset gameplay variables
    score = 0
    lives = 3
    level = 1
    wrong_hits = 0
    has_answered = False
    game_over_flag = False
    paused = False
    game_started = False

    fall_speed = 5
    car_speed = 5  # Đặt lại tốc độ xe về giá trị ban đầu
    items = []
    fireworks = []
    particles = []
    current_target_index = 0
    car_rect.center = (200, 500)  # Reset xe về vị trí ban đầu

    print("Game reset to initial state.")

def show_restart_screen():
    global restart_game, paused

    # Pause game
    paused = True

    # Load background image
    background_image = pg.image.load("Pic/leuleu.png")
    background_image = pg.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    while True:
        # Draw background
        screen.blit(background_image, (0, 0))

        # Display restart button
        font = pg.font.Font(font_xin, 48)
        restart_text = font.render("Restart", True, (255, 255, 255))

        button_rect = pg.Rect(150, 300, 125, 50)
        pg.draw.rect(screen, (0, 128, 0), button_rect)
        text_rect = restart_text.get_rect(center=button_rect.center)
        screen.blit(restart_text, text_rect)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Clicked restart button
                    reset_game()  # Reset game variables
                    paused = False  # Unpause the game
                    show_start_screen()
                    return
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                reset_game()  # Reset game variables
                paused = False  # Unpause the game
                return

        pg.display.flip()
        clock.tick(30)



# Play intro video before the game starts
def play_intro_video():
   cap = cv2.VideoCapture('Pic/videodaugame.mp4')
   if not cap.isOpened():
       sys.exit()
   scale_width=400
   scale_height=600
 
   while cap.isOpened():
       ret, frame = cap.read()
       if not ret: break
       # Xoay video 90 độ theo chiều kim đồng hồ
       # Cách xoay video
       frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
       # Lật lại video (nếu video bị lật ngang hoặc dọc)
       # Nếu video bị lật theo chiều ngang (ví dụ như bị xoay trái sang phải), bạn có thể lật lại:
       frame = cv2.flip(frame, 1)  # Lật ngang
       # Thay đổi kích thước video sao cho vừa vặn với cửa sổ Pygame
       # Điều này sẽ giữ tỷ lệ gốc của video và co giãn video sao cho vừa với cửa sổ
       frame = cv2.resize(frame, (scale_height, scale_width))
       # Chuyển đổi từ BGR (OpenCV) sang RGB (Pygame)
       frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
     
       # Chuyển đổi frame từ numpy array sang surface để vẽ vào màn hình Pygame
       frame_surface = pg.surfarray.make_surface(frame)
     
       # Vẽ lên cửa sổ
       screen.blit(frame_surface, (0, 0))
       pg.display.flip()
     
       for event in pg.event.get():
           if event.type == pg.QUIT: sys.exit()
       clock.tick(30)
 
 
   cap.release()


# Game Assets
road = pg.transform.smoothscale(pg.image.load('Pic/background-cuoiki.png').convert(), (400, 600))
car = pg.transform.smoothscale(pg.image.load('Pic/yellow-car.png').convert_alpha(), (150, 200))
car_rect = car.get_rect()  # Khởi tạo car_rect từ ảnh xe
car_rect.center = (300, 400)


game_over_background = pg.transform.smoothscale(pg.image.load('Pic/leuleu.png').convert(), (400, 600))
level_up_background = pg.transform.smoothscale(pg.image.load('Pic/zoigoi.png').convert(), (400, 600))
road_y_pos = 0


power_up_images = {
   "ExtraLife": pg.image.load('Pic/heart.png').convert_alpha(),
   "Shield": pg.image.load('Pic/shield.png').convert_alpha()
}




# Scale power-up images
for power_up_type in power_up_images:
   power_up_images[power_up_type] = pg.transform.scale(power_up_images[power_up_type], (120, 120))

# Initialize movement flags
move_right = move_left = move_up = move_down = False

# Initialize Car and Movement Flags
car_rect = car.get_rect(center=(200, 500))

# Game settings
score, lives, level = 0, 3, 1
wrong_hits, has_answered, game_over = 0, False, False
paused, game_started, target_collected = False, False, False

car_speed=5 
fall_speed=5

# Item setup
item_images = {
   "Target": pg.image.load("Pic/Item1.png").convert_alpha(),
   "Other1": pg.image.load("Pic/Item2.png").convert_alpha(),
   "Other2": pg.image.load("Pic/Item3.png").convert_alpha(),
   "Other3": pg.image.load("Pic/Item4.png").convert_alpha()
}



# Scale item images
for item_type in item_images:
   item_images[item_type] = pg.transform.scale(item_images[item_type], (120, 120))

# List to hold items
items = []

# Trivia Data
questions = [
   "When was the 3I Institute established?",
   "Who is the director of the 3I Institute?",
   "Who is the director of the Logistics Technology Program?",
   "What is I in 3I institute?",
   "Which major is currently being trained at 3I Institute?"
]
options = [
   ("A. 2019", "B. 2020", "C. 2018", "D. 2022"),
   ("A. PhD Trieu", "B. Dr. Thinh", "C. Dr. Dung", "D. Dr. Duc Cuong"),
   ("A. Dr. Duc Cuong", "B. PhD Trieu", "C. Dr. Dung", "D. Dr Son"),
   ("A.Institute", "B.Intelligent", "C.Interactive", "D. All answers are correct"),
   ("A.Marketing", "B.Logistics Technology", "C. International Business", "D. Management")
]
answers = ("A", "B", "A", "D", "B")


def show_start_screen():
    global game_started
    background_start = pg.image.load("Pic/background_start.png")  # Đường dẫn đến ảnh nền
    background_start = pg.transform.scale(background_start, (screen.get_width(), screen.get_height()))  # Scale ảnh nền
    
    rules_visible = False  # Trạng thái hiển thị rules
    rules_image = pg.image.load("Pic/rules.png")  # Đường dẫn đến ảnh rules
    rules_image = pg.transform.scale(rules_image, (screen.get_width(), screen.get_height()))  # Scale ảnh rules

    while not game_started:
        if not rules_visible:
            # Hiển thị màn hình start
            screen.blit(background_start, (0, 0))
            font = pg.font.Font(font_xin, 36)

            # Nút "Start"
            start_text = font.render("Start", True, (255, 255, 255))
            start_button_rect = pg.Rect(150, 440, 100, 50)  # (x, y, width, height)
            pg.draw.rect(screen, (0, 128, 0), start_button_rect)  # Nút màu xanh lá
            start_text_rect = start_text.get_rect(center=start_button_rect.center)
            screen.blit(start_text, start_text_rect)

            # Nút "Rules"
            rules_text = font.render("Rules", True, (255, 255, 255))
            rules_button_rect = pg.Rect(150, 520, 100, 50)  # (x, y, width, height)
            pg.draw.rect(screen, (128, 0, 0), rules_button_rect)  # Nút màu đỏ
            rules_text_rect = rules_text.get_rect(center=rules_button_rect.center)
            screen.blit(rules_text, rules_text_rect)
        
        else:
            # Hiển thị màn hình rules
            screen.blit(rules_image, (0, 0))
            font = pg.font.Font(font_xin, 36)
            rules_info = font.render("Press ENTER to go back", True, (255, 255, 255))
            info_rect = rules_info.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
            screen.blit(rules_info, info_rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if not rules_visible:
                    if start_button_rect.collidepoint(event.pos):  # Kiểm tra nhấn nút Start
                        game_started = True
                    elif rules_button_rect.collidepoint(event.pos):  # Kiểm tra nhấn nút Rules
                        rules_visible = True
            if event.type == pg.KEYDOWN and rules_visible:
                if event.key == pg.K_RETURN:  # Nhấn Enter để quay lại
                    rules_visible = False

        pg.display.flip()
        clock.tick(30)

# Helper functions
def droad():
   screen.blit(road, (0, road_y_pos))
   screen.blit(road, (0, road_y_pos - 600))

last_extra_life_spawn_time = 0
extra_life_cooldown = 10000  # 10 giây (10000 ms)
def spawn_power_up():
   global last_extra_life_spawn_time, items_fallen_count
   if items_fallen_count >= 5:
       # Spawn "ExtraLife" if cooldown is over
       current_time = pg.time.get_ticks()
       if current_time - last_extra_life_spawn_time > extra_life_cooldown:
           x_position = randint(20, 250)
           power_up_type = "ExtraLife"
           power_up_rect = power_up_images[power_up_type].get_rect(topleft=(x_position, 0))
           items.append((power_up_rect, power_up_type))
           last_extra_life_spawn_time = current_time
           items_fallen_count = 0  # Reset the count after spawning power-up
       else:
           # Spawn other power-ups
           if randint(0, 1):  # 50% chance for Shield to appear
               x_position = randint(20, 250)
               power_up_type = "Shield"
               power_up_rect = power_up_images[power_up_type].get_rect(topleft=(x_position, 0))
               items.append((power_up_rect, power_up_type))
               items_fallen_count = 0  # Reset the count after spawning power-up
# Biến toàn cục để theo dõi trạng thái khiên
shield_active = False
shield_timer = 0
shield_duration = 3000  # Thời gian khiên có hiệu lực (5000 ms = 5 giây)
target_collected=True



def handle_power_up_catch(power_up):
   global score, lives, wrong_hits, shield_active, shield_timer
 
   if power_up[1] == "ExtraLife":
       if lives < 3:  # Kiểm tra xem số mạng có nhỏ hơn 3 không
           lives += 1  # Cộng thêm mạng sống
           print("Extra Life collected! Lives:", lives)
       else:
           print("Lives are already at the maximum (3)!")
   elif power_up[1] == "Shield":
       shield_active = True
       shield_timer = pg.time.get_ticks()
       print("Shield Activated!")

def spawn_item():
   x_position = randint(20, 250)
   item_type = choice(list(item_images.keys()) + list(power_up_images.keys()))  # Randomly select an item or power-up
   if item_type in item_images:
       item_rect = item_images[item_type].get_rect(topleft=(x_position, 0))
   else:
       item_rect = power_up_images[item_type].get_rect(topleft=(x_position, 0))

   items.append((item_rect, item_type))  # Add item to the list


# Global variable to track the number of fallen items
items_fallen_count = 0
def move_items():
   global score, lives, wrong_hits, shield_active, target_collected,items_fallen_count
   margin = 30
   for item in items[:]:
       item[0].y += 5  # Move items down the screen
       if (car_rect.left < item[0].left and car_rect.right + margin > item[0].right and
           car_rect.top < item[0].top and car_rect.bottom + margin > item[0].bottom):

           if shield_active:
               print("Shield blocked the hit, but score is still updated!")
               if item[1] == "Target":
                   score += 1
                   print("Target collected! Score:", score)
                   spawn_firework(car_rect.centerx, car_rect.centery)
               items.remove(item)  
               continue  
           else:
               if item[1] == "Target":
                   score += 1
                   print("Target collected! Score:", score)
                   spawn_firework(car_rect.centerx, car_rect.centery)
                   if score == 6:
                       level_up()  
               elif item[1] in ["Other1", "Other2", "Other3"]:
                   lives -= 1
                   print("Wrong hit! Lost 1 life. Lives remaining:", lives)
               elif item[1] == "ExtraLife":
                   handle_power_up_catch(item)  # Lấy vật phẩm ExtraLife
               elif item[1] == "Shield":
                   handle_power_up_catch(item) 
               items.remove(item)  # Xóa vật phẩm sau khi va chạm
       elif item[0].top > screen.get_height():
           # Nếu vật phẩm đã rơi ra ngoài màn hình, xóa nó khỏi danh sách
           items.remove(item)
           items_fallen_count += 1

def check_shield_status():
   global shield_active, shield_timer
   if shield_active and pg.time.get_ticks() - shield_timer > shield_duration:
       shield_active = False  # Tắt khiên sau khi hết thời gian
       print("Shield Deactivated!")
     
def draw_shield():
   if shield_active:
       pg.draw.circle(screen, (0, 255, 0), car_rect.center, 50, 5)  # Vẽ vòng tròn xanh lá (khiên)
     
def draw_items():
   for item_rect, item_type in items:
       if item_type in item_images:
           screen.blit(item_images[item_type], item_rect)
       else:
           screen.blit(power_up_images[item_type], item_rect)



def handle_item_catch(item):
   global score, lives, wrong_hits, has_answered, game_over, target_collected
   if item[1] == targets[current_target_index]:
       score += 1
       target_collected = True
       if score == 6:
           level_up()
   else:
       lives -= 1
       if lives <= 0:
           if wrong_hits == 0 and not has_answered:  # First time losing and haven't answered yet
               ask_random_question()
           else:  # Second time losing (game over)
               wrong_hits += 1
               handle_game_over()




def show_target_message():
   font = pg.font.Font(font_xin, 24)
   message = f"Collect the {targets[current_target_index]}! Target is a cargo box"
   text = font.render(message, True, (255, 0, 0))  # Màu đỏ
   screen.blit(text, (60, 40))  # Vị trí hiển thị thông báo
   pg.display.flip()
targets = ["Target", "Other1", "Other2", "Other3"]  # Danh sách các mục tiêu
current_target_index = 0  # Mục tiêu hiện tại

def level_up():
    global score, level, fall_speed, current_target_index, car_speed

    level += 1
    current_target_index = (current_target_index + 1) % len(targets)  # Chuyển sang mục tiêu tiếp theo
    print(f"Level {level} Up! New target: {targets[current_target_index]}")

    # Tăng tốc độ rơi (fall_speed) cho các vật phẩm
    if level == 2:  # Khi lên cấp 2
        fall_speed +=45  # Tăng tốc độ rơi thêm 40
        car_speed = 15 # Tăng tốc độ xe lên 13 khi lên cấp 2
    elif level > 2:  # Nếu đã qua cấp 2
        fall_speed += 5  # Tăng tốc độ rơi thêm 2 cho các cấp tiếp theo
        car_speed += 5  # Tăng tốc độ xe thêm 2 cho các cấp tiếp theo

    show_level_up_screen()
    spawn_firework(200, 300)
    pg.time.delay(2000)
    show_target_message()  # Hiển thị thông báo mới sau khi level up
    

 
def show_level_up_screen():
   screen.blit(level_up_background, (0, 0))
   font = pg.font.Font(font_xin, 72)
   level_up_text = font.render(f"Level {level} Up!", True, (0, 255, 0))
   screen.blit(level_up_text, (100, 250))


   # Display the score
   score_text = font.render(f"Score: {score}", True, (255, 255, 255))
   screen.blit(score_text, (100, 350))


   pg.display.flip()  # Update the display to show "Level Up" text
   pg.time.delay(2000)  # Wait for 2 seconds before continuing the game
# Ask a random trivia question when player loses first time




fireworks=[]
class Firework:
   def __init__(self, x, y):
       self.x = x
       self.y = y
       self.color = choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])  # Random color
       self.size = randint(10, 15)   # Random size
       self.velocity = [randint(-3, 3), randint(-10,-5)]  # Random velocity for particle
       self.lifespan = 255  # Maximum transparency
       self.alpha = self.lifespan  # Transparency value








   def update(self):
       # Move the particle and decrease its alpha (fade effect)
       self.x += self.velocity[0]
       self.y += self.velocity[1]
       self.alpha -= 5  # Decrease alpha to simulate fading


       if self.alpha < 0:
           self.alpha = 0  # Avoid negative alpha value, ensuring it disappears




   def draw(self, screen):
       # Draw a circle with decreasing alpha (transparency)
       pg.draw.circle(screen, self.color, (self.x, self.y), self.size)
     
# Update fireworks to remove faded fireworks
def update_fireworks():
   global fireworks
   # Chỉ cập nhật và vẽ fireworks khi có ít hơn 5 quả pháo (hoặc một số lượng hợp lý)
   if len(fireworks) > 5:  # Giới hạn số lượng quả pháo đang tồn tại
       fireworks = [fw for fw in fireworks if fw.alpha > 0]  # Xóa các quả pháo đã biến mất
 
   for firework in fireworks[:]:
       firework.update()
       firework.draw(screen)
       if firework.alpha <= 0:
           fireworks.remove(firework)  # Xóa quả pháo khi hết hiệu lực
         
# Spawn firework when needed
def spawn_firework(x, y):
   fireworks.append(Firework(x, y))  # Add a new firework at the given position






class Particle:
   def __init__(self, x, y):
       self.x = x
       self.y = y
       self.size = randint(1,2)  # Kích thước particle
       self.color = (255, 255, 0)  # Màu vàng
       self.velocity = [randint(-1, 1), randint(1,3)]  # Vận tốc ngẫu nhiên
       self.lifespan=255
       self.alpha= self.lifespan



   # Trong firework/particle update
   def update(self):
       if self.x < 0 or self.x > screen.get_width() or self.y < 0 or self.y > screen.get_height():
           self.alpha = 0  # Loại bỏ particle nếu nó ra khỏi màn hình
       self.x += self.velocity[0]
       self.y += self.velocity[1]
       self.alpha -= 5
       if self.alpha < 0:
        self.alpha = 0  # Avoid negative alpha values




   def draw(self, screen):
       particle_surface = pg.Surface((self.size*2, self.size*2), pg.SRCALPHA)  # Tạo một Surface với alpha
       pg.draw.circle(particle_surface, (self.color[0], self.color[1], self.color[2], self.lifespan), (self.size, self.size), self.size)
       screen.blit(particle_surface, (self.x - self.size, self.y - self.size))  # Vẽ lên màn hình




def update_and_draw_particles(screen):
   # Cập nhật và vẽ tất cả particles
   for particle in particles[:]:
       particle.update()
       particle.draw(screen)
       # Xóa particle khi nó đã hết tuổi thọ
       if particle.lifespan == 0:
           particles.remove(particle)




# Khai báo danh sách particles
particles = []


# Hàm tạo particles cho xe
def create_car_particles(car_rect):
   # Tạo một số particles mỗi lần xe di chuyển
   for _ in range(5):  # Tạo ra 5 particle mỗi lần xe di chuyển
       particles.append(Particle(car_rect.centerx, car_rect.centery))




def ask_random_question():
   global paused, question_num,has_answered
   paused = True  
   has_answered=False 
   question_num = randint(0, len(questions) - 1) 

def handle_game_over():
   global game_over
   game_over = True
   print("Game Over!")
   show_game_over_screen()
   show_restart_screen()

def show_game_over_screen():
 
   screen.blit(game_over_background, (0, 0))
   font = pg.font.Font(font_xin, 72)  
   game_over_text = font.render("Game Over", True, (200, 0, 0))  
   screen.blit(game_over_text, (100, 250))  
   score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))  # White color
   screen.blit(score_text, (50, 350))
   pg.display.flip()  
   pg.time.delay(2000)  

paused = False
game_over_flag = False
last_spawn_time = pg.time.get_ticks()
hieuung()
chon_nhac()
play_intro_video()
show_start_screen()
# Biến toàn cục để theo dõi thời gian thông báo đã hiển thị
target_message_time, target_message_duration= None,3000  # Thời điểm hiển thị thông báo "Collect the Target item!" và thông báo hiển thị
message_shown, game_started = False, False
guess=None

def vienxe():
    def checkx():
        global move_left
        global move_right
        if car_rect.centerx <= 85:
            move_left = False
            car_rect.centerx = 85  

        if car_rect.centerx >= 325:
            move_right = False
            car_rect.centerx = 325  
    def checky():
        if car_rect.centery >= 600:
            car_rect.centery = 600 
     
        if car_rect.centery <= 0:
            car_rect.centery = 0 

    car_move_x = car_speed if move_right else -car_speed if move_left else 0
    car_move_y = car_speed if move_down else -car_speed if move_up else 0

    car_rect.centerx += car_move_x
    car_rect.centery += car_move_y

    checkx()
    checky()
# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Handle key press and release events for movement
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                move_right = True
            if event.key == pg.K_LEFT:
                move_left = True
            if event.key == pg.K_UP:
                move_up = True
            if event.key == pg.K_DOWN:
                move_down = True

            # Trivia question handling
            if paused:
               if event.key == pg.K_a:
                   guess = "A"
               elif event.key == pg.K_b:
                   guess = "B"
               elif event.key == pg.K_c:
                   guess = "C"
               elif event.key == pg.K_d:
                   guess = "D"
               if not has_answered:
                    if guess == answers[question_num]:  # Check if answer is correct
                            lives += 1  # Add 1 life for correct answer
                            wrong_hits = 0  # Reset wrong hits if correct
                            print(f"Correct! Lives: {lives}")  # Debugging output
                    else:
                            wrong_hits += 1
                            print("Incorrect! Game Over.")  # Debugging output
                            handle_game_over()


                    has_answered = True  # Mark the question as answered
                    paused = False  # Unpause the game after answering
                    print("Paused set to False, game resumes.")  # Debugging output


        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                move_right = False
            if event.key == pg.K_LEFT:
                move_left = False
            if event.key == pg.K_UP:
                move_up = False
            if event.key == pg.K_DOWN:
                move_down = False


    # Nếu trò chơi đang pause, chỉ vẽ câu hỏi và các lựa chọn câu trả lời
    if paused:
        background_question = pg.image.load("Pic/background_music.png")
        background_question = pg.transform.scale(background_question, (screen.get_width(), screen.get_height()))
        screen.blit(background_question,(0,0))
        font = pg.font.Font(font_xin, 24)
        question_text = font.render(questions[question_num], True, (0, 0, 0))
        question_rect= question_text.get_rect(topleft=(20, 50))
        pg.draw.rect(screen, (255, 255, 255), question_rect.inflate(20, 20)) # Nền màu trắng (đệm thêm 20 pixel mỗi hướng) 
        pg.draw.rect(screen, (0, 0, 0), question_rect.inflate(20, 20), 2)
        screen.blit(question_text,question_rect.topleft)
        

        for i, option in enumerate(options[question_num]):
            option_text = font.render(option, True, (0, 0, 0))
            # Tạo khung chữ nhật xung quanh 
            option_rect = option_text.get_rect(topleft=(20, 100 + i * 40)) 
            pg.draw.rect(screen, (255, 255, 255), option_rect.inflate(20, 20)) # Nền màu trắng (đệm thêm 20 pixel mỗi hướng)
            pg.draw.rect(screen, (0, 0, 0), option_rect.inflate(20, 20), 2)
            screen.blit(option_text, option_rect.topleft)


        pg.display.update()
        continue  # Ngừng vòng lặp game tại đây và chờ người chơi trả lời


    # Các hoạt động khác chỉ tiếp tục nếu trò chơi không bị pause
    if not paused:
        check_shield_status()
        move_items()


    # Kiểm tra điều kiện game over
    if lives <= 0:
        if not has_answered:
            ask_random_question()  # Ask a question if lives are 0 and not answered yet
        else:
            handle_game_over()  # Handle game over if already answered


    # Vẽ đường và xe
    droad()
    screen.blit(car, car_rect)


    # Vẽ khiên và các vật phẩm
    draw_shield()
    draw_items()
    update_fireworks()


    # Cập nhật và vẽ particles
    create_car_particles(car_rect)
    update_and_draw_particles(screen)


    # Hiển thị điểm và số mạng
    font = pg.font.Font(font_xin, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (300, 10))


    # Cập nhật vị trí đường
    road_y_pos += 2
    if road_y_pos >= 600:
        road_y_pos = 0


    if game_over_flag:
        continue


    if not paused and not game_over_flag:
        if not game_started:
            spawn_firework(200, 300)
            if target_message_time is None:
                target_message_time = pg.time.get_ticks()


            show_target_message()


            if pg.time.get_ticks() - target_message_time >= target_message_duration:
                game_started = True
                target_message_time = None
                message_shown = True


        if game_started:
            # Handle movement after the game starts
            vienxe()


            # Cập nhật spawn vật phẩm mỗi giây
            if pg.time.get_ticks() - last_spawn_time >= 1000 and not paused:
                spawn_item()
                last_spawn_time = pg.time.get_ticks()


        # Hiển thị thông báo nếu cần
        if score == 0 and not message_shown:
            if target_message_time is None:
                target_message_time = pg.time.get_ticks()
            show_target_message()


            if pg.time.get_ticks() - target_message_time >= target_message_duration:
                target_message_time = None
                message_shown = True


    pg.display.flip()  # Update the screen once after drawing everything


    clock.tick(90)  # Control the frame rate




