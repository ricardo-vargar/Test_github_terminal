"""
Launcher demonstrating the Sotelo game with a bot.

Usage examples:
- Bot plays on medium:  python trying_codex.py --mode bot --difficulty medium
- You play on easy:     python trying_codex.py --mode human --difficulty easy
"""

import argparse
import random


class SoteloGame:
    DIFFICULTY_LEVELS = {
        'easy': {'size': 5, 'obstacles': 5},
        'medium': {'size': 7, 'obstacles': 12},
        'hard': {'size': 10, 'obstacles': 25},
    }

    def __init__(self, difficulty='easy'):
        config = self.DIFFICULTY_LEVELS.get(difficulty, self.DIFFICULTY_LEVELS['easy'])
        self.size = config['size']
        self.num_obstacles = config['obstacles']
        self.reset_board()
        while not self.has_valid_path():
            self.reset_board()
        self.move_count = 0

    def reset_board(self):
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.player_pos = (0, 0)
        self.goal_pos = (self.size - 1, self.size - 1)
        self.board[self.player_pos[0]][self.player_pos[1]] = 'P'
        self.board[self.goal_pos[0]][self.goal_pos[1]] = 'G'
        self.obstacles = self.generate_obstacles()

    def has_valid_path(self):
        def dfs(x, y, visited):
            if (x, y) == self.goal_pos:
                return True
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.size
                    and 0 <= ny < self.size
                    and self.board[nx][ny] != '#'
                    and (nx, ny) not in visited
                ):
                    if dfs(nx, ny, visited):
                        return True
            return False

        return dfs(self.player_pos[0], self.player_pos[1], set())

    def generate_obstacles(self):
        obstacles = set()
        while len(obstacles) < self.num_obstacles:
            pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if pos != self.player_pos and pos != self.goal_pos and pos not in obstacles:
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
        moves = {'up': (x - 1, y), 'down': (x + 1, y), 'left': (x, y - 1), 'right': (x, y + 1)}
        if direction in moves:
            nx, ny = moves[direction]
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] != '#':
                self.board[x][y] = '.'
                self.player_pos = (nx, ny)
                self.move_count += 1
                if self.player_pos == self.goal_pos:
                    self.board[nx][ny] = 'P'
                    self.display_board()
                    print("Congratulations! You reached the goal!")
                    print(f"Total moves: {self.move_count}")
                    return True
                self.board[nx][ny] = 'P'
        return False


def get_arrow():
    # Try getch; fall back to WASD input if not available.
    try:
        import getch  # type: ignore
    except Exception:
        key = input("Enter move (w/a/s/d): ").strip().lower()
        return {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}.get(key)

    c1 = getch.getch()
    if c1 == '\x1b':
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


class SoteloBot:
    def __init__(self, game: SoteloGame):
        self.game = game

    def find_path(self):
        def heuristic(pos):
            return abs(pos[0] - self.game.goal_pos[0]) + abs(pos[1] - self.game.goal_pos[1])

        def get_neighbors(pos):
            neighbors = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < self.game.size and 0 <= ny < self.game.size and self.game.board[nx][ny] != '#':
                    neighbors.append((nx, ny))
            return neighbors

        start = self.game.player_pos
        goal = self.game.goal_pos
        frontier = [(heuristic(start), 0, start, [])]
        visited = set()

        while frontier:
            f_best, cost, current, path = min(frontier)
            frontier.remove((f_best, cost, current, path))

            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for next_pos in get_neighbors(current):
                if next_pos not in visited:
                    new_path = path + [next_pos]
                    new_cost = cost + 1
                    frontier.append((new_cost + heuristic(next_pos), new_cost, next_pos, new_path))

        return []

    def get_move(self, current, next_pos):
        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]
        if dx == -1:
            return 'up'
        if dx == 1:
            return 'down'
        if dy == -1:
            return 'left'
        if dy == 1:
            return 'right'
        return None

    def play(self):
        path = self.find_path()
        if not path:
            print("No solution found!")
            return

        current = self.game.player_pos
        for next_pos in path:
            move = self.get_move(current, next_pos)
            self.game.move_player(move)
            self.game.display_board()
            current = next_pos


def main():
    parser = argparse.ArgumentParser(description="Run Sotelo Game in human or bot mode.")
    parser.add_argument('--mode', choices=['human', 'bot'], default='bot', help='Play yourself or let the bot play')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], default='easy', help='Board size and obstacle count')
    args = parser.parse_args()

    game = SoteloGame(args.difficulty)
    game.display_board()

    if args.mode == 'bot':
        print("Bot is playing...")
        bot = SoteloBot(game)
        bot.play()
    else:
        print("You are playing. Use arrow keys or WASD fallback.")
        while True:
            move = get_arrow()
            if move in ['up', 'down', 'left', 'right']:
                if game.move_player(move):
                    break
                game.display_board()
            else:
                print("Invalid key. Use arrows or WASD.")


if __name__ == '__main__':
    main()
