import random
from PIL import Image, ImageDraw
import PIL

from TuringMachine import TuringMachine
from CellularAutomata import CellularAutomata

# TuringMachine (states, starting_state, alphabet, transition_function, halting_state, tape_length, random_start, pointer))
# CellularAutomata (rule_number, already_in_base, neighborhood, states, random_first_row, width)

class CursedImage():
    def __init__(self, ca_width=200, tm_width=35, scale=1, generations=100):
        # Side length for each cell (10 -> each cell will be 10 pixels wide)
        self.scale = scale
        self.generations = generations

        self.tm_width = scale * tm_width
        self.ca_width = scale * ca_width
        # Setting parameters for image
        # Pixel buffer on left side, inbetween, and on right side of image
        self.buffer = 3 * scale
        self.image_width = scale * (ca_width + tm_width + (3 * self.buffer))
        self.height = (self.scale * self.generations) + (2 * self.buffer)
        # x-value 
        self.ca_start = self.tm_width + (2 * self.buffer)

        # Create Actual Image as CursedImage.im
        self.im = Image.new("RGB", (self.image_width, self.height), "#000000")

    # Pass the entire Turing Machine
    def create_image(self, tm, ca):
        image = ImageDraw.Draw(self.im)

        for gen in range(self.generations):
            # Draw Turing Machine State
            for index, cell in enumerate(tm.tape):
                x = self.buffer + self.scale * index
                y = self.buffer + self.scale * gen
                image.rectangle([x, y, x+self.scale, y+self.scale],
                    fill = tm.colors[cell])
            #print(ca.curr_row)
            for index, cell in enumerate(ca.curr_row):
                x = self.ca_start + self.scale * index
                y = self.buffer + self.scale * gen
                image.rectangle([x, y, x+self.scale, y+self.scale],
                    fill = ca.colors[cell])

            # Advance Generations
            tm.advance_generation()
            # Use the new tape values as the values for the Cellular Automata
            ca.advance_generation(rule_values=tm.tape)
            #ca.advance_generation()


def main():
    # Creat
    ca = CellularAutomata(rule_number=None, already_in_base=True, neighborhood=3, states=('0', '1', '2'),
        random_first_row=False, width=500)
    # Almost nothing is defined because we're just using the default (2,3) Turing Machine
    tm = TuringMachine(tape_length=len(ca.rule_input_keys), 
        halting_state=None, random_start=True)

    image = CursedImage(tm_width=tm.tape_length, scale=10, generations=500, ca_width=ca.width)
    image.create_image(tm=tm, ca=ca)
    image.im.show()

main()