import random
import time

class Rooms:
    def __init__(self, rooms={}):
        self.rooms = rooms

    def add_room(self, room):
        self.rooms[room.name] = room


class Player:
    def __init__(
        self,
        alive=True,
        life=3,
        hand="",
        inv=[],
        eat=False,
        drink=False,
        deaths=0,
        start=None,
    ):
        self.alive = alive
        self.life = life
        self.hand = hand
        self.inv = inv
        self.eat = eat
        self.drink = drink
        self.deaths = deaths
        self.position = start

    def alife(self):
        if self.life <= 0:
            self.alive = False
        else:
            return 1
    def lose_life(self, amount):
        self.life -= amount
        if self.life <= 0:
            print("You have died.")
            self.alive = False
        else:
            print(f"Carefull you have {self.life} lives left!")

    def combat(self, boss):
        if self.hand in ["knife", "rusty sword"]:
            print(f"You defend yourself with {self.hand} and scared the boss away!")
        else:
            print("You have nothing to defend yourself with!")
            self.lose_life(2)
            if self.alive:
                print("Run to find something so you can fight!!")

    def show_inventory(self):
        if self.inv:
            print("This is what you have:")
            for item in self.inv:
                print(f"- {item}")
        else:
            print("Your inventory is empty.")

    def changepos(self, newposition, rooms):
        newposition.lower()
        self.position = rooms[newposition]

    def move(self, direction):
        if self.position.name == "Hall" and hasattr(self.position, "has_hole") and self.position.has_hole:

            print("You didn't notice the hole in the floor and fall through!")
            self.position = house.rooms["Basement"]
            self.lose_life(2)
            self.position.has_hole = False
        elif direction in self.position.exits:
            new_room = self.position.exits[direction]
            self.position = house.rooms[new_room]
            print(f"\nYou moved {direction} to {new_room}\n")
            time.sleep(1)
            if boss.state == "sleep":
                print(self.position.description)
        else:
            print(f"I can't move {direction} from here.")


class Boss:
    def __init__(self, alive=True, life=6, state="sleep", current_room=None):
        self.alive = alive
        self.life = life
        self.state = state
        self.current_room = current_room

    def awaken(self):
        self.state = "awake"
        print("You have awoken the boss!!")

    def take_damage(self, amount):
        self.life -= amount
        if self.life <= 0:
            print("The Boss has been defeated!!")
            self.alive = False
        else:
            print(f"The boss has {self.life} left!")
    def is_alive(self):
        return self.alive


    def move_randomly(self, house):
        if self.state == 'awake' and self.current_room:
            possible_exits = list(self.current_room.exits.values())
            if possible_exits:
                new_room_name = random.choice(possible_exits)
                if new_room_name in house.rooms:
                    self.current_room = house.rooms[new_room_name]
                    print(f"The boss has moved to {self.current_room.name}.")
                else:
                    print("The boss tried to move to an invalid room.")


class Game:
    ...


class Room:
    def __init__(self, name, exits={}, description="", has_hole=False):
        self.name = name
        self.exits = exits
        self.objects = []
        self.description = description
        self.has_hole = has_hole

    def add_description(self, dep):
        self.description = dep

    def add_object(self, *object):
        self.objects.extend(object)

    def remove_object(self, object):
        self.objects.remove(object)

    def list_objects(self):
        return self.objects

    def remove_objects(self, object):
        if object in self.objects:
            self.objects.remove(object)

    ...


