from project import Player, Room, Boss, search, jump, talk, drop, take

def test_player_movement():

    start_room = Room("Start", {"north": "End"})
    end_room = Room("End", {"south": "Start"})
    player = Player(start=start_room)


    player.move("north")
    assert player.position.name == "End", "El jugador no se movió al norte correctamente."

def test_combat_damage():

    player = Player(hand="knife")
    boss = Boss(life=6)

    player.attack_boss(boss)
    assert boss.life < 6, "El jefe no recibió daño correctamente."

def test_search():

    room_with_items = Room("Kitchen")
    room_with_items.add_object("knife")
    player = Player(start=room_with_items)

    items_before = len(player.position.objects)
    search()
    items_after = len(player.position.objects)

    assert items_before > items_after, "Search dont find items correctly"

def test_drop_and_take():

    room = Room("Bedroom")
    player = Player(start=room)
    player.inv.append("book")

    take("book")
    assert "book" in player.inv, "La función take no añade objetos al inventario."

    initial_inv_size = len(player.inv)
    drop("book")
    assert "book" not in player.inv and len(player.inv) < initial_inv_size, "La función drop no elimina objetos del inventario correctamente."

def test_jump():
    room_with_hole = Room("Hall", has_hole=True)
    player = Player(start=room_with_hole)

    jump()
    assert not player.position.has_hole, "La función jump no maneja correctamente el hoyo."

def test_talk():
    player = Player()

    assert talk(), "La función talk no produce ninguna salida."