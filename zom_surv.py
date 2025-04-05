import pygame
import random
import math
import heapq
import os

pygame.init()

WIDTH, HEIGHT = 900, 600
FPS = 60
BULLET_SPEED = 10
ZOMBIE_SPEED = 1.5
HUMAN_SPEED = 2.5
SPAWN_RATE = 60 #frames
GAME_DURATION = 60  # 60 seconds

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PEACH = (255, 221, 171)

# Creating screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI vs AI Zombie Survival")
clock = pygame.time.Clock()

# Load images or drawing images
def load_image(name, scale=1):
    try:
        img = pygame.image.load(f"assets/{name}.png").convert_alpha()
        return pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
    except:
        # draw image if image not found
        img = pygame.Surface((32, 32), pygame.SRCALPHA)
        if "human" in name:
            pygame.draw.rect(img, (0, 100, 200), (8, 4, 16, 24))  # Body
            pygame.draw.circle(img, (255, 200, 150), (16, 10), 8)  # Head
        elif "zombie" in name:
            pygame.draw.rect(img, (0, 100, 0), (8, 4, 16, 24))  # Body
            pygame.draw.circle(img, (100, 150, 100), (16, 10), 8)  # Head
            pygame.draw.line(img, BLACK, (10, 8), (14, 12), 2)  # Scars
            pygame.draw.line(img, BLACK, (22, 8), (18, 12), 2)
        elif "bullet" in name:
            pygame.draw.circle(img, YELLOW, (16, 16), 8)
        elif "background" in name:
            img = pygame.Surface((WIDTH, HEIGHT))
            img.fill(PEACH)
            # Drawing damaged buildings
            for i in range(5):
                width = random.randint(50, 150)
                height = random.randint(100, 300)
                x = random.randint(0, WIDTH - width)
                y = HEIGHT - height
                pygame.draw.rect(img, (50, 50, 50), (x, y, width, height))
                # drawing broken windows
                for wx in range(x + 5, x + width - 5, 15):
                    for wy in range(y + 5, y + height - 5, 20):
                        if random.random() > 0.3:  # Some windows are broken
                            pygame.draw.rect(img, (70, 70, 100), (wx, wy, 10, 15))
        return pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))

# Creating images(from above def load_image)
human_img = load_image("human")
zombie_img = load_image("zombie")
bullet_img = load_image("bullet")
background_img = load_image("background")

# Blood splattering
blood_img = pygame.Surface((64, 64), pygame.SRCALPHA)
for _ in range(15):
    pygame.draw.circle(blood_img, (150, 0, 0, 200), (random.randint(0, 64), random.randint(0, 64)), random.randint(2, 8))


