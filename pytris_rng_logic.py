import random

piecenum = 0
nextpiece1 = 0 #the first piece that is waiting to come down
nextpiece2 = 0 #the second one
nextpiece3 = 0 #the third one

def pieceroll():
    global piecenum
    global nextpiece1
    global nextpiece2
    global nextpiece3
    piecenum = nextpiece1
    nextpiece1 = nextpiece2
    nextpiece2 = nextpiece3
    nextpiece3 = random.randint(0,69) % 7