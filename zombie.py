import random

from pico2d import load_image, draw_rectangle, clamp

import game_framework
import game_world

# 좀비 달리기 속력: km/h -> 픽셀/초
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 좀비 애니메이션 속도: 0.5초에 10프레임
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

MIN_X, MAX_X = 800, 1600  # 좀비가 오가는 구간

# [과제 참고] 좀비
#   - 크기 200 이 draw 와 get_bb 에 따로 박혀 있다 -> 크기를 바꾸는 문제면 self.size 하나로 (조각 Z)
#     크기를 바꾸면 y = 50 + size / 2 로 다시 맞춰야 발이 땅에 붙는다 (지금 y=150 = 50 + 100)
#   - handle_collision 이 아직 없다 -> 그룹에 넣으면 꼭 만든다
#   - 이미지 폴더에 Dead (1)~(12), Attack (1)~(8), Idle (1)~(10) 도 있다 (지금은 Walk 만 씀)
#   - 박스가 bottom 50 이라 바닥 공(top 70.5)과 늘 겹친다 -> 'zombie:ball' 에서 other.stopped 확인


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images is None:
            Zombie.images = {
                'Walk': [load_image(f'./zombie/Walk ({i}).png') for i in range(1, 11)]
            }

    def __init__(self):
        self.load_images()
        self.x, self.y = random.randint(MIN_X, MAX_X), 150
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1, 1])

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION
        self.x += self.dir * RUN_SPEED_PPS * dt
        if self.x > MAX_X:
            self.dir = -1
        elif self.x < MIN_X:
            self.dir = 1
        self.x = clamp(MIN_X, self.x, MAX_X)

    def draw(self):
        image = Zombie.images['Walk'][int(self.frame)]
        if self.dir < 0:
            image.composite_draw(0, 'h', self.x, self.y, 200, 200)
        else:
            image.draw(self.x, self.y, 200, 200)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    # [과제] 충돌 처리는 여기에 추가
    # def handle_collision(self, group, other):
    #     if group == 'zombie:ball':      # 공에 맞음 (other.stopped 면 무시)
    #         ...
    #     elif group == 'boy:zombie':     # 소년과 닿음 (매 프레임 호출됨)
    #         ...
