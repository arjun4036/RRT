import pygame
import random
import math

Width_Screen = 800  # Screen width
Height_Screen = 600  # Screen height

Rand_point = 0.05  # Selecting goal as random point
distance_tree = 30  # Distance to extend the tree
Obstacle_Min_Size = 20
Obstacle_Max_Size = 50


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None


def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def sample_random_point(goal):
    if random.random() < Rand_point:
        return goal
    else:
        return Node(random.randint(0, Width_Screen), random.randint(0, Height_Screen))


def nearest_neighbour(tree, random_point):
    if not tree:
        return None

    nearest_node = tree[0]
    min_dist = distance(nearest_node, random_point)

    for node in tree[1:]:
        dist = distance(node, random_point)
        if dist < min_dist:
            min_dist = dist
            nearest_node = node

    return nearest_node


def changedir(nearest_node, random_point):
    if distance(nearest_node, random_point) <= distance_tree:
        return random_point
    else:
        theta = math.atan2(random_point.y - nearest_node.y, random_point.x - nearest_node.x)
        return Node(nearest_node.x + distance_tree * math.cos(theta), nearest_node.y + distance_tree * math.sin(theta))


def collision_free(node, obstacles):
    for obstacle in obstacles:
        if distance(node, obstacle) < obstacle.radius:
            return False
    return True


def main():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    pygame.init()
    screen = pygame.display.set_mode((Width_Screen, Height_Screen))
    pygame.display.set_caption("RRT Diagram")
    clock = pygame.time.Clock()

    start_x = int(input("Enter x coordinate of start node: "))
    start_y = int(input("Enter y coordinate of start node: "))
    goal_x = int(input("Enter x coordinate of goal node: "))
    goal_y = int(input("Enter y coordinate of goal node: "))

    start = Node(start_x, start_y)  # Defining start and goal nodes
    goal = Node(goal_x, goal_y)

    num_obstacles = int(input("Enter number of Obstacles : "))
    obstacles = []
    for i in range(num_obstacles):
        obstacle_x = int(input("Enter x coordinate of obstacle {}: ".format(i + 1)))
        obstacle_y = int(input("Enter y coordinate of obstacle {}: ".format(i + 1)))
        obstacle_size = random.randint(Obstacle_Min_Size, Obstacle_Max_Size)
        obstacle = Node(obstacle_x, obstacle_y)
        obstacle.radius = obstacle_size
        obstacles.append(obstacle)

    tree = [start]  # Initializing

    # RRT Algorithm
    while True:
        random_point = sample_random_point(goal)

        nearest_node = nearest_neighbour(tree, random_point)  # Find nearest node in the tree

        new_node = changedir(nearest_node, random_point)  # Move towards random point

        if collision_free(new_node, obstacles):
            new_node.parent = nearest_node
            tree.append(new_node)

        if distance(new_node, goal) < distance_tree:
            goal.parent = new_node
            tree.append(goal)
            break

    path = []
    current_node = goal
    while current_node:
        path.append((current_node.x, current_node.y))
        current_node = current_node.parent

    path.reverse()

    screen.fill(WHITE)  # for final path
    for node in tree:
        if node.parent:
            pygame.draw.line(screen, BLUE, (node.x, node.y), (node.parent.x, node.parent.y))
    for obstacle in obstacles:
        pygame.draw.circle(screen, RED, (obstacle.x, obstacle.y), obstacle.radius)
    pygame.draw.circle(screen, GREEN, (start.x, start.y), 10)
    pygame.draw.circle(screen, GREEN, (goal.x, goal.y), 10)
    pygame.draw.lines(screen, BLACK, False, path, 2)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == "__main__":
    main()
