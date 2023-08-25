# Battleship+
CZ1003 project. This is an upload of an old project done

Grading requirements:
* Strong password criteria (5)
* File operation and Exception handling (5) 
* Use of Dictionary (5)
* Use of tuple, list (5)
* Program correctness: Program produces the right output under all possible scenarios highlighted in the assignment guideline (20)
* Program organisation: Function, module (5)
* Programming style: Clarity and comprehensibility of code, appropriate use of variable/value/function names, indentations, comments and documentation.(5)
* Interface Design. User-friendliness: User controls are simple and intuitive, clear display of game progress that is comfortable for viewing, easily-understandable game instructions and output. (20)
* Teamwork & Presentation (10)
* Individual Oral Assessment (20)

### Account Creation Requirement:
Requirement:
 
#### File handling:
A file is used to store user information to simulate register and login function.
 
#### Once the program starts
Ø  New user registration: enter user name (make sure it is unique), date of birth, password to store in the file
 
#### String operation
The password must meet the following common criteria:<br>
*    	The length of the password is more than 8 characters
*    	At least one upper case letter
*    	At least one lower case letter
*    	At least one digit
*    	At least one special symbol (punctuation)
*    	Cannot contain user name
 
#### Exception handling for file operation
If the file cannot be found, need handle the exception. E.g., New text file will be created if there is no pre-existing file.

### Login Requirement:
Existing user needs enter user name and password to login. User name and password must match the one stored in the file to login. The users can try three times before the account is locked. Once the account is locked, the user has to answer question to activate the account, in our system, the question is date of birth.

#### Position the Battleships
The battleship board will be 10 rows, 10 columns, 2 depth layers (10 x 10 x 2). Among the depth layers, one represents the sea surface while the other represents the subsea. The length of the ships are as follows.
•	1 x Carrier: 4 units
•	1 x Submarine: 3 units

A ship takes up continuous boxes and can only oriented in a horizontal or vertical manner. A Carrier cannot be placed in the subsea layer, while a submarine can be placed on either of these two layers. Within the same layer, ships cannot be placed on one another, i.e. no overlapping coordinates. 


You can make use of up to 4 boards to track the progress of the game, each containing information of both the surface and the subsea layer. For example,

User’s ship placement board <br>
User’s targeting board <br>
Computer’s ship placement board <br>
Computer’s targeting board 

### Actual Game/Playing:

Note: You are not required to implement any form of “intelligence” in the computer’s selection of targets. Random targets will suffice for this assignment.

After the user and computer has placed all the ships, the user will be prompted to enter a target coordinate. The program then reports if it is a hit or miss and records it accordingly in the board. The computer then makes its move (selects a coordinate) and its results are also recorded respectively. In this version of Battleship, an attack does not only have impact on a grid, but also all the grids surrounding it. For example, for a target coordinate of (3,3,1), the affected targets are: (3,3,1), (4,3,1), (2,3,1), (3,4,1), (3,2,1), (2,2,1), (2,4,1), (4,2,1) and (4,4,1). This continues until either the player or computer’s ship are all sunk. Announce the winner and end the program

