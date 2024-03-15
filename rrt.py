import pygame
import random
import math

SCREEN_WIDTH = 800  # Screen width
SCREEN_HEIGHT = 600  # Screen height

GOAL_SELECTION_PROBABILITY = 0.05  # Selecting goal as random point
TREE_EXTENSION_DISTANCE = 30  # Distance to extend the tree
OBSTACLE_MIN_SIZE = 20
OBSTACLE_MAX_SIZE = 50


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None


def calculate_distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def sample_random_point(goal):
    if random.random() < GOAL_SELECTION_PROBABILITY:
        return goal
    else:
        return Node(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))


def find_nearest_neighbour(tree, random_point):
    if not tree:
        return None

    nearest_node = tree[0]
    min_dist = calculate_distance(nearest_node, random_point)

    for node in tree[1:]:
        dist = calculate_distance(node, random_point)
        if dist < min_dist:
            min_dist = dist
            nearest_node = node

    return nearest_node


def change_direction(nearest_node, random_point):
    if calculate_distance(nearest_node, random_point) <= TREE_EXTENSION_DISTANCE:
        return random_point
    else:
        theta = math.atan2(random_point.y - nearest_node.y, random_point.x - nearest_node.x)
        return Node(nearest_node.x + TREE_EXTENSION_DISTANCE * math.cos(theta), nearest_node.y + TREE_EXTENSION_DISTANCE * math.sin(theta))


def is_collision_free(node, obstacles):
    for obstacle in obstacles:
        if calculate_distance(node, obstacle) < obstacle.radius:
            return False
    return True


def main():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RRT Diagram")
    clock = pygame.time.Clock()

    start_x = int(input("Enter the x-coordinate of the start node: "))
    start_y = int(input("Enter the y-coordinate of the start node: "))
    goal_x = int(input("Enter the x-coordinate of the goal node: "))
    goal_y = int(input("Enter the y-coordinate of the goal node: "))

    start = Node(start_x, start_y)  # Defining start and goal nodes
    goal = Node(goal_x, goal_y)

    num_obstacles = int(input("Enter the number of obstacles: "))
    obstacles = []
    for i in range(num_obstacles):
        obstacle_x = int(input("Enter the x-coordinate of obstacle {}: ".format(i + 1)))
        obstacle_y = int(input("Enter the y-coordinate of obstacle {}: ".format(i + 1)))
        obstacle_size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
        obstacle = Node(obstacle_x, obstacle_y)
        obstacle.radius = obstacle_size
        obstacles.append(obstacle)

    tree = [start]  # Initializing

    # RRT Algorithm
    while True:
        random_point = sample_random_point(goal)

        nearest_node = find_nearest_neighbour(tree, random_point)  # Find nearest node in the tree

        new_node = change_direction(nearest_node, random_point)  # Move towards random point

        if is_collision_free(new_node, obstacles):
            new_node.parent = nearest_node
            tree.append(new_node)

        if calculate_distance(new_node, goal) < TREE_EXTENSION_DISTANCE:
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
