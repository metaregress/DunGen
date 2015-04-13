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
        self.parent = None
     
    def  getRandChild(self):
        print("seeking random child chamber to build")
        if len(self.passages) == self.passage_count:
            print("found full chamber: " + str(len(self.passages)) + " out of " + str(self.passage_count) + " in use")
            passage = random.choice(self.passages)
            chamber = random.choice(passage.chambers)
            return chamber.getRandChild()
        else:
            return self
        
    def __str__(self, level=0):
        return_string = "\t" * level + "A chamber of dimensions " + str(self.length) + " by " + str(self.width) + "\n"
        for passage in self.passages:
            return_string += passage.__str__(level+1)
        return return_string
        
#passage class
class Passage:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        #TODO: Passages currently just lead to chambers, make them able to branch etc.
        self.chambers = []
        self.parent = None
    
    def __str__(self, level=0):
        return_string = "\t" * level + "A corridor of dimensions " + str(self.length) + " by " + str(self.width) + "\n"
        for chamber in self.chambers:
            return_string += chamber.__str__(level+1)
        return return_string
        
class Door:
    pass

class Stairs:
    pass
    
def generateChamber():
    chamber_collection = []
    chamber_collection.append(Chamber(10,10,1))
    chamber_collection.append(Chamber(20, 20, 2))
    chamber_collection.append(Chamber(20, 30, 2))
    chamber_collection.append(Chamber(40, 40, 2))
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
    passage_collection.append(Passage(30, 10))
    passage_collection.append(Passage(20, 5))
    return random.choice(passage_collection)
    
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python DunGen.py [max_rooms] [num_levels]")
        exit()
    max_chambers = int(sys.argv[1])
    num_levels = int(sys.argv[2])
    print("creating dungeon with up to " + str(max_chambers) + " chambers")
    starting_areas = [Chamber(20, 20, 2), Chamber(30, 30, 2)]
    starting_area = random.choice(starting_areas)
    chambers = 1
    
    for p in range(starting_area.passage_count):
        if chambers < int(max_chambers):
            passage = generatePassage()
            starting_area.passages.append(passage)
            passage.parent = starting_area
    
    for passage in starting_area.passages:
        chamber = generateChamber()
        passage.chambers.append(chamber)
        chamber.parent = passage
        chambers += 1
     
    while chambers < max_chambers:
        rand_chamber = starting_area.getRandChild()
        passage = generatePassage()
        rand_chamber.passages.append(passage)
        passage.parent = rand_chamber
        child_chamber = generateChamber()
        passage.chambers.append(child_chamber)
        child_chamber.parent = passage
        chambers += 1

    print(starting_area)
        