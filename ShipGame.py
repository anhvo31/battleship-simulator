# Author: Anh Tuyet Vo
# GitHub username: anhvo31
# Date: 3/11/2022
# Description: The program is created as a portfolio project for CS 162. The program contains two classes and methods
# that allow two people to play the game Battleship. The players can place ships on a 10x10 grid. On their turn,
# they can fire a torpedo at a square on the enemy's grid. When a player sinks their opponent's final ship, they win.


class Ship:
    """Represents a ship created for the ShipGame class."""

    def __init__(self, length_of_ship, coordinate, orientation):
        """Creates a ship object with the specified length, starting coordinate, and orientation."""
        self._length_of_ship = length_of_ship
        self._starting_coordinate = coordinate
        self._orientation = orientation
        self._ship_coordinates = []
        self._number_of_hits = 0
        self._ship_status = True

    def place_ship(self):
        """
        Method to place the ship on the board.

        Returns False if:
        1. Length of ship is less than 2
        2. Ship will not fit on grid

        Otherwise, records the coordinates of the ship and returns True.
        """
        coord_lib = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8,
            "I": 9,
            "J": 10,
            "1": "A",
            "2": "B",
            "3": "C",
            "4": "D",
            "5": "E",
            "6": "F",
            "7": "G",
            "8": "H",
            "9": "I",
            "10": "J"
        }

        if self._length_of_ship >= 2:
            coord_letter = self._starting_coordinate[0]
            coord_num = int(self._starting_coordinate[1])
            coord_letter_num = coord_lib[coord_letter]
            if self._orientation == "R":
                self._ship_coordinates.append(self._starting_coordinate)

                for iteration in range(1, self._length_of_ship):
                    coord_num += 1
                    if coord_num <= 10:
                        next_coord = coord_letter + str(coord_num)
                        self._ship_coordinates.append(next_coord)
                    else:
                        return False

            elif self._orientation == "C":
                self._ship_coordinates.append(self._starting_coordinate)

                for iteration in range(1, self._length_of_ship):
                    coord_letter_num += 1

                    if coord_letter_num <= 10:
                        letter = coord_lib[str(coord_letter_num)]
                        next_coord = letter + str(coord_num)
                        self._ship_coordinates.append(next_coord)
                    else:
                        return False
            else:
                return False
        else:
            return False

    def get_coordinates(self):
        """Returns the list of coordinates of the ship."""
        return self._ship_coordinates

    def ship_hit(self):
        """Increment the number of hits taken by the ship."""
        self._number_of_hits += 1

    def is_sunk(self):
        """
        Checks whether the ship has been sunk.
        Returns True if the ship is sunk.
        Returns False if the ship is not sunk.
        """
        if self._number_of_hits >= self._length_of_ship:
            return True
        else:
            return False


