from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass
from ball import Ball
from zombie import Zombie
import random

boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    # 객체들을 생성
    boy = Boy()
    grass = Grass()
    global balls
    balls = [Ball(random.randint(100, 1500), 60, 0) for _ in range(30)]

    # 생성된 객체들을 game_world에 등록
    game_world.add_oject(boy)
    game_world.add_oject(grass, 0)
    game_world.add_objects(balls, 1)

    # 생성된 객체들의 충돌 관계를 등록
    game_world.add_collision_pairs("boy:ball", boy, None)
    for ball in balls:
        game_world.add_collision_pairs("boy:ball", None, ball)

    # [과제] 여기에 객체 생성과 그룹 등록을 추가한다
    #   땅과 던진 공  : add_collision_pairs('grass:ball', grass, None)   (공 쪽은 boy.fire_ball 에서)
    #   좀비 4마리    : global zombies / zombies = [Zombie() for _ in range(4)] / add_objects(zombies, 1)
    #                   (Zombie 는 import 만 되어 있고 아직 안 만든다)
    #   좀비와 공     : for zombie in zombies: add_collision_pairs('zombie:ball', zombie, None)
    #   소년과 좀비   : ('boy:zombie', boy, None) + 좀비마다 ('boy:zombie', None, zombie)
    #   grass 는 init 안의 지역 변수라 다른 함수에서 쓰려면 global 로




def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    # 순서: 모두 움직인 다음 충돌 검사 -> render
    # [과제] 결과가 나면 멈추는 문제(2-b)는 맨 앞에서 return, 결과 판정은 충돌 검사 뒤에
    game_world.update()
    game_world.handle_collision()
    

def render():
    clear_canvas()
    game_world.render()
    # [과제] CLEAR!, 결과 같은 글자는 여기 (update_canvas 전에). 폰트는 init 에서 load_font 로 한 번만
    update_canvas()