def play():
    global player
    global house
    global boss

    combat = False

    # Iniciate map:
    house = Rooms()

    # Create rooms here:
    forest = Room("Forest", {"north": "Mansion"})
    mansion = Room("Mansion", {"north": "Main Hall", "south": "Forest"})
    main_hall = Room(
        "Main Hall",
        {"south": "Mansion", "east": "Kitchen", "west": "Studio", "north": "Stairs"},
    )
    kitchen = Room("Kitchen", {"north": "Secret Room", "west": "Main Hall"})
    studio = Room("Studio", {"east": "Main Hall"})
    stairs = Room(
        "Stairs", {"up": "Second Floor", "down": "Basement", "south": "Main Hall"}
    )
    second_floor = Room(
        "Second Floor",
        {"east": "Baby Room", "west": "Boy's Room", "north": "Hall", "down": "Stairs"},
    )
    basement = Room("Basement", {"up": "Stairs"})
    baby_room = Room("Baby Room", {"west": "Second Floor"})
    boys_room = Room("Boy's Room", {"east": "Second Floor"})
    hall = Room("Hall", {"north": "Main Room", "up": "Attic", "south": "Second Floor"}, has_hole = True)
    main_room = Room("Main Room", {"south": "Hall"})
    attic = Room("Attic", {"down": "Hall"})
    secret_room = Room("Secret Room", {"south": "Kitchen"})

    # Add the rooms created to the game:
    house.add_room(forest)
    house.add_room(mansion)
    house.add_room(main_hall)
    house.add_room(kitchen)
    house.add_room(studio)
    house.add_room(stairs)
    house.add_room(second_floor)
    house.add_room(basement)
    house.add_room(baby_room)
    house.add_room(boys_room)
    house.add_room(hall)
    house.add_room(main_room)
    house.add_room(attic)
    house.add_room(secret_room)
    #print(house.rooms)

    # Add items to the rooms:
    mansion.add_object("key")
    kitchen.add_object("cookie", "cup", "knife")
    studio.add_object("paper", "book")
    baby_room.add_object("marshmellow", "old toy")
    boys_room.add_object("pencil", "glass of water")
    main_room.add_object("secret key", "shatter mirrow")
    attic.add_object("rusty sword", "some bones", "candles")

    # print(f"Attic items: {attic.list_objects()}")

    # Add descriptions to the rooms:
    forest.add_description("Estas en un bosque y no hay anda al rededor, parece que este bosque te observa, sientes la presion de miles de personas viendote, este sentimiento...\n No me gusta nada estar aquí.")
    mansion.add_description("Te encuentras frente a una mansion enorme, la puerta esta abierta, parece que puedes entrar.\nDa algo de miedo por lo teticra que se ve, pero mejor eso que estar aqui afuera.")
    main_hall.add_description("La sala principal de la manison, parece oscura y muy maltratada, el olor del polvo me llena los pulmones y me irrita la garganta.\nLos cuadros parecen antiguos la verdad esta fea pero bastante mas grande de lo que se veia por fuera, raro.")
    kitchen.add_description("Una cocina bien fea con un refri medio raro, todas las cosas parece que estan en su lugar, pero siento que hay algo mas aquí de lo que se alcanza a mirar...")
    studio.add_description("Es un estudio como cualquier otro solo que muy oscuro para ver más")
    stairs.add_description("Pasas por las ecaleras, viejas como solo ellas, nisiquiera se como se mantien en pie, puedo subir y bajar, pero del sotano vienen unos sonido muy extraños...")
    basement.add_description("Este sotano esta muy oscuro, tanto que no veo nada, si tan solo tuviera unas velas")
    second_floor.add_description("El segundo piso se ve muy bien cuidado y limpio, hay luz que se cuela de algun sitio pero no se donde, luz azul? uh curioso...")
    baby_room.add_description("La habitacion de un bebe, me da miedo estar aquí, las cosas se mueven solas y en mi periferia una sombra me sigue, si da miedo estar aquí.")
    boys_room.add_description("La habitacion de un niño, parece que le gustan los jugetes o le gustaban, de cualquier modo, esta familia parece que era muy bien acomodada, que les habrá pasado?")
    hall.add_description("Un pasillo largo pero algo oscuro")
    main_room.add_description("La habitacion principal, esta muy limpia, alguien vive aqui?\nDefinitivamente alguien vive aqui, esto no puede estar así de limpio, comparado con el resto de habitaciones, esta es la que mas seguridad da, curioso como ese baul esta cerrado y no hay forma de abrirlo sin la llave.")
    attic.add_description("Wow el atico esta muy moderno, casi futurista! de aquí viene la luz azul que ilumina todo el segundo piso, impresionante!\n Ahora solo tengo una pregunta, quien rayos vive aquí?")
    secret_room.add_description("Esta habitacion... ME RECUERDA ALGO... no... se... como sea debo seguir igual aquí no hay nada\nBueno quizá...")
    # print(house.current_room())

    # Remove items to the rooms with: name.remove_object(item)

    # Set initial room for the player:
    player = Player(start=forest)

    # Set initial room for boss:
    boss = Boss(current_room=house.rooms["Basement"])

    # Loop to test:
    onstart = False
    while player.alife() == 1 and boss.is_alive():
        if onstart == False:
            print("Welcome to my game, i hope you like it\nIf you have any question about how to play use 'help'\nObjetive kill Boss.")
            time.sleep(2)
            print(f"You got {player.life} lifes, make them count.\n\n\n")
            time.sleep(2)
            print("You awake on a Forest, lost and with nothing more than your guts.\n")
            time.sleep(2)
            print(player.position.description)
            onstart = True

        action = input("\nwhat do you want to do? ").lower()

        if player.position == boss.current_room and boss.state == "awake":
            combat = True
            while combat and player.alife() and boss.is_alive():
                print("You're facing the boss! Do you want to 'attack' or 'escape'?")
                combat_action = input("> ").lower()

                if combat_action == "attack":
                    attack()
                elif combat_action == "escape":
                    if escape():
                        combat = False
                else:
                    print("That's not a valid action, you lose your turn!")

                if boss.is_alive() and combat:

                    print("The boss is preparing for its next move...")


        if boss.state == "awake":
            boss.move_randomly(house)

        if action.startswith("take "):
            item_name = action.split(" ", 1)[1]
            take(item_name)

        elif action.startswith("drop "):
            item_name = action.split(" ", 1)[1]
            drop(item_name)

        elif action == "look":
            look()

        elif action.startswith("equip "):
            item_name = action.split(" ", 1)[1]
            equip(item_name)

        elif action == "jump":
            jump()
            if random.random() < .5:
                boss.awaken()

        elif "help" in action:
            help()

        elif "talk" in action:
            talk()
            if random.random() < .3:
                boss.awaken()

        elif "search" in action:
            search()
        elif action == "inventory" or action == "show inventory":
            player.show_inventory()

        elif "move" in action or "go" in action:
            player.move(action.split(" ")[1])

        elif action == "quit":
            break

        else:
            print("Alch no se que quieres hacer")
            ...
    ...


