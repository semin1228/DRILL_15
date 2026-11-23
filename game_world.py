# =============================================================================
# [과제 참고] 충돌 처리 4단계 (슬라이드 43쪽)
#   1. 충돌할 객체에 get_bb() -> (left, bottom, right, top)
#   2. draw() 에 draw_rectangle(*self.get_bb()) 로 박스 보이기
#   3. 그룹 'a:b' 로 A, B 등록: add_collision_pairs(group, a, b)
#      - 게임 중에 새로 생긴 객체(던진 공)는 생길 때 바로 등록, 이미 등록된 쪽은 None
#   4. play_mode.update() 에서 update() 다음에 handle_collision()
#      -> 겹치면 a.handle_collision(group, b), b.handle_collision(group, a)
#      -> 그룹에 넣은 객체는 모두 handle_collision 이 있어야 한다 (없으면 AttributeError)
# 함수 이름: 내 것은 add_collision_pairs / handle_collision,
#            교수님 것은 add_collision_pair / handle_collisions. 섞어 쓰지 말 것
# 정답 조각: 이 저장소 맨 위 collision_prep\puzzle_answers.py
# =============================================================================
world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI

def add_oject(o, depth=1):
    world[depth].append(o)

def add_objects(ol, depth=1):
    world[depth] += ol

def remove_collision_object(o):
    # 충돌 그룹에서도 제거해야, 사라진 객체와 계속 충돌하지 않는다
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o) 

def remove_object(o):
    # 월드에서 지우면 충돌 그룹에서도 지운다 (안 지우면 사라진 공을 계속 줍는다)
    # [과제] 죽는 애니메이션처럼 '화면엔 남고 충돌만 끄기' 는 remove_collision_object(o) 만 부른다
    # 이미 지운 객체를 또 지워도 조용히 넘어간다 (슬라이드는 여기서 ValueError 를 낸다)
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

def update():
    for layer in world:
        for o in layer[:]:
            o.update()

def render():
    for layer in world:
        for o in layer[:]:
            o.draw()

def clear():
    # [과제] 모드를 다시 시작하는 문제면 여기에 collision_pairs.clear() 추가 (조각 0-2)
    for layer in world:
        layer.clear()

# 두 박스가 안 겹치는 경우 4개만 걸러 내면 나머지는 겹침.
# [과제] 원 충돌(7-b): 맨 앞에 두 객체 모두 radius 가 있으면 중심 거리 비교
# [과제] 박스 여러 개(8번): 박스 튜플 두 개를 받는 collide_bb 로 빼서 재사용
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

collision_pairs = {}

def add_collision_pairs(group, a, b): 
    if group not in collision_pairs: # 처음 등록되는 충돌 그룹이면, 충돌 그룹을 생성
        collision_pairs[group] = [[], []] # a와 b를 담을 리스트 2개를 생성
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

# 그룹마다 A 쪽 x B 쪽을 모두 검사. 겹쳐 있는 동안은 '매 프레임' 호출된다 (1초에 60번)
# [과제] 공 하나가 좀비 둘에 동시에 닿는 문제면, 안쪽 for 맨 앞에 지워진 객체 건너뛰기 추가 (조각 0-1)
#        if a not in pairs[0]: break
#        if b not in pairs[1]: continue
def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0][:]:      # 순회 중 제거될 수 있으므로 복사본으로 순회
            for b in pairs[1][:]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

