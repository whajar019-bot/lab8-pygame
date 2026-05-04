Exercise 7
I used a list to store the square's old positions to draw the trail. A giant line would blink across the screen whenever a square wrapped around the edge.  This happened beacause the code tried to draw a line connecting the left side of the screen to the right side. So I cleared the list of positions inside the wrap() function so the trail starts over when hitting a wall.

Exercise 8
I need to prove the square moves at the right speed using a test mode. The plan is to Use a global TEST_MODE_ON variable to isolate one square. And to test I Set a square to 100 pixels per second. If it moves 100 pixels after 1 second of game time, the math is right