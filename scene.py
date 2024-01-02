from manim import *

import random

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation
class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        square.next_to(circle, RIGHT, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen
class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        square = Square()  # create a square

        self.play(Create(square))  # show the square on screen
        self.play(square.animate.rotate(PI / 4))  # rotate the square
        self.play(
            ReplacementTransform(square, circle)
        )  # transform the square into a circle
        self.play(
            circle.animate.set_fill(PINK, opacity=0.5)
        )  # color the circle on screen
class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()
class Chunks(Scene):
   
    def construct(self):
         # Define parameters
        num_rows = 1
        num_cols = 4
        square_size = 1
        spacing = 0
        
         # Create array of squares and corresponding text
        activeChunks = VGroup()
        for i in range(num_rows):
            for j in range(num_cols):
                square = Square(side_length=square_size, fill_color=BLUE, fill_opacity=0.7)
                square.move_to(
                    square_size * (i - (num_rows - 1) / 2) * UP +
                    square_size * (j - (num_cols - 1) / 2) * RIGHT +
                    spacing * i * UP +
                    spacing * j * RIGHT
                )
                text = Tex(f"({j})")  # Customize the text as needed
                text.next_to(square, DOWN, buff=0.1)

                textA = Tex("active").scale(0.5)  # Customize the text as needed
                textA.next_to(square, ORIGIN, buff=0.1)  # Replace "center" with "CENTER"

                activeChunks.add(VGroup(square, text, textA))
        activeChunks.shift(LEFT*5)


        #inactive
        inactiveChunks = VGroup()
        for i in range(num_rows):
            for j in range(num_cols+5):
                square = Square(side_length=square_size, fill_color=RED, fill_opacity=0.2)
                square.move_to(
                    square_size * (i - (num_rows - 1) / 2) * UP +
                    square_size * (j - (num_cols - 1) / 2) * RIGHT +
                    spacing * i * UP +
                    spacing * j * RIGHT
                )
                text = Tex(f"({j+num_cols})")  # Customize the text as needed
                text.next_to(square, DOWN, buff=0.1)

                textA = Tex("inactive").scale(0.5)  # Customize the text as needed
                textA.next_to(square, ORIGIN, buff=0.1)  

                inactiveChunks.add(VGroup(square, text, textA))
        inactiveChunks.shift(LEFT*5)
        inactiveChunks.shift(UP*2)

        #animation
        self.add(activeChunks)
        self.add(inactiveChunks)

        for i in range(5):
            self.play(activeChunks.animate.shift(LEFT*square_size), run_time=1)
            animations = []
            for chunk in activeChunks:
                if chunk.get_center()[0] < -self.camera.frame_width / 2:
                    # Select a random inactive chunk
                    inactive_chunk = random.choice(inactiveChunks)

                    # Store the color and text of the chunks in temporary variables
                    chunk_square = chunk[0]
                    chunk_text = chunk[2]
                    inactive_chunk_square = inactive_chunk[0]
                    inactive_chunk_text = inactive_chunk[2]

                    chunk_text_content = chunk_text.get_tex_string()
                    inactive_chunk_text_content = inactive_chunk_text.get_tex_string()

                    # Create new Tex objects with the switched text
                    new_chunk_text = Tex(inactive_chunk_text_content).scale(0.5)
                    new_inactive_chunk_text = Tex(chunk_text_content).scale(0.5)
                    # Position the new Tex objects
                    new_chunk_text.next_to(chunk_square, ORIGIN, buff=0.1)
                    new_inactive_chunk_text.next_to(inactive_chunk_square, ORIGIN, buff=0.1)

                    chunk[2] = new_chunk_text

                    inactive_chunk[2] = new_inactive_chunk_text

                    chunk_color = chunk_square.get_fill_color()
                    chunk_opacity = chunk_square.get_fill_opacity()
                    inactive_chunk_color = inactive_chunk_square.get_fill_color()
                    inactive_chunk_opacity = inactive_chunk_square.get_fill_opacity()

                    # Switch the color and opacity of the chunks
                    chunk_square.set_fill(inactive_chunk_color, opacity=inactive_chunk_opacity)
                    inactive_chunk_square.set_fill(chunk_color, opacity=chunk_opacity)

                    # Move the inactive chunk to the position of the offscreen chunk
                    aux = inactive_chunk.get_center()
                    inactive_chunk.move_to(chunk.get_center())
                    chunk.move_to(aux)

                    # Animate the inactive chunk moving to the right
                    animations.append(inactive_chunk.animate.shift(RIGHT * square_size*num_rows*num_cols))
                    inactiveChunks.remove(inactive_chunk)
                    activeChunks.remove(chunk)

                    # Add the offscreen chunk to the list of inactive chunks
                    inactiveChunks.add(chunk)
                    activeChunks.add(inactive_chunk)
            if(len(animations) > 0):
                self.play(*animations, run_time=.5)
