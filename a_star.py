import pygame
import time
from queue import PriorityQueue  #gets the min number of the queue


pygame.init()
myfont1 = pygame.font.SysFont('Comic Sans MS', 25, bold = True)
myfont = pygame.font.SysFont('Comic Sans MS', 14, bold = True)
#I am using a square window, so defined only width
width = 800

#For the window
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Path Finding Algorithm")

#Colours I'm gonna use
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0,128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
FUCHSIA = (255, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)



#All the nodes in the grid (window)
class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

    #to get the position of the node
	def get_pos(self):
		return self.row, self.col

    #closed is the block which is closed amd already checked (we use red for this)
	def is_closed(self):
		return self.color == CYAN

    #open is for not closed 
	def is_open(self):
		return self.color == GREEN

    #Barrier is the black walls we draw
	def is_barrier(self):
		return self.color == BLACK

    #The start node
	def is_start(self):
		return self.color == MAGENTA

    #The ending node
	def is_end(self):
		return self.color == ORANGE

    #If we right click it should become blank again
	def reset(self):
		self.color = WHITE

    #These are to make the methods mentioned above
	def make_start(self):
		self.color = PURPLE

	def make_closed(self):
		self.color = CYAN

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def remove_open_closed(self):
		self.color = WHITE

	def make_end(self):
		self.color = BLUE

	def make_path(self):
		self.color = ORANGE
		pygame.draw.rect(win, BLACK, [10, 10, 10, 10])

	def draw(self, win): 
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []         #every single node's neighbours
        #we check up,down,left,right, if the neighnouring is not barrier, we should add them into neighbours list
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN (first ,we are mamking sure we are not in the last row, then lastrow+1 will come out of the grid(so <totalrows+1); second, if the next row down(so row+1 cuz down) isnt a barrier, append it to the neighbours list)
			self.neighbors.append(grid[self.row + 1][self.col])     

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


#Calculating the heuristic function by using Manhattan Distance by absolute function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)      


#constructing path  
def construct_path(grid,came_from, current, draw,ctr,start,end):    #current node starts at the end node, we're gonna traverse from the end node back to the start node
    while current in came_from:            
        current = came_from[current]    #current will be equal to whatver we came from from the last node, from the end node, where we come from, thats current
        current.make_path()      #making that current part of the path
        end.make_end()      #so that the path doesnt overdraw on the end node covering it off
        start.make_start()
        ctr+=1
        draw()    #drawing and keep doinf that,, once we reach the node that came from the start node and we hit the start node, it'll stop constructing  the path
        for i in grid:
                for j in i:
                    if j.is_closed() or j.is_open():
                        j.remove_open_closed()
    dis = 'Distance = '+str(ctr)
    textsurface = myfont1.render(dis, True, OLIVE)
    win.blit(textsurface,(600,80))
    pygame.display.update()
    time.sleep(10)
    


#Original A* algorithm
def algorithm(draw,grid,start,end,ctr):
    count = 0        #to keep track of when we inserted an item, so that if we have two items with same f-score, we can go based on which was inserted first
    open_set = PriorityQueue()    #defining the open set which has f-value and the nodes, originally has starting node with f-value=0
    open_set.put((0,count,start))  #pushing the start node along with its f-val
    came_from = {}     #keeps track of which node that the present node came from


    #initially we set g-scores of all as 0 and f-scores of all nodes as infinity , except the f-score of start which will be the heuristic func
    g_score = {spot: float("inf") for row in grid for spot in row}     #sets g-score to infinity
    g_score[start] = 0         #g-score of start =0
    f_score = {spot: float("inf") for row in grid for spot in row}      #sets f-score to inf
    f_score[start] = h(start.get_pos(), end.get_pos())      #sets f score of start node as the heuristic func returned dist , cuz we wanna estimate how far the end node is from the start node when we begin, so that when we reach the end node, we dont automatically assume that thats the best node (if we circle all around back to the start node,, so that we dont take that as the shortest path cuz it was infifnity before hand)
    

    open_set_hash = {start}     #In priority queue we cant check if a particular node is present in the queue or not, so we use a set for that purpose to keep track of items in the priority queue(ie we have to check the open set for the f-score )


    while not open_set.empty():     #algorithm runs till the open set is empty(ie it has traversed all nodes, if open set is empty,that means we have checked every single neighbour possibility and if we havent found the path, the path doesnt exist
        for event in pygame.event.get():      #To make a way for the useer to exit
            if event.type == pygame.QUIT:
                pygame.quit()


        current = open_set.get()[2]    #I want the 2nd index item in open set, which is the node (it has fscore,count,node)
        # we have to pop the lowest value f-score from the openset, if two nodes have same f-score, we go by count, whatever is insesrted first will get popped
        #basically current is the starting node
        open_set_hash.remove(current)  #we're gonna take whatever node that we just popped out of the priorityq aand we are gonna synchronize it with the opensethash by removing it from that


        if current == end:   #if the node we just popped out is the end, this is the shortest path, we should construct the path, return true tells we founf the path
            construct_path(grid,came_from,end,draw,ctr,start,end)
            pygame.display.update()
            return True

        for i in current.neighbors:
            temp_g_score = g_score[current]+1    #we assume that all the edges are 1(non weighted graphs) so if we want to know what the temporary g_score of the neighbour would be, then we take currently known shortest distance and add 1 to it, cuz we're going one more node over, which is the neigh of this node


            if(temp_g_score<g_score[i]):     #if we found a better way to reach this neighbour than what we have found before,update
                #updating cuz this is the better path now
                came_from[i] = current    #cz its a neighbour of the current and that optimal shortest path neighbouur came from our current node
                g_score[i] = temp_g_score
                f_score[i] = temp_g_score+ h(i.get_pos(),end.get_pos())       #gets the position of the neighbour and the end and calls h func to calculate heuristic dist from neigh node which gave the lowest path to the end node
                if i not in open_set_hash:   #checking like this only possible in opensesthash, thats y we are using it
                    count+=1   #incrementing count for the neighboour if its not already in opensethash
                    open_set.put((f_score[i],count,i))   #pushing the three values of the neighbour to the openset
                    open_set_hash.add(i)    #adding the neighbour to the open set 
                    i.make_open()    #making this neighbour open so that we know that we have already considered this node
        draw()

        if current != start:     #if the node that we just considered is not the startnode, we make it closed cuz we already considered that node, and its not gonna be added back to openset
            current.make_closed()
 
    return None   #tells we didnt find the path 



