import random
from turtle import *
from freegames import floor, vector
from turtle import TurtleGraphicsError

class PacmanGame:
    def __init__(self):
        # 게임 상태 초기화
        self.state = {'score': 0}
        self.path = Turtle(visible=False)
        self.writer = Turtle(visible=False)
        self.path.up()
        self.writer.up()
        
        # 성능 최적화를 위한 터틀 설정
        self.path.speed(0)
        self.writer.speed(0)
        
        # 게임 요소 초기화
        self.aim = vector(5, 0)
        self.pacman = vector(-40, -80)
        self.ghosts = [
            [vector(-180, 160), vector(5, 0)],
            [vector(-180, -160), vector(0, 5)],
            [vector(100, 160), vector(0, -5)],
            [vector(100, -160), vector(-5, 0)],
            [vector(0, 0), vector(5, 5)],
        ]
        
        # 게임 상태 변수
        self.cookies_left = 0
        self.power_up_duration = 0
        
        self._ghost_options = [
            vector(5, 0),
            vector(-5, 0),
            vector(0, 5),
            vector(0, -5),
        ]
        
        # 게임 맵
        self.tiles = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
            0, 3, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 3, 0, 0, 0, 0,
            0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]

    def square(self, x, y):
        """사각형 그리기"""
        self.path.goto(x, y)
        self.path.down()
        self.path.begin_fill()
        for _ in range(4):
            self.path.forward(20)
            self.path.left(90)
        self.path.end_fill()
        self.path.up()

    def offset(self, point):
        """좌표를 타일 인덱스로 변환"""
        x = (floor(point.x, 20) + 200) / 20
        y = (180 - floor(point.y, 20)) / 20
        index = int(x + y * 20)
        return index if 0 <= index < len(self.tiles) else None

    def valid(self, point):
        """유효한 이동인지 확인"""
        index = self.offset(point)
        if index is None:
            return False
        if self.tiles[index] == 0:
            return False
        
        index = self.offset(point + 19)
        if index is None:
            return False
        if self.tiles[index] == 0:
            return False
        
        return True

    def world(self):
        """게임 월드 그리기"""
        bgcolor('black')
        self.path.color('blue')
        self.cookies_left = 0

        for index, tile in enumerate(self.tiles):
            if tile > 0:
                x = (index % 20) * 20 - 200
                y = 180 - (index // 20) * 20
                self.square(x, y)
                
                if tile == 1:  # 일반 쿠키
                    self.path.goto(x + 10, y + 10)
                    self.path.dot(2, 'white')
                    self.cookies_left += 1
                elif tile == 3:  # 파워 쿠키
                    self.path.goto(x + 10, y + 10)
                    self.path.dot(8, 'white')
                    self.cookies_left += 1

    def move(self):
        """게임 요소들의 이동 처리"""
        # 파워업 지속시간 감소
        if self.power_up_duration > 0:
            self.power_up_duration -= 1
        
        # 팩맨 이동
        writer = self.writer
        if self.valid(self.pacman + self.aim):
            self.pacman.move(self.aim)
        
        # 쿠키 먹기 처리
        index = self.offset(self.pacman)
        if index is not None:
            if self.tiles[index] == 1:  # 일반 쿠키
                self.tiles[index] = 2  # 먹은 상태로 변경
                self.state['score'] += 1
                self.cookies_left -= 1
                
                # 기존 맵을 지우고 다시 그리기
                x = (index % 20) * 20 - 200
                y = 180 - (index // 20) * 20
                
                # 해당 위치의 파란색 사각형만 다시 그리기
                self.path.color('blue')
                self.path.fillcolor('blue')
                self.square(x, y)
                
                if self.cookies_left == 0:
                    return self.win()
                    
            elif self.tiles[index] == 3:  # 파워 쿠키
                self.tiles[index] = 2
                self.power_up_duration = 30
                self.state['score'] += 5
                self.cookies_left -= 1
                
                # 기존 맵을 지우고 다시 그리기
                x = (index % 20) * 20 - 200
                y = 180 - (index // 20) * 20
                
                # 해당 위치의 파란색 사각형만 다시 그리기
                self.path.color('blue')
                self.path.fillcolor('blue')
                self.square(x, y)
                
                if self.cookies_left == 0:
                    return self.win()
        
        # 점수 표시
        writer.clear()
        writer.write(f"Score: {self.state['score']} Cookies left: {self.cookies_left}",
                    align="right", font=("Arial", 16, "normal"))
        
        clear()
        
        # 팩맨 그리기
        up()
        goto(self.pacman.x + 10, self.pacman.y + 10)
        dot(20, 'yellow')
        
        # 유령 이동 및 그리기
        for point, course in self.ghosts:
            if not self.valid(point + course):
                options = []
                for option in self._ghost_options:
                    if self.valid(point + option):
                        options.append(option)
                if options:
                    course.x, course.y = random.choice(options)
                continue
                
            point.move(course)
            
            up()
            goto(point.x + 10, point.y + 10)
            
            if self.power_up_duration > 0:
                dot(20, 'purple')
                if abs(self.pacman - point) < 20:
                    point.x = -180
                    point.y = 160
                    self.state['score'] += 20
            else:
                dot(20, 'red')
                if abs(self.pacman - point) < 20:
                    return self.lose()
        
        update()
        ontimer(self.move, 100)

    def change(self, x, y):
        """팩맨의 방향 변경"""
        if self.valid(self.pacman + vector(x, y)):
            self.aim.x, self.aim.y = x, y

    def win(self):
        """승리 화면 표시"""
        self.show_end_screen("YOU WIN!", 'yellow')

    def lose(self):
        """패배 화면 표시"""
        self.show_end_screen("GAME OVER!", 'red')

    def show_end_screen(self, message, text_color):
        """게임 종료 화면 표시"""
        clear()
        up()
        
        # 게임 결과 메시지
        goto(0, 100)
        pencolor(text_color)  # color 대신 pencolor 사용
        write(message, align="center", font=("Arial", 30, "normal"))
        
        # 최종 점수 표시
        goto(0, 50)
        pencolor('white')  # color 대신 pencolor 사용
        write(f"Final Score: {self.state['score']}", align="center", font=("Arial", 20, "normal"))
        
        # 버튼 그리기
        self.show_buttons()
        # 게임 입력 비활성화
        onkey(None, 'Right')
        onkey(None, 'Left')
        onkey(None, 'Up')
        onkey(None, 'Down')

    def show_buttons(self):
        """Play Again과 Exit 버튼 표시"""
        # Play Again 버튼
        self.draw_button(-70, -50, 'green', "Play Again")
        # Exit 버튼
        self.draw_button(70, -50, 'red', "Exit")
        update()
        onscreenclick(self.handle_click)

    def draw_button(self, x, y, button_color, text):
        """버튼 그리기"""
        up()
        goto(x, y)
        shape('square')
        shapesize(2, 4.5)
        fillcolor(button_color)
        stamp()
        goto(x, y - 5)
        pencolor('white')  # color 대신 pencolor 사용
        write(text, align="center", font=("Arial", 11, "bold"))

    def handle_click(self, x, y):
        """버튼 클릭 처리"""
        # Play Again 버튼 영역
        if -115 < x < -25 and -70 < y < -30:
            self.reset_game()
        # Exit 버튼 영역
        elif 25 < x < 115 and -70 < y < -30:
            bye()
            return True

    def reset_game(self):
        """게임 재시작"""
        self.__init__()
        clear()
        self.world()
        # 키 이벤트 재설정
        listen()
        onkey(lambda: self.change(5, 0), 'Right')
        onkey(lambda: self.change(-5, 0), 'Left')
        onkey(lambda: self.change(0, 5), 'Up')
        onkey(lambda: self.change(0, -5), 'Down')
        self.move()

    def setup_game(self):
        """게임 초기 설정"""
        try:
            resetscreen()
        except:
            pass
            
        setup(420, 420, 370, 0)
        hideturtle()
        tracer(False)
        self.writer.goto(160, 160)
        self.writer.color('white')
        listen()
        onkey(lambda: self.change(5, 0), 'Right')
        onkey(lambda: self.change(-5, 0), 'Left')
        onkey(lambda: self.change(0, 5), 'Up')
        onkey(lambda: self.change(0, -5), 'Down')
        self.world()
        self.move()
        done()

    def run(self):
        """게임 실행"""
        try:
            self.setup_game()
        except TurtleGraphicsError:
            pass

if __name__ == "__main__":
    game = PacmanGame()
    game.run()