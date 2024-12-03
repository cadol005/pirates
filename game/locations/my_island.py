
from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import random
from game.context import Context

class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)


class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['south'] = self
    
    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()


class Ghost_Ship(Context, event.Event):
    print("The fog around the ship begins to thicken and ghostly ship peaks through")
    def __init__(self):
        super().__init__()
        self.name = "ghost ship"
        self.events = ["You see treasure on the boat",
              "You hear strange nosies coming from the ship",
              "The captain of the ghos ship challenges you to a duel",
              "The ship silently and slowly floats by as a figure stares from the ship",
              ]
        self.event = random.choice(self.events)
        self.verbs['approach'] = self
        self.verbs['flee'] = self
        self.verbs['attack'] = self
        self.result = {}
        self.go = False
    
    def process(self):
         print("The fog around the ship begins to thicken and ghostly ship peaks through with a ghostly figure in the cockpit")
         monsters = []
         print(self.event)
    
    def process_verb (self, verb, cmd_list, nouns):
        
        if (verb == "approach"):
            self.result["message"] = "you carefully get closer to the ghost ship and sneak on"
            Treasue()
        if (verb == "flee"): 
            self.result["message"] = "You try to flee but the ship starts follwing close behind and jump om from there ship"
            monsters = [combat.Drowned("Drowned pirate "+str(n)), combat.Ghost_captain("Captain "+str(n))]
            combat.Combat(monsters).combat()
        
        if (verb == "attack"):
            self.result["message"] = "You and your crew get ready to engage in combat with the ship"
            monsters = [combat.Drowned("Drowned pirate"), combat.Ghost_captain("Captain")]
            min = 2
            uplim = 6
        if random.randrange(2) == 0:
            min = 1
            uplim = 5
            monsters.append(combat.Drowned("Pirate captain"))
            self.type_name = "Drowned Pirate Captain"
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.Drowned("Drowned pirate "+str(n)))
            n += 1
            combat.Combat(monsters).combat()




class Treasue():
    def __init__(self):
        self.result = {}
        self.loot = [items.Cutlass, items.Flintlock, items.Glock_switch]
        self.reward = random.choice(self.loot)
    
    def open_chest(self):
        self.result["message"] = "You open the chest slowly to reveal your loot"
        print(self.reward)







    