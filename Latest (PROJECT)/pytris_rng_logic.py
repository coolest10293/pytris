import random

piecenum = 0
nextpiece1 = 0 #the first piece that is waiting to come down
nextpiece2 = 0 #the second one
nextpiece3 = 0 #the third one
avail_pieces = [0,1,2,3,4,5,6]

def pieceroll():
    global piecenum, nextpiece1, nextpiece2, nextpiece3, avail_pieces
    piecenum = nextpiece1
    nextpiece1 = nextpiece2
    nextpiece2 = nextpiece3
    nextpiece3 = random.randint(0,69) % 7
    try:
        avail_pieces[0]
    except:
        pass
    else:
        while nextpiece3 not in avail_pieces:
            nextpiece3 = random.randint(0,69) % 7
        avail_pieces.remove(nextpiece3)
        print(avail_pieces)