#Making the main grid
def make_grid(rows, width) :
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])        #First we are creating an empty list and then append into that list (2D array)
		for j in range(rows):
			spot = Node(i, j, gap, rows)
			grid[i].append(spot)        #Appending the spot inside the list
	return grid


def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):       #For every row, drawing a horizontal line first
        pygame.draw.line(win, GREY, (0, i*gap) , (width, i*gap))        #Drawing the lines based on i value ex: i=1-> line starts from (0,16) to (800,16)

    for j in range(rows):       #For every row, drawing a horizontal line first
        pygame.draw.line(win, GREY, (j*gap, 0) , (j*gap, width))        #Drawing the lines based on i value ex: i=1-> line starts from (0,16) to (800,16)


def D(win, grid, rows, width):        #Drawing on the screen
	win.fill(WHITE)       #Filling the entire screen with white first then draw the grids
	for i in grid:
		for j in i:
			j.draw(win)      #draws a cube with its on colour (we're calling the draw func from Node class)
	draw_grid(win, rows, width)
	pygame.display.update()



def get_clicked_pos(pos, rows, width):     #pos - the mouse position
    gap = width//rows
    x, y = pos       # assigning the pos to x part and y part
    row = x // gap           #we're taking the position of x and dividing with the gap(width) which will give us what cube we clicked on
    col = y // gap
    return row, col


def main(win, width):

    win.fill('YELLOW')
    text1 = myfont.render('A* Path Finding Algorithm', True, BLACK)
    text2= myfont.render('A* Algorithm takes a start point and a goal and attempts to make the shortest path between the two nodes,', True, BLACK)
    text21 = myfont.render(' ignoring obstacles blocking the way.', True, BLACK)
    text3= myfont.render('You can select the starting node and ending node by pressing anywhere on the grid,', True, BLACK)
    text31 = myfont.render(' and create obstacles and see how the algorithm runs ignoring the obstacles', True, BLACK)
    text4 = myfont.render('the grid you select first and second becomes the starting and ending nodes respectively', True, BLACK)
    text41 = myfont.render(' and then you can create obstacles anywhere on screen, which are represented by black', True, BLACK)
    text5 = myfont.render('When you are ready, hit space bar to watch the algorithm run!', True, BLACK)
	
    win.blit(text1,(290,310))
    win.blit(text2,(0,360))
    win.blit(text21,(250,390))
    win.blit(text3,(100,440))
    win.blit(text31,(100,470))
    win.blit(text4,(100,520))
    win.blit(text41,(100,550))
    win.blit(text5,(100,600))


    pygame.display.update()
    time.sleep(20)

    rows = 50       #defining rows as 50 which is also equal to columns cuz its a square grid
    grid = make_grid(rows, width)       #To generate the grid and give us the 2d array of spots
    ctr = 0

    #Defining the start and end position as None initially
    start = None
    end =  None

    run = True      #For the while loopp to check when to stop
    while run:
        D(win, grid, rows, width)
        for event in pygame.event.get():      #Looping through all the events
            if event.type == pygame.QUIT:
                run = False  #If the user wants to quit , to be able to quit

            if pygame.mouse.get_pressed()[0]:     #Tells what mouse button is presseed  ->0 is left click, 2 is right clicked
                pos = pygame.mouse.get_pos()      #gives us the position of mouse on the screen
                row, col = get_clicked_pos(pos, rows,width)      #Calling the func to give us what exact position in the 2D list we clicked on
                spot = grid[row][col]       #indexing the row and column in the grid 

                #If he havent yet placed the start position, do that first
                if not start and spot !=end:
                    start = spot
                    start.make_start()

                #If we havent yet clicked the endc
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                #If we are not clicking on start and end, make it a barrier
                elif spot!= end and spot!= start: 
                    spot.make_barrier()



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:        #By space key and when the algo is not  started, to make sure we have a start and end before starting algorithm
                    for i in grid:
                        for j in i:
                            j.update_neighbors(grid)    #whenever we hit space key and we havent yet started algo,for all the nodes in that row update all the neighbours
                    algorithm(lambda: D(win, grid,rows,width),grid, start,end,ctr)

                if event.key == pygame.K_c:    #for clearing the screen and reset everything
                    start = None
                    end = None
                    ctr = 0
                    grid = make_grid(rows,width)

    pygame.quit()

main(win,width)
