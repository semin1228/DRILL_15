from pico2d import draw_rectangle, get_canvas_width, load_image

import game_world
import game_framework

# 단위: 픽셀, 초
LAUNCH_SPEED_X = 300.0
LAUNCH_SPEED_Y = 300.0
GRAVITY = 9.8 * (10.0 / 0.3)  # 9.8 m/s²를 픽셀/s²로 변환
GROUND_Y = 40


class Ball:
    images = {}

    def __init__(self, x, y, direction, ball_type=1):
        if ball_type not in Ball.images:
            Ball.images[ball_type] = load_image(
                'ball21x21.png' if ball_type == 1 else 'ball41x41.png')
        self.image = Ball.images[ball_type]
        self.x, self.y = x, y
        self.velocity_x = direction * LAUNCH_SPEED_X
        self.velocity_y = LAUNCH_SPEED_Y
        self.radius = 10.5 if ball_type == 1 else 20.5
        self.stopped = (direction == 0)  # direction 이 0이면 바닥에 놓인 공
        # [과제] 공 종류별 처리(7-a)면 self.ball_type = ball_type 저장 (지금은 저장 안 함)
        # [과제] 하늘에서 떨어지는 공(5-a)이면 인자 fall 을 받아 velocity_x, velocity_y = 0, stopped = False

    def update(self):
        if self.stopped:
            return
        dt = game_framework.frame_time
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt - 0.5 * GRAVITY * dt ** 2
        self.velocity_y -= GRAVITY * dt
        # [과제] 땅에서 멈추게 하려면(슬라이드 40쪽, 조각 0-3) 아래 조건의 땅 부분을
        #        'self.y < -self.radius' 로 바꾸고, 땅 닿기는 grass:ball 충돌에서 stopped = True
        if (self.x < -self.radius or self.x > get_canvas_width() + self.radius
                or self.y - self.radius <= GROUND_Y):
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius

    # [과제] 새 그룹은 여기에 elif group == '...': 로 추가
    #   'grass:ball'  : if not self.stopped: stopped = True (땅에 멈춤)
    #   'zombie:ball' : 좀비 맞히기면 if not self.stopped: 자기 삭제 (안 지우면 다음 프레임에 또 맞음)
    #                   좀비가 줍기면 if self.stopped: 자기 삭제
    #   other.stopped / self.stopped 로 '날아가는 공' 과 '바닥 공' 을 꼭 구분할 것
    def handle_collision(self, group, other):
        if group == 'boy:ball':
            game_world.remove_object(self)