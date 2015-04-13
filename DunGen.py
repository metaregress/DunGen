#A program to generate random D&D dungeons

import random
import sys

#room class
class Chamber:
    def __init__(self, length, width, passage_count):
        self.length = length
        self.width = width
        self.passage_count = passage_count
        self.passages = []
        
#passage class
class Passage:
    def __init__(self, length, width):
        self.legnth = length
        self.width = width
        #TODO: Passages currently just lead to chambers, make them able to branch etc.
        self.chambers = []
        
class Door:
    pass

class Stairs:
    pass
    
def generateChamber():
    chamber_collection = []
    chamber_collection.append(Chamber(10,10,1))
    chamber_collection.append(Chamber(20, 20, 2))
    return random.choice(chamber_collection)

def generatePassage():
    #I'm doing this kind of weirdly to keep in the spirit of rolling on a table, as well as not having a more elegant idea off-hand. I'm open to suggestions.
    passage_widths = []
    passage_widths.extend([5]*2)
    passage_widths.extend([10]*10)
    passage_widths.extend([20]*2)
    passage_widths.extend([30]*2)
    #TODO: the book makes a note of pillars being in a 40ft passage and height stuff; not sure how to capture that
    passage_widths.extend([40]*4)
    
    #TODO: can probably make these into json blobs or something for more sustainable storage
    passage_collection = []
    passage_collection.append(Passage(20, 10))
    return random.choice(passage_collection)
    
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [max_rooms] [num_levels]")
        exit()
    max_rooms = sys.argv[1]
    num_levels = sys.argv[2]
    print("creating dungeon with up to " + max_rooms + " rooms")
    starting_areas = [Chamber(20, 20, 2)]
    starting_area = random.choice(starting_areas)
    print("You are in a chamber " + str(starting_area.width) + " wide and " + str(starting_area.length) + " long. " + str(starting_area.passage_count) + " passages extend from here.")
    for p in range(starting_area.passage_count):
        #breadth first or depth first...?
        passage = generatePassage()
        starting_area.passages.append(passage)
        passage.chambers.append(starting_area)
    
    for passage in starting_area.passages:
        