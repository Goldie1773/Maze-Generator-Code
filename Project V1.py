import pygame
import sys
import csv
import random
from datetime import date

pygame.init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

cols = 10
rows = 10

width = 600
height = 600
wr = width/cols
hr = height/rows

screen = pygame.display.set_mode([width, height])
screen_rect = screen.get_rect()
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.visited = False
        self.walls = [True, True, True, True]

    def show(self, color=BLACK):
        if self.walls[0]:
            pygame.draw.line(screen, color, [self.x*hr, self.y*wr],       [self.x*hr+hr, self.y*wr], 2)
        if self.walls[1]:
            pygame.draw.line(screen, color, [self.x*hr+hr, self.y*wr],    [self.x*hr+hr, self.y*wr + wr], 2)
        if self.walls[2]:
            pygame.draw.line(screen, color, [self.x*hr+hr, self.y*wr+wr], [self.x*hr, self.y*wr+wr], 2)
        if self.walls[3]:
            pygame.draw.line(screen, color, [self.x*hr, self.y*wr+wr],    [self.x*hr, self.y*wr], 2)

    def show_block(self, color):
        if self.visited:
            pygame.draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-2, wr-2])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

current = grid[0][0]
visited = [current]
completed = False


def breakwalls(a, b):
    if a.y == b.y and a.x > b.x:
        grid[b.x][b.y].walls[1] = False
        grid[a.x][a.y].walls[3] = False
    if a.y == b.y and a.x < b.x:
        grid[a.x][a.y].walls[1] = False
        grid[b.x][b.y].walls[3] = False
    if a.x == b.x and a.y < b.y:
        grid[b.x][b.y].walls[0] = False
        grid[a.x][a.y].walls[2] = False
    if a.x == b.x and a.y > b.y:
        grid[a.x][a.y].walls[0] = False
        grid[b.x][b.y].walls[2] = False


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, hr-2, wr-2)
        self.x = int(x)
        self.y = int(y)
        self.colour = (255, 0, 0)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 5

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect)

    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(self.x, self.y, hr-2, wr-2)


def readMyFiles():
    questionsAndAnswers = []
    correctAnswers = []

    with open('questions.txt', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            questionsAndAnswers.append(row)

    return questionsAndAnswers


def game(questions, answers, correctAnswers):
    score = 0
    counter = 0
    numberOfQuestions = len(questions)
    while not counter == numberOfQuestions:
        print(questions[counter])
        print(answers[counter])
        userAnswer = input('\nWhat is the correct answer?\n')
        if userAnswer == correctAnswers[counter]:
            print('Well done! That is correct.')
            score += 1
        else:
            print('Better luck next time, that is not correct.')
        counter += 1

    return score


def shuffleSplit(qna):
    random.shuffle(qna)
    questions = []
    answers = []
    correctAnswers = []
    for q in qna:
        questions.append(q[0])
        correctAnswers.append(q[1])
        del q[0]
        random.shuffle(q)
        answers.append(q)

    return (questions, answers, correctAnswers)


def exportScores(score, ):
    with open('scores.txt', mode='a') as scores:
        scores = csv.writer(scores, delimiter='\t')

        today = date.today()
        dateFormat = today.strftime("%d/%m/%Y")

        scores.writerow([dateFormat, score])


player = Player(2, 2)


while not done:
    clock.tick(60)
    screen.fill(BLACK)
    if not completed:
        grid[current.x][current.y].visited = True
        got_new = False
        temp = 10

        while not got_new and not completed:
            r = random.randint(0, len(current.neighbors)-1)
            Tempcurrent = current.neighbors[r]
            if not Tempcurrent.visited:
                visited.append(current)
                current = Tempcurrent
                got_new = True
            if temp == 0:
                temp = 10
                if len(visited) == 0:
                    completed = True
                    break
                else:
                    current = visited.pop()
            temp = temp - 1

        if not completed:
            breakwalls(current, visited[len(visited)-1])

        current.visited = True
        current.show_block(WHITE)

    for i in range(rows):
        for j in range(cols):
            grid[i][j].show(WHITE)
            # grid[i][j].show_block(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            questionsAndAnswers = readMyFiles()
            questions, answers, correctAnswers = shuffleSplit(questionsAndAnswers)
            score = game(questions, answers, correctAnswers)
            exportScores(score)
            print('\nYour score is', str(score))
            sys.exit()
        if event.type == pygame.KEYDOWN and completed:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            if event.key == pygame.K_UP:
                player.up_pressed = True
            if event.key == pygame.K_DOWN:
                player.down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False
    player.rect.clamp_ip(screen_rect)

    if player.x <= 2:
        player.left_pressed = False
        player.x = 2
    if player.y <= 2:
        player.up_pressed = False
        player.y = 2
    if player.x >= width-(wr-2):
        player.right_pressed = False
        player.x = width-(wr-2)
    if player.y >= height-(wr-2):
        player.down_pressed = False
        player.y = height-(wr-2)

    player.draw(screen)
    player.update()
    pygame.display.flip()
