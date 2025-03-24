import os
import random

class GameObject:
    def __init__(self, x, y, symbol, health=100, damage=20):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.health = health
        self.damage = damage

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 'P', 200, 30)

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 'T', 80, 15)

class Game:
    def __init__(self, width=10, height=8):
        self.width = width
        self.height = height
        self.map = [['.' for _ in range(width)] for _ in range(height)]
        self.player = Player(0, 0)
        self.enemies = []
        self.init_game()
        
    def init_game(self):
        # Добавляем стены
        for i in range(self.height):
            self.map[i][3] = '#'
            self.map[i][6] = '#'
        
        # Создаем врагов
        for _ in range(3):
            x = random.randint(4, self.width-1)
            y = random.randint(0, self.height-1)
            self.enemies.append(Enemy(x, y))
            
        self.update_map()

    def update_map(self):
        # Очищаем карту
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] != '#':
                    self.map[y][x] = '.'
        
        # Добавляем объекты
        self.map[self.player.y][self.player.x] = self.player.symbol
        for enemy in self.enemies:
            self.map[enemy.y][enemy.x] = enemy.symbol

    def print_map(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("===== ЗАБРОШЕННАЯ ФАБРИКА =====")
        for row in self.map:
            print(' '.join(row))
        print(f"Здоровье: {self.player.health}  Урон: {self.player.damage}")
        print("Управление: Стрелки - движение, A - атака")

    def move_player(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if self.map[new_y][new_x] == '.':
                self.player.x = new_x
                self.player.y = new_y
                return True
        return False

    def enemy_turn(self):
        for enemy in self.enemies:
            # Простой ИИ: двигаться к игроку или атаковать
            dx = dy = 0
            if abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y) == 1:
                self.player.health -= enemy.damage
                print(f"Террорист атаковал вас! Осталось здоровья: {self.player.health}")
            else:
                if enemy.x < self.player.x and self.map[enemy.y][enemy.x+1] == '.':
                    dx = 1
                elif enemy.x > self.player.x and self.map[enemy.y][enemy.x-1] == '.':
                    dx = -1
                elif enemy.y < self.player.y and self.map[enemy.y+1][enemy.x] == '.':
                    dy = 1
                elif enemy.y > self.player.y and self.map[enemy.y-1][enemy.x] == '.':
                    dy = -1
                
                enemy.x += dx
                enemy.y += dy

    def player_attack(self, direction):
        dx, dy = 0, 0
        if direction == 'up': dy = -1
        elif direction == 'down': dy = 1
        elif direction == 'left': dx = -1
        elif direction == 'right': dx = 1
        
        target_x = self.player.x + dx
        target_y = self.player.y + dy
        for enemy in self.enemies:
            if enemy.x == target_x and enemy.y == target_y:
                enemy.health -= self.player.damage
                print(f"Вы атаковали террориста! У врага осталось {enemy.health} здоровья")
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
                    print("Террорист уничтожен!")
                return True
        return False

    def run(self):
        while self.player.health > 0 and len(self.enemies) > 0:
            self.update_map()
            self.print_map()
            
            action = input("Введите действие (←↑↓→/A): ").lower()
            
            if action == 'a':
                direction = input("Направление атаки (←↑↓→): ")
                success = self.player_attack(direction)
            else:
                moves = {'left': (-1,0), 'right': (1,0),
                        'up': (0,-1), 'down': (0,1)}
                success = self.move_player(*moves.get(action, (0,0)))
            
            if success:
                self.enemy_turn()
            
        if self.player.health <= 0:
            print("Миссия провалена...")
        else:
            print("Все террористы уничтожены! Миссия выполнена!")

if __name__ == "__main__":
    game = Game()
    game.run()
