from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
        self.ruler_image = load_image('ruler.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        self.ruler_image.draw(800, 350)

    # 바닥 공(y=60, 반지름 10.5)의 bottom 이 49.5 라 땅과 겹친다 -> 바닥 공을 grass:ball 에 넣지 말 것
    # [과제] 슬라이드 값은 0, 0, 1600 - 1, 50 (조각 0-5)
    def get_bb(self):
        return 0, 0, 1600, 60

    # [과제] grass:ball, grass:zombie 그룹에 넣으면 할 일이 없어도 필요:
    #   def handle_collision(self, group, other):
    #       pass
