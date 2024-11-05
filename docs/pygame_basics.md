### Use case of pygame

For our current needs we need a tile system. The following is a [proof of concept](/simulation/example_tiles.py) on how to implement one.

![alt text](images/image.png)

In this case, the red block represents the mower and it can be controlled using the arrow keys or a,w,s,d keys for the first person shooter guys.

Here you can see the trail of cut grass (bright green)

![alt text](images/image-2.png)

The program reads the lawn info from a CSV file:

![alt text](images/image-3.png)

And the possible states of a tile are given by this enum:

![alt text](images/image-4.png)