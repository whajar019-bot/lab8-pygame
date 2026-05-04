Exercise 7
I used a list to store the square's old positions to draw the trail.  
A giant line would blink across the screen whenever a square wrapped around the edge.  
This hapopend beacause the code tried to draw a line connecting the left side of the screen to the right side. So I cleared the list of positions inside the wrap() function so the trail starts over when hitting a wall.