# This physics simulation represents a pogostick. There is a top n shaped body that represents the person and a more complicated set of bodies
# that represent the pogostick. There are springs connecting them that a user (or agent) can control. The spring on the top right and on the top
# represents the hands of someone on a pogostick, the spring on the bottom left represents the feet of a person on a pogostick, and the bottom
# spring represents the jumping of the preson.
#
# Jacob Karty 12/4/2024

import pymunk
import time

class Pogo:
    
    def __init__(self):
        #begin the simulation
        self.reset_simulation()

        #global variables
        self.spring_jump_distance = 100
        self.jumping_spring_rest_length = 30
        self.jump_pressed = False
        self.top_spring_rest_length = 25
        self.bottom_spring_rest_length = 25
        self.press_time = time.time()

    """this is the information given to the agent to control the pogo"""
    def get_current_state(self):
        return [self.pogo_body.angle,   self.pogo_body.angular_velocity,   self.pogo_body.position[0],   self.pogo_body.position[1],   self.pogo_body.velocity[0],   self.pogo_body.velocity[1],
                self.pogo_body_2.angle, self.pogo_body_2.angular_velocity, self.pogo_body_2.position[0], self.pogo_body_2.position[1], self.pogo_body_2.velocity[0], self.pogo_body_2.velocity[1]]

    """The 5 possible actions are to extend and retract the upper spring, extend and retract the lower spring, and jump. This takes
    an array of length 5 as input and applies the desired actions"""
    def apply_actions(self, actions):
        #jump
        if actions[0] == 1:
            if time.time() - self.press_time >= 0.2:
                self.jump_pressed = True
                self.press_time = time.time()
                self.jumping_spring.rest_length += self.spring_jump_distance  # Increase the rest length by 50 units

        # Check if the spring length should revert after 0.1 seconds
        if self.jump_pressed and time.time() - self.press_time >= .1:
            self.jumping_spring.rest_length = self.jumping_spring_rest_length  # Revert to the original length
            self.jump_pressed = False
        
        #top spring right, left, and center
        if actions[1] == 1:
            self.top_spring.rest_length = self.top_spring_rest_length + 20
        elif actions[2] == 1:
            self.top_spring.rest_length = self.top_spring_rest_length - 20
        else:
            self.top_spring.rest_length = self.top_spring_rest_length
        
        #bottom spring right, left, and center
        if actions[3] == 1:
            self.bottom_spring.rest_length = self.bottom_spring_rest_length - 20
        elif actions[4] == 1:
            self.bottom_spring.rest_length = self.bottom_spring_rest_length + 20
        else:
            self.bottom_spring.rest_length = self.bottom_spring_rest_length
    
    """Resets the simulation by re-creating all of the bodies and resetting their positions."""
    def reset_simulation(self):
        # Create the Pymunk physics space and gravity
        space = pymunk.Space()
        space.gravity = (0, 900) 

        # Create static ground at the bottom
        ground = pymunk.Segment(space.static_body, (-500, 550), (1700, 550), 5)  # Ground line at y = 550
        ground.friction = 1
        space.add(ground)

        """Create a single body for the pogostics"""
        mass = 2
        width = 25
        height = 150

        # Create the body for the U-shaped object.
        pogo_body = pymunk.Body(mass, pymunk.moment_for_box(mass, (100, 20)))  # Approximation for moment of inertia
        pogo_body.position = (300, 450)  # Starting position of the U shape
        space.add(pogo_body)  # Add body to the space        

        # Box 1 (left vertical part of the U)
        box1_vertices = [
            (-width / 2, height / 3),    # Bottom-left corner of the first vertical box
            (-width / 6, height / 3),    # Bottom-right corner
            (-width / 6, -height / 3),  # Top-right corner
            (-width / 2, -height / 3)   # Top-left corner
        ]
        pogo_box1_shape = pymunk.Poly(pogo_body, box1_vertices)
        pogo_box1_shape.elasticity = 0.5
        pogo_box1_shape.friction = 1
        space.add(pogo_box1_shape)

        # Box 2 (horizontal base of the U)
        box2_vertices = [
            (-width / 2, -height / 3),   # Bottom-left corner of the base
            (width / 2, -height / 3),    # Bottom-right corner of the base
            (width / 2, -2 * height / 3),    # Top-right corner
            (-width / 2, -2 * height / 3)    # Top-left corner
        ]
        pogo_box2_shape = pymunk.Poly(pogo_body, box2_vertices)
        pogo_box2_shape.elasticity = 0.5
        pogo_box2_shape.friction = 1
        space.add(pogo_box2_shape)

        # Box 3 (right vertical part of the U)
        box3_vertices = [
            (width / 6, height / 3),    # Bottom-left corner of the second vertical box
            (width / 2, height / 3),    # Bottom-right corner
            (width / 2, -height / 3),  # Top-right corner
            (width / 6, -height / 3)   # Top-left corner
        ]
        pogo_box3_shape = pymunk.Poly(pogo_body, box3_vertices)
        pogo_box3_shape.elasticity = 0.5
        pogo_box3_shape.friction = 1
        space.add(pogo_box3_shape)

        # Box 4 (left foot holder)
        box4_vertices = [
            (width / 2, height / 6),    # Bottom-left corner of the second vertical box
            (width * 1.5, height / 6),    # Bottom-right corner
            (width / 2, height / 7),  # Top-right corner
            (width * 1.5, height / 7)   # Top-left corner
        ]
        pogo_box4_shape = pymunk.Poly(pogo_body, box4_vertices)
        pogo_box4_shape.elasticity = 0.5
        pogo_box4_shape.friction = 1
        space.add(pogo_box4_shape)

        # Box 5 (right foot holder)
        box5_vertices = [
            (-width / 2, height / 6),    # Bottom-left corner of the second vertical box
            (-width * 1.5, height / 6),    # Bottom-right corner
            (-width / 2, height / 7),  # Top-right corner
            (-width * 1.5, height / 7)   # Top-left corner
        ]
        pogo_box5_shape = pymunk.Poly(pogo_body, box5_vertices)
        pogo_box5_shape.elasticity = 0.5
        pogo_box5_shape.friction = 1
        space.add(pogo_box5_shape)


        """Create a single body for the second U-shape (the person)"""
        mass = 4
        pogo_body_2 = pymunk.Body(mass, pymunk.moment_for_box(mass, (100, 20)))  # Approximation for moment of inertia
        pogo_body_2.position = (300, 400)  # Starting position of the U shape
        space.add(pogo_body_2)  # Add body to the space


        # Box 1 (left leg of the U)
        box1_vertices_2 = [
            (-width, height / 2),    # Bottom-left corner of the first vertical box
            (-width * 1.5 , height / 2),    # Bottom-right corner
            (-width, -height / 2.5),  # Top-right corner
            (-width * 1.5, -height / 2.5)   # Top-left corner
        ]
        pogo_box1_shape_2 = pymunk.Poly(pogo_body_2, box1_vertices_2)
        pogo_box1_shape_2.elasticity = 0.5
        pogo_box1_shape_2.friction = 0.5
        space.add(pogo_box1_shape_2)

        # Box 2 (left right of the U)
        box2_vertices_2 = [
            (width, height / 2),    # Bottom-left corner of the first vertical box
            (width * 1.5 , height / 2),    # Bottom-right corner
            (width, -height / 2.5),  # Top-right corner
            (width * 1.5, -height / 2.5)   # Top-left corner
        ]
        pogo_box2_shape_2 = pymunk.Poly(pogo_body_2, box2_vertices_2)
        pogo_box2_shape_2.elasticity = 0.5
        pogo_box2_shape_2.friction = 0.5
        space.add(pogo_box2_shape_2)

        # Box 3 (top part of the U)
        box2_vertices_3 = [
            (-width * 1.5, -height / 2.5),    # Bottom-left corner of the first vertical box
            (width * 1.5, -height / 2.5),    # Bottom-right corner
            (width * 1.5, -height / 2),  # Top-right corner
            (-width * 1.5, -height / 2)   # Top-left corner
        ]
        pogo_box3_shape_2 = pymunk.Poly(pogo_body_2, box2_vertices_3)
        pogo_box3_shape_2.elasticity = 0.5
        pogo_box3_shape_2.friction = 0.5
        space.add(pogo_box3_shape_2)


        """Springs for the body to control the pogostick"""

        stiffness = 300  # How stiff the spring is
        damping = 10  # Damping effect (controls oscillation)
        top_spring_rest_length = width
        bottom_spring_rest_length = width

        # Bottom spring
        # Attach the spring to the 2 U shaped objects
        bottom_spring = pymunk.DampedSpring(
            pogo_body, pogo_body_2,  # Bodies to connect
            (0, -20),  # Attach to the first U object (pogo)
            (-width, 35),  # Attach to the second U object (body)
            bottom_spring_rest_length, stiffness, damping
        )
        space.add(bottom_spring)

        # Top spring
        top_spring = pymunk.DampedSpring(
            pogo_body, pogo_body_2,  # Bodies to connect
            (0, -100),  # Attach to the first U object (pogo)
            (width, -45),  # Attach to the second U object (body)
            top_spring_rest_length, 300, 10
        )
        space.add(top_spring)

        # Very top spring (The user does not control this one)
        very_top_spring = pymunk.DampedSpring(
            pogo_body, pogo_body_2,  # Bodies to connect
            (0, -100),  # Attach to the first U object (pogo)
            (0, -60),  # Attach to the second U object (body)
            15, 300, 10
        )
        space.add(very_top_spring)
        

        """Create a separate body for the jumping part of the pogo (single box) and a spring attaching that box"""
        box_mass = .1
        box_size = (width / 3, 2 * height / 3)

        jumping_box_body = pymunk.Body(box_mass, pymunk.moment_for_box(box_mass, box_size))
        jumping_box_body.position = (300, 475)  # Position the box elsewhere in the simulation
        space.add(jumping_box_body)

        jumping_box_shape = pymunk.Poly.create_box(jumping_box_body, box_size)
        jumping_box_shape.elasticity = 0.5
        jumping_box_shape.friction = 1
        space.add(jumping_box_shape)

        #Create a spring between the U-shaped body and the separate box body
        original_rest_length = 30  # Original rest length of the spring
        rest_length = original_rest_length
        spring_jump_distance = 100 # change the length of the spring to jump

        # Attach the spring to the center of the U-shaped object and the separate box
        jumping_spring = pymunk.DampedSpring(
            pogo_body, jumping_box_body,  # Bodies to connect
            (0, -75),  # Attach to the center-bottom of the U-shaped object (the middle of Box 2)
            (0, -50),  # Attach to the center of the separate box
            rest_length, stiffness, damping
        )
        space.add(jumping_spring)

        #set global variables that are used in get_current_state
        self.pogo_body = pogo_body
        self.pogo_body_2 = pogo_body_2
        self.top_spring = top_spring
        self.bottom_spring = bottom_spring
        self.jumping_spring = jumping_spring
        self.space = space