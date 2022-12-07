# Group#:           G2
# Student Names:    Idil Bil & Suhail Khalil
# student numbers:  21344189 - 56517816

"""
    This program implements a variety of the snake 
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue        #the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self, queue, game):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour, 
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self, queue, gui):
        self.queue = queue
        self.gui = gui
        self.queueHandler()
    
    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules 
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self, queue):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = queue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15     #speed of snake updates (sec)
        while self.gameNotOver:
            time.sleep(SPEED)               #Use sleep to implement a delay that sets how often "move" tasks are generated
            self.move()                     #Run the move method first before putting a move task in the queue such that the SnakeCoordinates list is updated first then the snake is redrawn.
            self.queue.put_nowait({"move": self.snakeCoordinates})

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """

        #Start by defining a helper function called CheckRange that checks if a value is within center-lowerlimit and center+upperlimit
        #Since we deal boundaries that are floats and python's "in range()" handles integers only this saves us having to convert boundary coordinates to integers and decide on whether to round or truncate towards zero
        def checkRange(value: float, center: float, lowertolerance: float, uppertolerance: float) -> bool:
            if (center-lowertolerance) <= value <= (center+uppertolerance):
                return True
            else:
                return False

        #DESIGN DECISION EXPLANATION:
        #In order to ensure that a generated prey is entirely contained within the snake before capture we check that the center of the prey is within 5 pixels of the center of the snake to account for width 
        #Note: Ideally, this would be 2.5 to ensure that the prey is ONLY captured if fully contained in the snake.
        #We start by realising that if the snake is moving to the right the y coordinates of the snake go from NewSnakeCoordinates[1]-7.5 to NewSnakeCoordinates[1]+7.5 but since the prey dimensions go 5 pixels in either direction from its center that only allows the prey's centre to be +-2.5 pixels from the Snake's head coordinates
        #However, this is troublesome with Coordinates such at (240,60) for example as it is uncapturable when moving up or down or left or right (note that when moving up or down the x coordinates of the snake go from NewSnakeCoordinates[0]-7.5 to NewSnakeCoordinates[0]+7.5)
        #As if moving up, sure 240 can be contained within the generated square (new head position) but the y-coordinate is out of bounds of 55+-2.5 and if moving down 60 can be contained within the generated square but not 240 as it out of bounds of 245+-2.5
        #This is a design limitation due to us defining the coordinates of the snake as always being multiples of 5 but not 10 (245,235,225 etc) and the snake always moving in increments of 10.
        #So while using a tolerance of 5 to check if a prey will be captured does offer a 5 pixel error range (2.5 + 2.5) where a prey might be slighly not encompassed by the snake yet captured,
        #however this was the only way to always keep the game progressing without uncapturable squares being generated (especially since square generation has to be truly random and can't adhere to strict rules that only generate capturable squares as was my first attempt.)

        WIDTHTOLERANCE = 5
        NEWCOORDINATE_DIMENSIONS = 10

        NewSnakeCoordinates = self.calculateNewCoordinates()
        self.snakeCoordinates.append(NewSnakeCoordinates)                                   #Add the generated coordinate to the end of the snakeCoordinate list (creating a new head and causing apparent motion)
        self.isGameOver(NewSnakeCoordinates)                                                #Check to see if the new head's position after motion would cause the game to end
        preycoords = gui.canvas.coords(gui.preyIcon)                                        #Extract the prey's coordinates from the gui object by using the coords method on the canvas (allowed since we are using Threading and the move method is never called before the gui object is instantiated)
        preycenter = ((preycoords[0]+preycoords[2])/2,(preycoords[1]+preycoords[3])/2)      #Average out x1 and x2 and y1 and y2 to get the coordinates of the center (effectively our generated x,y from the createNewPrey method)

        #This if conditional checks to see if our prey is captured. 
        #Test is different depending on what direction the snake is moving as if it is moving to the right for example then we know our NewSnakeCoordinate's x coordinate has increased by NEWCOORDINATE_DIMENSIONS and so we test 10 points to the left of it to see if our prey's centre lies in that region (i.e, within the NewSnakeCoordinates x-bounds as we treat it as a rectangle)
        #And following on the above example, if moving to the right we know that our y-coordinate is the one affected by the width parameter and so we test our prey's y to see if it is WIDTHTOLERANCE away from the centre of our new snake's position.
        #So depending on if the snake is moving Left or Up or Down or Right different tests are performed that all surmount to checking if the snake's new position would cause it to capture a prey

        if ((self.direction == "Left") and checkRange(NewSnakeCoordinates[1],preycenter[1],WIDTHTOLERANCE,WIDTHTOLERANCE) and checkRange(NewSnakeCoordinates[0],preycenter[0],0,NEWCOORDINATE_DIMENSIONS))\
             or ((self.direction == "Right") and checkRange(NewSnakeCoordinates[1],preycenter[1],WIDTHTOLERANCE,WIDTHTOLERANCE) and checkRange(NewSnakeCoordinates[0],preycenter[0],NEWCOORDINATE_DIMENSIONS,0))\
             or ((self.direction == "Up") and checkRange(NewSnakeCoordinates[0],preycenter[0],WIDTHTOLERANCE,WIDTHTOLERANCE) and checkRange(NewSnakeCoordinates[1],preycenter[1],NEWCOORDINATE_DIMENSIONS,0))\
             or ((self.direction == "Down") and checkRange(NewSnakeCoordinates[0],preycenter[0],WIDTHTOLERANCE,WIDTHTOLERANCE) and checkRange(NewSnakeCoordinates[1],preycenter[1],0,NEWCOORDINATE_DIMENSIONS)):

            #If a prey has been captured update the score, put a "score" task in the queue and run the createNewPrey() method 
            #(also note that the tail of the snake isn't popped effectively making it longer)
            self.score += 1
            self.queue.put_nowait({"score": self.score})
            self.createNewPrey()
        else:
            self.snakeCoordinates.pop(0)     #Pop the tail of the snake to visually cause motion and keep the snake of fixed length
        
    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]

        #Since the snake is defined as a collection of points whose dimensions change in increments of 10, it moves in increments of 10
        #Remember: increasing x is to the right
        #Remember: increasing y is to the bottom

        if self.direction == "Left":
            return((lastX-10,lastY))
        elif self.direction == "Right":
            return((lastX+10,lastY))
        elif self.direction == "Up":
            return((lastX,lastY-10))
        else:
            return((lastX,lastY+10))

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        x, y = snakeCoordinates
        #Check if our new head's position is out of bounds or is in the snakeCoordinates list (i.e., it bit itself)
        #(barring the last element in the list, as this method is called after the NewSnakeCoordinate is appended to the snakeCoordinates list)
        #If game is over then set the gameNotOver flag to false to kill the superloop
        #And put a "game_over" task in the queue
        if x > 500 or x < 0 or y > 300 or y < 0 or (x,y) in self.snakeCoordinates[0:-1]:
            self.gameNotOver = False
            self.queue.put_nowait({"game_over": True})

    def createNewPrey(self) -> None:
        """ 
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). 
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
        THRESHOLD = 15   #sets how close prey can be to borders
       
        x , y = (0,0)    #Initialise them at 0 so the loop runs at least once
        
        while x <= 130 and y <= 30: #To provide enough room around the score counter so prey never spawns inside of it (this allows scores up to 3 digits without interferance)
            x , y = random.randint(THRESHOLD,WINDOW_WIDTH-THRESHOLD), random.randint(THRESHOLD,WINDOW_HEIGHT-THRESHOLD)     #Randomly generate prey inside the canvas and THRESHOLD away from the walls
        self.queue.put_nowait({"prey": (x-5,y-5,x+5,y+5)})      #Upon generating a new prey position put a "prey" task in the queue


if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300 
    SNAKE_ICON_WIDTH = 15
    
    BACKGROUND_COLOUR = "purple"  #you may change this colour if you wish
    ICON_COLOUR = "pink"          #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game(gameQueue)        #instantiate the game object

    gui = Gui(gameQueue, game)    #instantiate the game user interface
    
    QueueHandler(gameQueue, gui)  #instantiate our queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()
    
    



    #OLD ATTEMPTS: Dr Farshid told us to include old attempts so we will keep them here for clarity and cleanliness.

    #INITAL ATTEMPT 1: (for CreateNewPrey) Tried to generate prey in positions where both the x and y coords are multiples of 5 but not 10 to simplify prey capture, which is incorrect
        # x , y = -1, -1 
        # while x % 10 != 0 or y % 10 != 0 or (x,y) in self.snakeCoordinates: 
        #     x , y = random.randrange(THRESHOLD,WINDOW_WIDTH-THRESHOLD,5), random.randrange(THRESHOLD,WINDOW_HEIGHT-THRESHOLD,5)
        # self.queue.put_nowait({"prey": (x-5,y-5,x+5,y+5)})

    #INITAL ATTEMPT 2: (for move) Tried to use the exact coordinates of the two points defining the prey for capture instead of using the center, accounting for the width of the snake
    #def move(self) -> None:
        # """ 
        #     This method implements what is needed to be done
        #     for the movement of the snake.
        #     It generates a new snake coordinate. 
        #     If based on this new movement, the prey has been 
        #     captured, it adds a task to the queue for the updated
        #     score and also creates a new prey.
        #     It also calls a corresponding method to check if 
        #     the game should be over. 
        #     The snake coordinates list (representing its length 
        #     and position) should be correctly updated.
        # """
        # NewSnakeCoordinates = self.calculateNewCoordinates()
        # #complete the method implementation below
        # self.snakeCoordinates.append(NewSnakeCoordinates)
        # self.isGameOver(NewSnakeCoordinates)
        # preycoords = gui.canvas.coords(gui.preyIcon)
        # preycoords1 = tuple(preycoords[0:2])
        # preycoords2 = tuple(preycoords[2::])
        # yrange_with_width = range(int(NewSnakeCoordinates[1]-9),int(NewSnakeCoordinates[1]+8))
        # xrange_with_width = range(int(NewSnakeCoordinates[0]-9),int(NewSnakeCoordinates[0]+8))
        # yrange_no_width = range(0)
        # xrange_no_width = range(0)
        # correctionfactor = 0 #only needed if I have to use -3rd index of snakeCoordinates, else can just be elimated and replaced with 10 in all calcs as -1 always matches because of how newcoordinate works
        # if self.direction == "Up":
        #     if self.snakeCoordinates[-2][0] == NewSnakeCoordinates[0]:
        #         correctionfactor = -10  
        #     yrange_no_width = range(int(NewSnakeCoordinates[1]+correctionfactor),int(NewSnakeCoordinates[1]+11))
        # elif self.direction == "Down":
        #     if self.snakeCoordinates[-2][0] == NewSnakeCoordinates[0]:
        #         correctionfactor = 10 
        #     yrange_no_width = range(int(NewSnakeCoordinates[1]-10),int(NewSnakeCoordinates[1]+1+correctionfactor))
        # elif self.direction == "Left":
        #     if self.snakeCoordinates[-2][1] == NewSnakeCoordinates[1]:
        #         correctionfactor = -10
        #     xrange_no_width = range(int(NewSnakeCoordinates[0]+correctionfactor),int(NewSnakeCoordinates[0]+11))
        # elif self.direction == "Right":
        #     if self.snakeCoordinates[-2][1] == NewSnakeCoordinates[1]:
        #         correctionfactor = 10
        #     xrange_no_width = range(int(NewSnakeCoordinates[0]-10),int(NewSnakeCoordinates[0]+1+correctionfactor))
        
        # #Debugging lines:
        # print(*xrange_no_width)
        # print(*xrange_with_width)
        # print(*yrange_no_width)
        # print(*yrange_with_width)
        # print(preycoords1, preycoords2) 

        # if ((self.direction == "Left" or self.direction == "Right") and (preycoords1[1] in yrange_with_width) and (preycoords2[1] in yrange_with_width) and (preycoords1[0] in xrange_no_width) and (preycoords2[0] in xrange_no_width)) or ((self.direction == "Up" or self.direction == "Down") and (preycoords1[1] in yrange_no_width) and (preycoords2[1] in yrange_no_width) and (preycoords1[0] in xrange_with_width) and (preycoords2[0] in xrange_with_width)): #FIXXXXXXXXXXXXXX THIS NEEDS TO CHECK IF WE CAPTURE PREY
        #     self.score += 1
        #     self.queue.put_nowait({"score": self.score})
        #     self.createNewPrey()
        # else:
        #     self.snakeCoordinates.pop(0)