#for playing of human using AI
class HumanAI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 16
        self.health = 100
        self.speed = HUMAN_SPEED
        self.image = human_img
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.path = []
        self.grid_size = 20
        self.recalculate_counter = 0
        self.fear_level = 0  #range from0 to 100
        self.ammo = 30
        self.reload_time = 0
        self.target_zombie = None
    
    def draw(self, screen):
        # Rotate to face movement direction
        if hasattr(self, 'vx') and hasattr(self, 'vy'):
            angle = math.degrees(math.atan2(self.vy, self.vx))
            rotated_img = pygame.transform.rotate(self.image, -angle)
            self.rect = rotated_img.get_rect(center=(self.x, self.y))
            screen.blit(rotated_img, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect)
        
        # Health bar
        pygame.draw.rect(screen, RED, (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 20, self.y - 30, 40 * (self.health / 100), 5))
    
    def update(self, zombies, obstacles, safe_zones, bullets, grid):
        # Updating fear level based upon closest zombie
        closest_zombie = None
        min_dist = float('inf')
        
        for zombie in zombies:
            dist = math.sqrt((zombie.x - self.x)**2 + (zombie.y - self.y)**2)
            if dist < min_dist:
                min_dist = dist
                closest_zombie = zombie
        
        self.fear_level = max(0, min(100, 100 - min_dist * 2))
        
        # AI decision making
        if self.fear_level > 70 and safe_zones:
            # going to safe zone
            closest_safe = min(safe_zones,  key=lambda sz: math.sqrt((sz[0]-self.x)**2 + (sz[1]-self.y)**2))
            self.move_to(closest_safe[0], closest_safe[1], obstacles, grid)
        elif closest_zombie and min_dist < 150:
            # Combat behavior
            if min_dist > 100 and self.ammo > 0:
                # Shoot at zombie
                self.target_zombie = closest_zombie
                if self.reload_time <= 0:
                    bullets.append(self.shoot_at(closest_zombie))
                    self.ammo -= 1
                    self.reload_time = 10
            else:
                # Evade zombie
                flee_x = self.x + (self.x - closest_zombie.x) / min_dist * 100
                flee_y = self.y + (self.y - closest_zombie.y) / min_dist * 100
                flee_x = max(0, min(WIDTH, flee_x))
                flee_y = max(0, min(HEIGHT, flee_y))
                self.move_to(flee_x, flee_y, obstacles, grid)
        elif not self.path or random.random() < 0.02:
            # Wander randomly
            target_x = random.randint(0, WIDTH)
            target_y = random.randint(0, HEIGHT)
            self.move_to(target_x, target_y, obstacles, grid)
        
        # Reload if empty
        if self.ammo <= 0 and self.reload_time <= 0:
            self.ammo = 30
            self.reload_time = 60  # Longer reload when empty
        
        if self.reload_time > 0:
            self.reload_time -= 1
    
    def move_to(self, target_x, target_y, obstacles, grid):
        # Pathfinding with A*
        self.recalculate_counter += 1
        if self.recalculate_counter >= 30 or not self.path:
            self.recalculate_counter = 0
            self.path = self.find_path((self.x, self.y), (target_x, target_y), obstacles, grid)
        
        if self.path:
            next_pos = self.path[0]
            dx = next_pos[0] - self.x
            dy = next_pos[1] - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            # Store direction for rotation
            self.vx = dx / dist if dist != 0 else 0
            self.vy = dy / dist if dist != 0 else 0
            
            if dist < 5:  # Reached next node
                self.path.pop(0)
            else:
                # Move towards next path node
                if dist != 0:
                    self.x += (dx / dist) * self.speed
                    self.y += (dy / dist) * self.speed
                    self.rect.center = (self.x, self.y)
    
    def shoot_at(self, target):
        # Calculate direction to target
        dx = target.x - self.x
        dy = target.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        # Add some inaccuracy based on distance
        inaccuracy = min(0.2, dist / 1000)
        dx += random.uniform(-inaccuracy, inaccuracy) * dist
        dy += random.uniform(-inaccuracy, inaccuracy) * dist
        
        return Bullet(self.x, self.y, self.x + dx, self.y + dy)
    
    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def find_path(self, start, end, obstacles, grid):
        """A* pathfinding algorithm"""
        grid_start = (int(start[0] / self.grid_size), int(start[1] / self.grid_size))
        grid_end = (int(end[0] / self.grid_size), int(end[1] / self.grid_size))
        
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-directional
        close_set = set()
        came_from = {}
        gscore = {grid_start: 0}
        fscore = {grid_start: self.heuristic(grid_start, grid_end)}
        oheap = []
        heapq.heappush(oheap, (fscore[grid_start], grid_start))
        
        while oheap:
            current = heapq.heappop(oheap)[1]
            
            if current == grid_end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                # Convert to world coordinates
                return [(p[0] * self.grid_size + self.grid_size//2,  p[1] * self.grid_size + self.grid_size//2) for p in path]
            
            close_set.add(current)
            
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j                
                if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]].walkable):
                    tentative_g_score = gscore[current] + 1
                    
                    if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                        continue
                        
                    if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, grid_end)
                        heapq.heappush(oheap, (fscore[neighbor], neighbor))
        
        return []  # No path found

