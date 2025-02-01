import math;
import pygame;
import time;

class Simulation():
    def __init__(self, width, height, tittle, color, collisions = False):
        self.width = width
        self.height = height
        self.tittle = tittle
        self.color = color
        self.objects = []
        self.position = self(7,5)
        self.positions_history = []
        self.collisions = collisions
        self.gravity_objects = []
        self.collisionLayers = []
    def add_object(self, object):
        self.objects.append(object)
        if object.gravity:
            self.gravity_objects.append(object)
    def store_positions(self):
        current_positions = []
        for obj in self.objects:
            current_positions.append([obj, obj.position])
        self.positions_history.append(current_positions)
    def run(self, speed=1, fps=60, frames='all'):
        if frames == 'all': frames = len(self.positions_history)
        display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.tittle)
        frame = 0
        clock = pygame.time.Clock()
        tempo = time.time()
        x = 0
        for objects in self.positions_history[:frames]:
            if x == round((self.lenght/self.dt)/(fps*self.lenght/speed)):
                x=0
                display.fill(self.color)
                for object in objects:
                    if object[0].circle:
                        object[0].position = list(object[0].position)
                        object[0].position[0] = object[1][0]-object[0].width/2
                        object[0].position[1] = object[1][1]-object[0].height/2
                        object[0].position = tuple(object[0].position)
                    else:
                        object[0].position = object[1]
                    display.blit(object[0].body, (object[0].position))
                pygame.display.update()
                clock.tick(fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    frame += 1
            x+=1
    def calculate(self, lenght, dt):
        self.lenght = lenght
        self.dt = dt
        self.steps = round(lenght/dt)
        for q in range(self.steps):
            if self.collisions: 
                for i in range(len(self.objects)):
                    object1 = self.objects[i]
                    for j in range(i + 1, len(self.objects)):
                        object2 = self.objects[j]
                        if object1.collisionLayer == object2.collisionLayer:
                            if checkCollision(object1, object2):
                                Collide(object1, object2)
            calculate_gravity(self.gravity_objects, dt)
            for object in self.objects:
                if not object.locked:
                    object.updatePosition(dt)
                if object.dV != 0:
                    object.accelerate(dt)
                if object.hitBorder:
                    border(object)
            self.store_positions()


class Object(pygame.Surface):
    def __init__(self, width, height, position, mass, speed, direction, color, simulation,circle=False, COR = 1, collisionLayer=0, hitBorder=False):
        self.height = height
        self.width = width
        self.gravity = False
        self.position = position
        self.circle = circle
        self.mass = mass
        self.speed = speed
        if color == "black" or color == (0,0,0):
            color = (0,0,1)
        self.color = color
        self.hitBorder = hitBorder
        self.collisionLayer = collisionLayer
        self.direction = direction
        self.simulation = simulation
        self.COR = COR
        self.body = pygame.Surface((self.width, self.height))
        if circle:
            self.body.set_colorkey((0, 0, 0))  
            pygame.draw.circle(self.body, (color), (self.width/2, self.height/2), self.width/2)
        else:
            self.body.fill(color)
        self.dV = 0
        simulation.add_object(self)
        self.locked = False
        self.angle = 0
    def lockPos(self):
        self.locked = True
    def addGravity(self, g=0):
        self.gravity = True
        self.g = g
        self.simulation.gravity_objects.append(self)
    def addAceleration(self, dV, angle):
        self.dV = dV
        self.angle = angle
    def updatePosition(self, dt):
        x, y = self.position
        radians = math.radians(self.direction)
        dx = self.speed * math.cos(radians)
        dy = self.speed * math.sin(radians)
        new_x = x + dx * dt
        new_y = y + dy * dt
        self.position = (new_x, new_y)
    def onScreen(self):
        if self.position[0] > self.simulation.width+self.width or self.position[0] < 0-self.width or self.position[1] > self.simulation.height+self.height or self.position[1] < 0-self.height:
            return False
        return True
    def accelerate(self, dt):
        directionRad = math.radians(self.direction)

        # Calculate the object's current x and y velocity components
        speedX = self.speed * math.cos(directionRad)
        speedY = self.speed * math.sin(directionRad)

        # Calculate the x and y components of the speed_change
        DeltaVX = self.dV * math.cos(math.radians(self.angle - math.pi))
        DeltaVY = self.dV * math.sin(math.radians(self.angle - math.pi))

        # Add the speed_change components to the current speed components
        new_speedX = speedX + DeltaVX*dt
        new_speedY = speedY + DeltaVY*dt

        # Calculate the new speed and direction
        new_speed = math.sqrt(new_speedX ** 2 + new_speedY ** 2)
        new_direction = math.degrees(math.atan2(new_speedY, new_speedX))

        # Update the object's speed and direction
        self.speed = new_speed
        self.direction = new_direction
def angle_difference(angle1, angle2):
    diff = (angle1 - angle2) % 360
    return diff if diff < 180 else 360 - diff
def checkCollision(object1, object2):
    if object1.circle and object2.circle:
        if distance(object1, object2) <= object1.width/2 + object2.width/2:
                return True
        return False
    elif object1.circle == object2.circle:
        if (object1.position[0] < object2.position[0] + object2.width and
        object1.position[0] + object1.width > object2.position[0]):
        
        # Check if the rectangles are overlapping along the y-axis
            if (object1.position[1] < object2.position[1] + object2.height and object1.position[1] + object1.height > object2.position[1]):
            
            # The rectangles are overlapping
                return True
    # The rectangles are not overlapping
        return False
def border(object):
    x, y = object.position
    if object.circle:
        radius = object.width / 2
        # Check collision with left or right border
        if x - radius < 0:
            

            object.position = list(object.position)
            object.direction = 180 - object.direction
            object.position[0] = (object.width/2)
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)
        if x + radius > object.simulation.width:
            
            object.position = list(object.position)
            object.direction = 180 - object.direction
            object.position[0] = (object.simulation.width -object.width/2)
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)

        if y - radius < 0:
            
            object.position = list(object.position)
            object.direction = -object.direction
            object.position[1] = (object.width/2)
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)
        
        if y+ radius > object.simulation.height:
            
            object.position = list(object.position)
            object.direction = -object.direction
            object.position[1] = (object.simulation.height -object.width/2)-1
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)
    else:
        # Check collision with left or right border
        if x < 0:
            
            object.position = list(object.position)
            object.direction = 180 - object.direction
            object.position[0] = 0
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)
        if x+object.width > object.simulation.width:
            
            object.position = list(object.position)
            object.direction = 180 - object.direction
            object.position[0] = (object.simulation.width -object.width)
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)

        if y < 0:
            
            object.position = list(object.position)
            object.direction = -object.direction
            object.position[1] = 0
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)
        
        if y+object.height > object.simulation.height:
            
            object.position = list(object.position)
            object.direction = -object.direction
            object.position[1] = (object.simulation.height -object.height)-1
            object.speed *= object.COR
            if abs(object.speed) < 0.1:
                object.speed = 0
            object.position = tuple(object.position)
        

