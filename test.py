import random
import getch
#import tkinter as tk
#from tkinter import messagebox

class SoteloGame:
    def __init__(self, size=5):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.player_pos = (0, 0)
        self.goal_pos = (size-1, size-1)
        self.board[self.player_pos[0]][self.player_pos[1]] = 'P'
        self.board[self.goal_pos[0]][self.goal_pos[1]] = 'G'
        self.obstacles = self.generate_obstacles()

    def generate_obstacles(self):
        obstacles = set()
        while len(obstacles) < self.size:
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if pos != self.player_pos and pos != self.goal_pos:
                obstacles.add(pos)
        for x, y in obstacles:
            self.board[x][y] = '#'
        return obstacles

    def display_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def move_player(self, direction):
        x, y = self.player_pos
        moves = {'up': (x-1, y), 'down': (x+1, y), 'left': (x, y-1), 'right': (x, y+1)}
        if direction in moves:
            nx, ny = moves[direction]
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] != '#':
                self.board[x][y] = '.'
                self.player_pos = (nx, ny)
                if self.player_pos == self.goal_pos:
                    self.board[nx][ny] = 'P'
                    self.display_board()
                    print("Congratulations! You reached the goal!")
                    return True
                self.board[nx][ny] = 'P'
        return False

def get_arrow():
    c1 = getch.getch()
    if c1 == '\x1b':  # Escape character
        c2 = getch.getch()
        if c2 == '[':
            c3 = getch.getch()
            if c3 == 'A':
                return 'up'
            elif c3 == 'B':
                return 'down'
            elif c3 == 'C':
                return 'right'
            elif c3 == 'D':
                return 'left'
    return None

def main():
    print("Welcome to Sotelo Game!")
    print("Use arrow keys to move.")
    game = SoteloGame()
    game.display_board()
    while True:
        print("Press an arrow key to move:")
        move = get_arrow()
        if move in ['up', 'down', 'left', 'right']:
            if game.move_player(move):
                break
            game.display_board()
        else:
            print("Invalid key. Use arrow keys.")

if __name__ == "__main__":
    main()

    