class ZombieAI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 16
        self.health = 30
        self.speed = ZOMBIE_SPEED
        self.image = zombie_img
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.path = []
        self.grid_size = 20
        self.recalculate_counter = 0
        self.blood_splatters = []
        self.aggression = random.uniform(0.5, 1.5)  # Speed multiplier when chasing
    
    def draw(self, screen):
        # Rotate to face movement direction
        if hasattr(self, 'vx') and hasattr(self, 'vy'):
            angle = math.degrees(math.atan2(self.vy, self.vx))
            rotated_img = pygame.transform.rotate(self.image, -angle)
            self.rect = rotated_img.get_rect(center=(self.x, self.y))
            screen.blit(rotated_img, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect)
        
        # Draw blood splattering
        for splatter in self.blood_splatters:
            screen.blit(blood_img, (splatter[0] - 32, splatter[1] - 32))
        
        # Health bar
        pygame.draw.rect(screen, RED, (self.x - 15, self.y - 25, 30, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 15, self.y - 25, 30 * (self.health / 30), 5))
    
    def update(self, humans, obstacles, grid):
        # Find closest human
        if humans:
            closest_human = min(humans,key=lambda h: math.sqrt((h.x - self.x)**2 + (h.y - self.y)**2))
            # Recalculate path occasionally
            self.recalculate_counter += 1
            if self.recalculate_counter >= 30 or not self.path:
                self.recalculate_counter = 0
                self.path = self.find_path((self.x, self.y), (closest_human.x, closest_human.y), obstacles, grid)
            
            # Follow path
            if self.path:
                next_pos = self.path[0]
                dx = next_pos[0] - self.x
                dy = next_pos[1] - self.y
                dist = math.sqrt(dx**2 + dy**2)
                
                # Store direction for rotation
                self.vx = dx / dist if dist != 0 else 0
                self.vy = dy / dist if dist != 0 else 0
                
                if dist < 5:  # Reached next node
                    self.path.pop(0)
                else:
                    # Move with aggression multiplier when close to human
                    current_speed = self.speed * (self.aggression if dist < 100 else 1)
                    if dist != 0:
                        self.x += (dx / dist) * current_speed
                        self.y += (dy / dist) * current_speed
                        self.rect.center = (self.x, self.y)
    
    def add_blood_splatter(self):
        self.blood_splatters.append((self.x, self.y))
        if len(self.blood_splatters) > 3:  # Limit splatters
            self.blood_splatters.pop(0)
    
    def find_path(self, start, end, obstacles, grid):
        """A* pathfinding with obstacle avoidance"""
        grid_start = (int(start[0] / self.grid_size), int(start[1] / self.grid_size))
        grid_end = (int(end[0] / self.grid_size), (int(end[1] / self.grid_size)))
        
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-directional
        close_set = set()
        came_from = {}
        gscore = {grid_start: 0}
        fscore = {grid_start: self.heuristic(grid_start, grid_end)}
        oheap = []
        heapq.heappush(oheap, (fscore[grid_start], grid_start))
        
        while oheap:
            current = heapq.heappop(oheap)[1]
            
            if current == grid_end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                # Converting  into world coordinates
                return [(p[0] * self.grid_size + self.grid_size//2,  p[1] * self.grid_size + self.grid_size//2) for p in path]
            
            close_set.add(current)
            
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j                
                if (0 <= neighbor[0] < len(grid)) and (0 <= neighbor[1] < len(grid[0])):
                    if not grid[neighbor[0]][neighbor[1]].walkable:
                        continue
                    
                    tentative_g_score = gscore[current] + 1
                    
                    if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                        continue
                        
                    if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, grid_end)
                        heapq.heappush(oheap, (fscore[neighbor], neighbor))
        
        return []  # No path found
    
    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.radius = 4
        self.speed = BULLET_SPEED
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx**2 + dy**2)
        self.vx = (dx / dist) * self.speed if dist != 0 else 0
        self.vy = (dy / dist) * self.speed if dist != 0 else 0
        
        # Rotation angle
        self.angle = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(bullet_img, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def is_off_screen(self):
        return (self.x < 0 or self.x > WIDTH or 
                self.y < 0 or self.y > HEIGHT)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (70, 50, 30)  # Brown for walls/blockers
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Add details to make it look like rubble
        for i in range(5):
            pygame.draw.line(screen, (50, 30, 10),(self.x + 5 + i*10, self.y + 5),(self.x + 5 + i*10, self.y + self.height - 5), 2)
    
    def collides_with(self, x, y, radius):
        # Check if circle collides with rectangle
        closest_x = max(self.x, min(x, self.x + self.width))
        closest_y = max(self.y, min(y, self.y + self.height))
        
        distance_x = x - closest_x
        distance_y = y - closest_y
        
        return (distance_x**2 + distance_y**2) < (radius**2)

class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
    
    def __lt__(self, other):
        return self.f < other.f

def create_grid(obstacles, grid_size=20):
    grid_width = WIDTH // grid_size
    grid_height = HEIGHT // grid_size
    grid = []
    
    for x in range(grid_width):
        grid.append([])
        for y in range(grid_height):
            walkable = True
            node_rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            
            for obstacle in obstacles:
                if node_rect.colliderect(obstacle.rect):
                    walkable = False
                    break
            
            grid[x].append(Node(x, y, walkable))
    
    return grid

def main():
    # Create background
    background = background_img
    
    # Create obstacles
    obstacles = [
        Obstacle(100, 100, 200, 50),
        Obstacle(400, 300, 50, 200),
        Obstacle(200, 400, 300, 50),
        Obstacle(500, 100, 50, 150),
        Obstacle(50, 250, 30, 100),
        Obstacle(700, 200, 80, 80)
    ]
    
    # Safe zones (humans will flee here when scared)
    safe_zones = [
        (50, 50),
        (WIDTH - 50, 50),
        (WIDTH // 2, 50),
        (50, HEIGHT - 50),
        (WIDTH - 50, HEIGHT - 50)
    ]
    
    grid = create_grid(obstacles)
    
    humans = [HumanAI(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)) for _ in range(5)]
    
    zombies = [ZombieAI(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(3)]
    
    bullets = []
    blood_splatters = []
    spawn_counter = 0
    
    # Timer variables
    start_time = pygame.time.get_ticks()  # Get initial time in milliseconds
    game_over = False
    game_won = False  # To track if humans survived
    
    font = pygame.font.SysFont('Arial', 32)
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Calculate remaining time
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
        remaining_time = max(0, GAME_DURATION - elapsed_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    start_time = pygame.time.get_ticks()  # Reset timer
                    humans = [HumanAI(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100)) for _ in range(5)]
                    zombies = [ZombieAI(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(3)]
                    bullets = []
                    blood_splatters = []
                    game_over = False
                    game_won = False
        
        # Check for time-based game over
        if remaining_time <= 0 and not game_over:
            game_over = True
            game_won = len(humans) > 0  # Humans win if any survive
        
        if not game_over:
            # adding  new zombies occasionally
            spawn_counter += 1
            if spawn_counter >= SPAWN_RATE and len(zombies) < 50:
                spawn_counter = 0
                side = random.randint(0, 3)
                if side == 0:  # Top
                    x = random.randint(0, WIDTH)
                    y = -20
                elif side == 1:  # Right
                    x = WIDTH + 20
                    y = random.randint(0, HEIGHT)
                elif side == 2:  # Bottom
                    x = random.randint(0, WIDTH)
                    y = HEIGHT + 20
                else:  # Left
                    x = -20
                    y = random.randint(0, HEIGHT)
                zombies.append(ZombieAI(x, y))
            
            # Updating humans
            for human in humans[:]:
                human.update(zombies, obstacles, safe_zones, bullets, grid)
                
                # Checking whether human is dead
                if human.health <= 0:
                    humans.remove(human)
                    # Human turning into zombie
                    zombies.append(ZombieAI(human.x, human.y))
            
            # Updating zombies
            for zombie in zombies[:]:
                zombie.update(humans, obstacles, grid)
                
                # Checking whether zombie is dead
                if zombie.health <= 0:
                    zombies.remove(zombie)
            
            # Updating bullets
            for bullet in bullets[:]:
                bullet.update()
                
                if bullet.is_off_screen():
                    bullets.remove(bullet)
                    continue
                
                # Checking bullet collisions with zombies
                for zombie in zombies[:]:
                    dx = bullet.x - zombie.x
                    dy = bullet.y - zombie.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < bullet.radius + zombie.radius:
                        zombie.health -= 10
                        zombie.add_blood_splatter()
                        blood_splatters.append((zombie.x, zombie.y))
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if zombie.health <= 0:
                            zombies.remove(zombie)
                        break
                
                # Checking bullet collisions with obstacles
                for obstacle in obstacles:
                    if obstacle.collides_with(bullet.x, bullet.y, bullet.radius):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        blood_splatters.append((bullet.x, bullet.y))
                        break
            
            # Checking zombie-human collisions
            for zombie in zombies:
                for human in humans[:]:
                    dx = zombie.x - human.x
                    dy = zombie.y - human.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < zombie.radius + human.radius:
                        human.health -= 1
                        if human.health <= 0:
                            humans.remove(human)
                            zombies.append(ZombieAI(human.x, human.y))
            
            # Early game over condition - all humans dead
            if not humans:
                game_over = True
                game_won = False
        
        # Drawing
        screen.blit(background, (0, 0))
        
        # Draw blood splatters
        for splatter in blood_splatters[-50:]:  # Limit to 50 splatters
            screen.blit(blood_img, (splatter[0] - 32, splatter[1] - 32))
        
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)
        
        # Draw zombies
        for zombie in zombies:
            zombie.draw(screen)
        
        # Draw humans
        for human in humans:
            human.draw(screen)
        
        # Draw stats
        humans_text = font.render(f"Humans: {len(humans)}", True, WHITE)
        zombies_text = font.render(f"Score: {len(zombies)}", True, WHITE)
        timer_text = font.render(f"Time: {int(remaining_time)}", True, WHITE)
        screen.blit(humans_text, (10, 10))
        screen.blit(zombies_text, (10, 50))
        screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))
        
        # Game over screen
        if game_over:
            if game_won:
                result_text = font.render("Humans Survived! Press R to restart", True, GREEN)
            else:
                result_text = font.render("Zombies Won! Press R to restart", True, RED)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()