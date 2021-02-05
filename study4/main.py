from tetris import *
from random import *

def LED_init():
    thread=threading.Thread(target=LMD.main, args=())
    thread.setDaemon(True)
    thread.start()
    return

def rotate(m_array, rot_num):
        N = len(m_array)
        rot_m = [[0] * N for _ in range(N)]

        if rot_num % 4 == 1:
            for i in range(N):
                for j in range(N):
                    rot_m[j][N-1-i] = m_array[i][j]
        elif rot_num % 4 == 2:
            for i in range(N):
                for j in range(N):
                    rot_m[N-1-i][N-1-j] = m_array[i][j]
        elif rot_num % 4 == 3:
            for i in range(N):
                for j in range(N):
                    rot_m[N-1-j][i] = m_array[i][j]
        else:
            for i in range(N):
                for j in range(N):
                    rot_m[i][j] = m_array[i][j]

        return rot_m

def initSetOfBlockArrays():
    arrayBlks = [  [ [ 0, 0, 1, 0 ],     # ㅁ
                    [ 0, 0, 1, 0 ],     # ㅁ
                    [ 0, 0, 1, 0 ],     # ㅁ
                    [ 0, 0, 1, 0 ] ],   # ㅁ
                  [ [0, 1, 0],              
                    [1, 1, 1],          # ㅗ
                    [0, 0, 0] ],
                  [ [1, 0, 0],
                    [1, 1, 1],          # ㄴ
                    [0, 0, 0] ],
                  [ [0, 0, 1],          #    ㅁ
                    [1, 1, 1],          # ㅁㅁㅁ 
                    [0, 0, 0] ],        #
                  [ [1, 1],             # ㅁ
                    [1, 1] ],           
                  [ [0, 1, 1],          #   ㅁㅁ
                    [1, 1, 0],          # ㅁㅁ 
                    [0, 0, 0] ],        #
                  [ [1, 1, 0],          # ㅁㅁ
                    [0, 1, 1],          #   ㅁㅁ
                    [0, 0, 0] ]         #
                ]

    nBlocks = len(arrayBlks)
    setOfBlockArrays = [[0] * 4 for _ in range(nBlocks)]

    for idxBlockType in range(nBlocks):
        for idxBlockDegree in range(4):
            rotate_matrix = rotate(arrayBlks[idxBlockType], idxBlockDegree)
            setOfBlockArrays[idxBlockType][idxBlockDegree] = rotate_matrix

    return setOfBlockArrays

class OnLeft():
    def run(t, key):
        t.left = t.left - 1
        return t.anyConflict()

class OnRight():
    def run(t, key):
        t.left = t.left + 1
        return t.anyConflict()

class OnDown():
    def run(t, key):
        t.top = t.top + 1
        return t.anyConflict()

class OnUp():
    def run(t, key):
        t.top = t.top - 1
        return t.anyConflict()

class OnDrop():
    def run(t, key):
        while(t.anyConflict() == false):
            t.top = t.top + 1
        return t.anyConflict()

class OnCw():
    def run(t, key):
        t.idxBlockDegree = (t.idxBlockDegree + 1) % t.nBlockDegrees
        t.currBlk = t.setOfBlockObjects[t.idxBlockType][t.idxBlockDegree]
        return t.anyConflict()

class OnCcw():
    def run(t, key):
        t.idxBlockDegree = (t.idxBlockDegree + t.nBlockDegrees - 1) % t.nBlockDegrees
        t.currBlk = t.setOfBlockObjects[t.idxBlockType][t.idxBlockDegree]
        return t.anyConflict()

class OnNewBlock():
    def run(t, key):
        t.oScreen = deleteFullLines(t.oScreen, t.currBlk, t.top, t.iScreenDy, t.iScreenDx, t.iScreenDw)
        t.iScreen = Matrix(oScreen)
        t.idxBlockType = int(key)
        t.idxBlockDegree = 0
        t.currBlk = t.setOfBlockObjects[t.idxBlockType][t.idxBlockDegree]
        t.top = 0
        t.left = t.iScreenDw + t.iScreenDx / 2 - (t.currBlk.get_dx() + 1) / 2
        return t.anyConflict()

    def deleteFullLines(screen, blk, top, dy, dx, dw):
        if(blk == None):
            return screen
        cy, y, nDeleted = 0, 0, 0
        nScanned = blk.get_dy()
        if(top + blk.get_dy() - 1 >= dy):
            nScanned -= (top + blk.get_dy() - dy)
        zero = Matrix(1, dx = 2*dw)
        for y in range(nScanned - 1, -1, -1):
            cy = top + y + nDeleted
            line = screen.clip(cy, 0, cy + 1, screen.get_dx())
            if(line.sum() == screen.get_dx()):
                temp = screen.clip(0, 0, cy, screen.get_dx())
                screen.paste(temp, 1, 0)
                screen.paste(zero, 0, dw)
                nDeleted += 1
        return screen

class OnFinished():
    def run(t, key):
        print("OnFinished.run() called")
        return False

myOnLeft = OnLeft()
myOnRight = OnRight()
myOnDown = OnDown()
myOnUp = OnUp()
myOnDrop = OnDrop()
myOnCw = OnCw()
myOnCcw = OnCcw()
myOnNewBlock = OnNewBlock()
myOnFinished = OnFinished()

Tetris.setOperation('a', TetrisState.Running, myOnLeft, TetrisState.Running, myOnRight, TetrisState.Running)
Tetris.setOperation('d', TetrisState.Running, myOnRight, TetrisState.Running, myOnLeft, TetrisState.Running)
Tetris.setOperation('s', TetrisState.Running, myOnDown, TetrisState.Running, myOnUp, TetrisState.NewBlock)
Tetris.setOperation('w', TetrisState.Running, myOnCw, TetrisState.Running, myOnCcw, TetrisState.Running)
Tetris.setOperation(' ', TetrisState.Running, myOnDrop, TetrisState.Running, myOnUp, TetrisState.NewBlock)
Tetris.setOperation('0', TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation('1', TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation('2', TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation('3', TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation('4', TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation('5', TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation('6', TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished) 
    
if __name__ == "__main__":
    setOfBlockArrays = initSetOfBlockArrays()
    Tetris.init(setOfBlockArrays)

    board = Tetris(15, 10)
    idxBlockType = randint(0, 6)
    key = '0' + str(idxBlockType)
    board.accept(key)
    board.printScreen()
      
    while (1):
        key = input('Enter a key from [ q (quit), a (left), d (right), s (down), w (rotate), \' \' (drop) ] : ')
        
        if key != 'q':
          state = board.accept(key)
          board.printScreen()
          
          if(state == TetrisState.NewBlock):
              idxBlockType = randint(0, 6)
              key = '0' + str(idxBlockType)
              state = board.accept(key)
              board.printScreen()
              if(state == TetrisState.Finished):
                  break
    
    print('Program terminated...')

### end of pytet.py
