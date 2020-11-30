
class Hero:
  def __init__(self):
    self.name = "hero"
    self.health = 100
    self.stength = 5
    self.speed = 5
    self.stamina = 100
    
  
  def rest(self):
    print(hero.name + " is resting")
    self.stamina += 10
  
  def heal(self):
    if self.stamina >= 5:
      print(self.name + " is healing")
      self.health += 10
      self.stamina -= 5
    else:
      print(self.name + " does not have enough stamina to heal")
    
  
  def attack(self,other):
    if self.stamina >= 5:
      print(self.name + " attacks " + other.name)
      other.health -= self.strength
    else:
      print(self.name + " does not have enought stamina to attack")
      
class monster:
  def _init_(self):
      


hero = Hero()
hero.name = "jeff"

print(hero.name + " is born")
print(hero.name + " has " + str(hero.health) + " health")


print(hero.name + " is standing in a forest")
choice = input("does " + hero.name + " 1. take a nap, 2. explore the forest")
if choice == "1":
  print(hero.name + " decides to take a nap")
  hero.rest()
  choice = input("what should " + hero.name + " do next 1. take another nap, 2. explore the forest")
  if choice == "1":
    print(hero.name + " was eaten by a wolf in their sleep, GAME OVER")
    quit()
  if choice == "2":
    print("something else happens")
if choice == "2":
  print(hero.name + " explores the forest")
  print(hero.name + " is attacked by a wolf")
  hero.health -= 10
  print(hero.name + "was hurt by the wolf")

  
    
  


