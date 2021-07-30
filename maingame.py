size = 40
back_color = (102,167,67)

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.x = size * 3
        self.y = size * 3

    #to draw the apple on surface 
    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
    
    def move(self):
        self.x = random.randint(1,24)*size
        self.y = random.randint(1,19)*size

class Snake:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/block.jpg').convert()
        self.direction = 'right'
        self.length = 3
        self.score = 0
        self.x = [40]*self.length
        self.y = [40]*self.length
        self.game_time = 0.26

        
    
    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size 
        self.draw()
    
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
    
    def increase_length(self):
        self.score += 1
        if self.game_time >= 0.01:
            self.game_time -= 0.01
        else:
            self.game_time = 0.01
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Block and Apple game by Rishabh Bilwal")
        self.play_back_music()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000,800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        
    
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
    
    def play_back_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()
    
    def render_back(self):
        bg = pygame.image.load('resources/background.jpg')
        self.surface.blit(bg,(0,0))

    
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False
    
    def play(self):
        self.render_back()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound('resources/ding.mp3')
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound('resources/crash.mp3')
                pygame.mixer.Sound.play(sound)
                raise "Collision Occured"
        
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            sound = pygame.mixer.Sound('resources/crash.mp3')
            pygame.mixer.Sound.play(sound)
            raise "Hit the boundary error"

    
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.score}",True,(200,200,200))
        self.surface.blit(score,(850,10))
    
    def show_game_over(self):
        self.render_back()
        font = pygame.font.SysFont('arial',50)
        line1 = font.render('GAME OVER!!', True,(200,200,200))
        self.surface.blit(line1,(200,300))
        font1 = pygame.font.SysFont('arial',30)
        line2 = font1.render(f'Your score is {self.snake.score}', True,(200,200,200))
        self.surface.blit(line2,(200,360))
        line3 = font1.render('To play again press Enter. To exit press Escape!', True,(200,200,200))
        self.surface.blit(line3, (200,400))

        pygame.display.flip()
        pygame.mixer.music.pause()
 
    


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        self.play_back_music()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.snake.game_time)

if __name__ == '__main__':
    import pygame
    from pygame.locals import *
    import time
    import random

    game = Game()
    game.run()


