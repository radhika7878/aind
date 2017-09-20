assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8','I9'],['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2','I1']]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        twins = []
        #Searches for all possible twins in a unit
        for i in range(0, len(unit)-1):
            val = values[unit[i]]
            if len(val) == 2:
                for j in range(i+1, len(unit)):
                    if val == values[unit[j]]:
                        twins.append(unit[i])
        #For all twins found in a unit removes the possibilities from the peers except the other twin
        for twin in twins:
            val = values[twin]
            if(len(val)==2):
                for box in unit:
                    if len(values[box]) > 1 and values[box] != val:
                        values[box] = values[box].replace(val[0], '')
                        values[box] = values[box].replace(val[1], '')

    return values                


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    sodoku_dict = {}
    i=0
    for c in grid:
        if c == '.':
            sodoku_dict[boxes[i]] = "123456789"
        else:
            sodoku_dict[boxes[i]] = c
        i +=1
    return sodoku_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    #Call naked twins to reduce possibilties of each box and maybe getting a solution for some and hence resulting in better elimination
    values = naked_twins(values)
    #Removes possibility of a solved boxes value from its peers
    for key in values:
        #Check if box is solved
        if len(values[key]) == 1:
            sol = values[key]
            #Removed solved value from all peers of a box
            for peer in peers[key]:
                values[peer] = values[peer].replace(sol, '')
                
    return values

def only_choice(values):
    #Finds if there is any digit which can be in only only box in a unit and assign the box that digit
    for unit in unitlist:
        for num in '123456789':
            #possList stores all the boxes in a unit which can be assigned a digit
            possList = []
            for box in unit:
                if num in values[box]:
                    possList.append(box)
            #If there is only one box which can contain a particular digit, assign it to that box
            if len(possList) == 1:
                assign_value(values, possList[0], num)
                values[possList[0]] = num
        
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    solved = True
    if values is False:
        return False
    for box in boxes:
        if len(values[box]) != 1:
            solved = False
            break
    if solved:
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    min = 9
    for box in boxes:
        if len(values[box]) != 1 and len(values[box]) < min:
            min = len(values[box])
            chosenBox = box
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for c in values[chosenBox]:
        new_dict = values.copy()
        new_dict[chosenBox] = c
        ans = search(new_dict)
        if ans:
            return ans

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    ans = search(values)
    return ans

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    test_grid = '......4...7......3.12..5............7.....28...6......8......4....8.........719.8'
    display(solve(test_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
