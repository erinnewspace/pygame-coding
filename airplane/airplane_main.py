

import random
import pygame
from airplane_object import GameObject # from 폴더명.파일명 import 클래스명
import sqlite3

pygame.init()

screen_width = 480
screen_height = 480
screen = pygame.display.set_mode([screen_width,screen_height])

id = 'erin'

kill_value = 0
loss_value = 0

pygame.display.set_caption('Airplane Game')
clock = pygame.time.Clock()

my_plane = GameObject(screen)
my_plane.load_image('E:\\ccube_coding\\c3coding\\Python class\\pygame\\airplane\\images\\plane.png')
my_plane.set_size(50, 80)
my_plane.set_position(GameObject.center_below)
my_plane.moving = 5

ufo = GameObject(screen)
ufo.load_image('E:\\ccube_coding\\c3coding\\Python class\\pygame\\airplane\\images\\ufo.png')
ufo.set_size(50, 80)
ufo.set_position(GameObject.center_upper)

# 충돌 함수
def is_crash(a, b) :
    x_condition = a.x -b.width <= b.x and b.x <= a.x + a.width
    y_condition = a.y - b.height <= b.y and b.y <= a.y + a.height
    return x_condition and y_condition

sky_blue = (112,202,227)

bullet_list = list() # 총알이 만들어 지고 저장되는 리스트
rock_list = list()
delete_list = list() # 총알(돌)이 화면을 나가면 메모리에서 삭제할 리스트
count = 0

running = True
while running:
    clock.tick(60)  

    random_value = random.random()
    if random_value > 0.98 : # 2%  
        rock = GameObject(screen)
        rock.load_image('E:\\ccube_coding\\c3coding\\Python class\\pygame\\airplane\\images\\rock.png')        
        rock.set_size(15, 15)
        rock.x = random.randrange(my_plane.width/2, screen_width - my_plane.width/2)
        rock.y = 10
        rock.moving = 3
        rock_list.append(rock)

    delete_list.clear()
    for index, rock in enumerate(rock_list) : 
        rock.y += rock.moving        
        if rock.y >= screen_height :
            delete_list.append(index)
            loss_value += 1 # 놓친 rock count 증가  
    
    for rock_index in delete_list :         
        del rock_list[rock_index]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            # account 정보
            # database 연결          
            conn = sqlite3.connect("airplane.db")
            cur = conn.cursor()

            # table 생성
            cur.execute('create table if not exists airplane_info(id text primary key, name text, killed int, missed int)')            

            # data 검색
            cur.execute(f'select * from airplane_info where name ="{id}"')
            if len(cur.fetchall()) != 0 :
                cur.execute(f"update airplane_info set killed={kill_value}, missed={loss_value} where name='{id}'")
            else :
            # 데이터 추가
                cur.execute('insert into airplane_info values(?, ?,?,?);', (str(random.random()), id, kill_value, loss_value))            
            conn.commit()
            
            # database 해제
            conn.close()

            # system 종료
            running = False
 
    key_event = pygame.key.get_pressed()

    if key_event[pygame.K_LEFT]:
        my_plane.x -= my_plane.moving
        if my_plane.x <= 0 : 
            my_plane.x = 0

    if key_event[pygame.K_RIGHT]:
        my_plane.x  += my_plane.moving
        if my_plane.x >= screen_width - my_plane.width :
            my_plane.x = screen_width  - my_plane.width

    if key_event[pygame.K_UP]:
        my_plane.y -= my_plane.moving

    if key_event[pygame.K_DOWN]:
        my_plane.y += my_plane.moving
        if my_plane.y >= screen_height- my_plane.height:
            my_plane.y = screen_height- my_plane.height
    
    if key_event[pygame.K_SPACE] and count%8 == 0 : # 총알 만들기
        bullet = GameObject(screen)        
        bullet.load_image('E:\\ccube_coding\\c3coding\\Python class\\pygame\\airplane\\images\\bullet.png')
        bullet.set_size(15, 10)
        bullet.x = round(my_plane.x + my_plane.width/2-bullet.width/2)
        bullet.y = my_plane.y - bullet.height - 10
        bullet.moving = 5

        bullet_list.append(bullet)        
    count = count + 1

    delete_list.clear()
    for index, bullet in enumerate(bullet_list) :
        bullet.y -= bullet.moving 
        if bullet.y <= 0 :
            delete_list.append(index)            

    for index in delete_list : # 화면에 나간 bulllet 은 메모리에서 삭제됨.
        del bullet_list[index]          

    d_bu_list = [] # 충돌시 삭제될 bullet index list
    d_ro_list = [] # 충돌시 삭제될 rock index list
    for i, bu in enumerate(bullet_list) :
        for j, ro in enumerate(rock_list) :
            if is_crash(bu,ro) :
                d_bu_list.append(i)
                d_ro_list.append(j)
                kill_value += 1 # kill value count 증가
    # 삭제    
    for d in d_bu_list :        
        del bullet_list[d]
    for d in d_ro_list :        
        del rock_list[d]

    screen.fill(sky_blue)
    my_plane.show()
    ufo.show()

    for rock in rock_list :         
        rock.show()

    for bu in bullet_list :
        bu.show()

    # kill,loss 정보 표시
    font = pygame.font.Font('C:\\Windows\\Fonts\\arialbd.ttf', 15)    
    info = font.render(f'[{id}] killed : {kill_value}, loss : {loss_value}', True, (255, 255, 0))
    screen.blit(info, (10, 10))
 
    pygame.display.update()