def move(direction):
    player.move(direction)

    ...

def look():
    current_room = player.position

    print(f"Looking around in the {current_room.name}:")
    time.sleep(2)
    print(current_room.description)
    print("Posible direcctions:")
    time.sleep(2)
    for direction in current_room.exits.items():
        print(f"- {direction}")

    if hasattr(current_room, "has_hole") and current_room.has_hole:
        print("There's a hole on the ground carefull!")

def search():
    current_room = player.position
    if current_room.objects:
        print("You find something!")
        for item in current_room.objects:
            print(item)
    else:
        print("You didn't find anything at all.")
    ...


def take(item_name):
    current_room = player.position
    inventory = player.inv

    if item_name in current_room.objects:
        current_room.remove_objects(item_name)
        inventory.append(item_name)
        print(f"You take the {item_name} and added it to youre inventory!")
    else:
        print(f"The {item_name} is not here to take.")
    ...

def drop(item_name):
    current_room = player.position
    inventory = player.inv

    if item_name in inventory:
        inventory.remove(item_name)
        current_room.add_object(item_name)
        print(f"You have dropped {item_name}!")
    else:
        print(f"You don't have {item_name}.")
    ...

def attack():
    if player.hand in ["knife", "rusty sword"]:
        print(f"You attack the boss with {player.hand}")
        boss.take_damage(3)
    else:
        print(f"You attack the boss with {player.hand}")
        boss.take_damage(1)
        if boss.is_alive():
            print("The Boss attack!")
            player.lose_life(2)

def escape():
    if random.random() < 0.4:
        print("You manage to escape!")
    else:
        print("You barely escape!")
        player.lose_life(1)

def jump():
    current_room = player.position

    if hasattr(current_room, "has_hole") and current_room.has_hole:
        print("You jump over the hole in the floor!")
        current_room.has_hole = False
    else:
        print("You jump up and down like for what reason???")
    ...


def equip(item_name):
    inventory = player.inv
    current_equipped = player.hand

    if item_name in inventory:
        player.hand = item_name
        print(f"You have equipped {item_name}!")
    else:
        print(f"You don't have {item_name}.")
    ...

def talk():
    prhases = [
        "There's no one here I can talk to.",
        "There's no one, why talk alone?",
        "Yes, I'm crazy if I talk to myself.",
    ]
    print(random.choice(prhases))

def help():
    print(
        """Your available actions are:
          move: moves player in that direction (north, south, east, west)
          jump: jumps lol
          look: looks around and gives aditional info
          search: search the room
          take: takes item (when found)
          inventory: shows you your inventory
          equip: equips item if it can be equipped
          drop: drops selected item
          talk: character say somthing random
          help: gives a list of actions player might do"""
    )


def main():
    play()


if __name__ == "__main__":
    main()