def calculate_gravity(objects, dt):
    """
    Calculates the effect of gravity on each object and updates its speed and direction.
    """
    
    for i, object1 in enumerate(objects):
        net_force_x, net_force_y = 0, 0
        
        for j, object2 in enumerate(objects):
            if i == j:
                continue
            
            dx = object2.position[0] - object1.position[0]
            dy = object2.position[1] - object1.position[1]
            dist = math.sqrt(dx ** 2 + dy ** 2)+0.000001
            force = ((object1.g+object2.g)/2) * object1.mass * object2.mass / dist ** 2
            
            net_force_x += force * (dx / dist)*1000
            net_force_y += force * (dy / dist)*1000

            object1_speed_x = object1.speed * math.cos(math.radians(object1.direction))
            object1_speed_y = object1.speed * math.sin(math.radians(object1.direction))
            object1_speed_x += (net_force_x / object1.mass) * dt
            object1_speed_y += (net_force_y / object1.mass) * dt
            object1.speed = math.sqrt(object1_speed_x ** 2 + object1_speed_y ** 2)
            object1.direction = math.degrees(math.atan2(object1_speed_y, object1_speed_x))
def distance(objeto1, objeto2):
    x1, y1 = objeto1.position
    x2, y2 = objeto2.position
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)
def Collide(object1, object2):

    COR = object1.COR*object2.COR
    x1, y1 = object1.position
    x2, y2 = object2.position
    if not object1.circle:
        x1 += object1.width/2
        y1 += object1.height/2
    if not object2.circle:
        x2 += object2.width/2
        y2 += object2.height/2
    v1 = object1.speed
    v2 = object2.speed
    d1 = object1.direction
    d2 = object2.direction
    m1 = object1.mass
    m2 = object2.mass

    # Convert direction to radians
    r1 = math.radians(d1)
    r2 = math.radians(d2)

    # Calculate the normal vector (unit vector) between the two objects
    
    delta_x = x2 - x1
    delta_y = y2 - y1
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    if distance == 0:
        normal_x, normal_y = 0,0
    else:
        normal_x = delta_x / distance
        normal_y = delta_y / distance

    # Calculate the relative velocity along the normal vector
    relative_velocity_x = v2 * math.cos(r2) - v1 * math.cos(r1)
    relative_velocity_y = v2 * math.sin(r2) - v1 * math.sin(r1)
    relative_velocity = relative_velocity_x * normal_x + relative_velocity_y * normal_y

    # Calculate the impulse using the COR
    impulse = 2 * relative_velocity * COR / (1/m1 + 1/m2)

    # Calculate the final velocities using the impulse
    if COR != 0:
        
        v1fx = v1 * math.cos(r1) + (impulse * normal_x) / m1
        v1fy = v1 * math.sin(r1) + (impulse * normal_y) / m1
        v2fx = v2 * math.cos(r2) - (impulse * normal_x) / m2
        v2fy = v2 * math.sin(r2) - (impulse * normal_y) / m2
    else:
        # In the case of COR = 0 (perfectly inelastic collision), objects stick together
        v1fx = (m1 * v1 * math.cos(r1) + m2 * v2 * math.cos(r2)) / (m1 + m2)
        v1fy = (m1 * v1 * math.sin(r1) + m2 * v2 * math.sin(r2)) / (m1 + m2)
        v2fx = v1fx
        v2fy = v1fy

    # Calculate the magnitudes and directions of the final velocities
    v1f = math.sqrt(v1fx ** 2 + v1fy ** 2)
    v2f = math.sqrt(v2fx ** 2 + v2fy ** 2)
    d1f = math.degrees(math.atan2(v1fy, v1fx))
    d2f = math.degrees(math.atan2(v2fy, v2fx))
    if object1.circle and object2.circle:
        dx = object2.position[0] - object1.position[0]
        dy = object2.position[1] - object1.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Calculate the sum of the radii of the two circles, plus one unit of distance
        radius_sum = (object1.width / 2) + (object2.width / 2)

        # Check if the circles are overlapping or touching
        if distance < radius_sum:
            # Calculate the overlap distance, plus one unit of distance
            overlap = (radius_sum - distance)+0.1

            # Calculate the unit vector in the direction from circle1 to circle2
            try:
                unit_vector_x = dx / distance
                unit_vector_y = dy / distance
            except:
                print("Error: object1 = {}, object2 = {}, distance = {}".format(object1.position, object2.position, distance))
                raise

            # Move the circles apart by half the overlap distance each, in opposite directions
            object1.position = list(object1.position)
            object2.position = list(object2.position)
            object1.position[0] -= (unit_vector_x * (overlap / 2))
            object1.position[1] -= (unit_vector_y * (overlap / 2))
            object2.position[0] += (unit_vector_x * (overlap / 2))
            object2.position[1] += (unit_vector_y * (overlap / 2))
            object1.position = tuple(object1.position)
            object2.position = tuple(object2.position)
    elif object1.circle == object2.circle:
        # Check if the rectangles are overlapping along the x-axis
        if (object1.position[0] < object2.position[0] + object2.width and
            object1.position[0] + object1.width > object2.position[0]):
            
            # Check if the rectangles are overlapping along the y-axis
            if (object1.position[1] < object2.position[1] + object2.height and
                object1.position[1] + object1.height > object2.position[1]):
                
                # Calculate the overlap distances along the x and y axes
                overlap_x = min(object1.position[0] + object1.width - object2.position[0],
                                object2.position[0] + object2.width - object1.position[0])
                overlap_y = min(object1.position[1] + object1.height - object2.position[1],
                                object2.position[1] + object2.height - object1.position[1])

                # Separate the rectangles along the axis with the least overlap
                if overlap_x < overlap_y:
                    if object1.position[0] < object2.position[0]:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[0] -= overlap_x / 2
                        object2.position[0] += overlap_x / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)
                    else:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[0] += overlap_x / 2
                        object2.position[0] -= overlap_x / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)
                else:
                    if object1.position[1] < object2.position[1]:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[1] -= overlap_y / 2
                        object2.position[1] += overlap_y / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)
                    else:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[1] += overlap_y / 2
                        object2.position[1] -= overlap_y / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)

    # Update the velocities and directions of the objects
    object1.speed = v1f
    object1.direction = d1f
    object2.speed = v2f
    object2.direction = d2f
    return object1, object2