class ShipGame:
    """
    A class to represent a Ship Game that is modeled after the game BattleShip.
    Each player has a 10x10 grid to place ships.

    The class contains functions to:
    1. Allows each player to place ships on their respective grid
    2. Returns the current state of the game
    3. Allows each player to fire a torpedo onto the opponent's board
    4. Returns the number of ships each player has left

    A ship is considered sunk when all of its squares have been hit. Each ship can be different lengths.
    The game is won when the player sinks the opponent's final ship.
    """

    def __init__(self):
        """Takes no parameter. Initializes the variables for the class."""
        self._player_1_ships = {}
        self._player_2_ships = {}
        self._player_1_ship_num = 1
        self._player_2_ship_num = 1
        self._record_all_firing = []
        # can be "FIRST_WON", "SECOND_WON", "UNFINISHED"
        self._current_state = "UNFINISHED"
        # can be "first" or "second"
        self._current_player_turn = "first"

    def get_current_state(self):
        """Returns the current state of the game."""
        return self._current_state

    def place_ship(self, player, length_of_ship, coordinate, orientation):
        """
        Takes the parameter:
        1. Player as a string
        2. Integer indicating the length of the ship
        3. Coordinate of the square it will occupy that is closest to A1 as a string
        4. Ship's orientation as a string (either 'R' or 'C')

        Method creates a Ship object.
        Calls validate_ship method to check whether the ship overlaps with another ship.

        Returns False if:
        1. Ship will not fit on grid
        2. Ship overlaps another ship
        3. Length of ship is less than 2

        Otherwise, returns True and add the Ship to the specified player's board.
        """
        ship = Ship(length_of_ship, coordinate, orientation)                # creates the Ship object

        if player == "first":
            if ship.place_ship() is not False:                             # if place_ship() execute successfully
                ship_coordinates = ship.get_coordinates()

                if self._player_1_ships == {}:
                    self._player_1_ships[self._player_1_ship_num] = ship
                    self._player_1_ship_num += 1
                    return True
                else:
                    if self.validate_ship("first", ship_coordinates) is True:
                        self._player_1_ships[self._player_1_ship_num] = ship
                        self._player_1_ship_num += 1
                        return True
                    else:
                        return False
            else:
                return False

        elif player == "second":
            if ship.place_ship() is not False:                             # if place_ship() execute successfully
                ship_coordinates = ship.get_coordinates()

                if self._player_2_ships == {}:
                    self._player_2_ships[self._player_2_ship_num] = ship
                    self._player_2_ship_num += 1
                    return True
                else:
                    if self.validate_ship("second", ship_coordinates) is True:
                        self._player_2_ships[self._player_2_ship_num] = ship
                        self._player_2_ship_num += 1
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False

    def validate_ship(self, player, ship_coordinates):
        """
        Takes the parameter of the player placing the ship and a list of the ship's coordinates.
        Validates ship's coordinates does not overlap with any existing ship's coordinates.

        Returns True if no overlap.
        Returns False if there is overlap.
        """
        no_overlap = False

        if player == "first":
            for key in self._player_1_ships:
                temp_ship = self._player_1_ships[key]                   # temp_ship contains the Ship object
                temp_ship_coordinates = temp_ship.get_coordinates()

                for coordinates in ship_coordinates:
                    if coordinates in temp_ship_coordinates:
                        no_overlap = False
                        return no_overlap                       # escapes the loop when it encounters a match
                    else:
                        no_overlap = True

        elif player == "second":
            for key in self._player_2_ships:
                temp_ship = self._player_2_ships[key]
                temp_ship_coordinates = temp_ship.get_coordinates()

                for coordinates in ship_coordinates:
                    if coordinates in temp_ship_coordinates:
                        no_overlap = False
                        return no_overlap
                    else:
                        no_overlap = True

        return no_overlap

    def fire_torpedo(self, player, target):
        """
        Takes the parameter:
        1. Player as a string
        2. Coordinate of the target as a string

        Returns False if:
        1. It is not the player's turn
        2. The game is already won

        Otherwise, returns True and:
        1. Updates the player's turn
        2. Records the move
        3. Updates the current state of the game

        If the specified player has fired a torpedo at the specific target before, the move is not recorded.
        """
        if player == self._current_player_turn:                            # enforcing player's turn
            if self._current_state == "UNFINISHED":
                if target not in self._record_all_firing:
                    self._record_all_firing.append(target)
                    num_of_sunken_ship = self.ship_sunk(self._current_player_turn, target)

                    if num_of_sunken_ship != 0:
                        if player == "first":
                            self.delete_ship("second", num_of_sunken_ship)
                            self._current_player_turn = "second"
                        elif player == "second":
                            self.delete_ship("first", num_of_sunken_ship)
                            self._current_player_turn = "first"
                    else:
                        if player == "first":
                            self._current_player_turn = "second"
                        elif player == "second":
                            self._current_player_turn = "first"

                    self.update_state()

                    return True

                else:
                    if player == "first":
                        self._current_player_turn = "second"
                    elif player == "second":
                        self._current_player_turn = "first"

                    return True
            else:
                return False
        else:
            return False

    def ship_sunk(self, player, target):
        """
        Takes the parameter of the player firing the torpedo and the target.
        Determines whether the hit has sunk a ship.

        If the no ship has been sunk by the target, returns 0.
        If a ship has been sunk by the target, returns the key (int) corresponding to the Ship object that was sunk.
        """
        sunken_ship = 0

        if player == "first":
            for key in self._player_2_ships:
                ship = self._player_2_ships[key]
                ship_coordinates = ship.get_coordinates()

                if target in ship_coordinates:
                    ship.ship_hit()
                    if ship.is_sunk() is True:
                        sunken_ship = key              # using a return statement here causes the loop to stop looping

        elif player == "second":
            for key in self._player_1_ships:
                ship = self._player_1_ships[key]
                ship_coordinates = ship.get_coordinates()

                if target in ship_coordinates:
                    ship.ship_hit()
                    if ship.is_sunk() is True:
                        sunken_ship = key

        return sunken_ship

    def delete_ship(self, player, ship):
        """
        Takes the parameter of the player whose ship was sunk and the key (int)
        corresponding to the Ship object that was sunk.

        Deletes the ship from the specified player's board.
        """
        if player == "first":
            del self._player_1_ships[ship]
        elif player == "second":
            del self._player_2_ships[ship]

    def update_state(self):
        """
        Determines whether a game has been won.
        Calls the method get_num_ships_remaining to determine the condition.

        If a player has won, the method updates the current state of the game.
        """
        if self.get_num_ships_remaining("first") == 0:
            self._current_state = "SECOND_WON"
        elif self.get_num_ships_remaining("second") == 0:
            self._current_state = "FIRST_WON"
        else:
            self._current_state = "UNFINISHED"

    def get_num_ships_remaining(self, player):
        """
        Takes the parameter of the string containing the player's turn.
        Returns the number of ship(s) the specified player has remaining.
        """
        if player == "first":
            return len(self._player_1_ships)                # returns length of the dictionary
        elif player == "second":
            return len(self._player_2_ships)


# test code
def main():
    game = ShipGame()
    game.place_ship('first', 2, 'B2', 'C')              # ship at C2, B2
    game.place_ship('second', 2, 'H2', 'R')             # ship at H2, H3
    print(game.fire_torpedo('first', 'H3'))
    print(game.fire_torpedo('second', 'C2'))
    print(game.fire_torpedo('first', 'H2'))
    print(game.fire_torpedo('second', 'B3'))
    print(game.get_current_state())


if __name__ == '__main__':
    main()
