from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD 

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
### end of class TetrisState():

class Colors():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        Tetris.iScreenDw = arrayBlk_maxSize     # larget enough to cover the largest block

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j])
        return
		
    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen
		
    def __init__(self, iScreenDy, iScreenDx):
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        return

    def printScreen(self):
#        self.oScreen.print()
        array = self.oScreen.get_array()

        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                if array[y][x] == 0:
                    print("□", end='')
                    #LMD.set_pixel(y, 19-x, 0)
                elif array[y][x] == 1:
                    print(Colors.BLACK + "■" + Colors.RESET, end='')
                    #LMD.set_pixel(y, 19-x, 4)
                elif array[y][x] == 2:
                    print(Colors.CYAN + "■" + Colors.RESET, end='')
                elif array[y][x] == 3:
                    print(Colors.MAGENTA + "■" + Colors.RESET, end='')
                elif array[y][x] == 4:
                    print(Colors.BLUE + "■" + Colors.RESET, end='')
                elif array[y][x] == 5:
                    print(Colors.WHITE + "■" + Colors.RESET, end='')
                elif array[y][x] == 6:
                    print(Colors.YELLOW + "■" + Colors.RESET, end='')
                elif array[y][x] == 7:
                    print(Colors.GREEN + "■" + Colors.RESET, end='')
                elif array[y][x] == 8:
                    print(Colors.RED + "■" + Colors.RESET, end='')
                else:
                    print("XX", end='')
                    #continue
            print()

    def deleteFullLines(self): # To be implemented!!
        nScreen = self.oScreen.get_array()
        nline = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        y = 31
        while y > -1:
            line = nScreen[y]
            delete = True
            for x in range(4, 20):
                if line[x] == 0:
                    delete = False
                    break
            if delete == True:
                del nScreen[y]
                nScreen.insert(0, nline)
            elif delete == False:
                y -= 1

        self.oScreen = Matrix(nScreen)
        return self.oScreen

    def accept(self, key): # To be implemented!!
        if key in ['00', '01', '02', '03', '04', '05', '06']:
            print()
            self.state = TetrisState.NewBlock
            self.idxBlockType = int(key)
            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
            self.idxBlockType = (1 + self.idxBlockType) % Tetris.nBlockTypes
            self.idxBlockDegree = 0

            tmp_currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            tmp_tempBlk = self.iScreen.clip(self.top, self.left, self.top + tmp_currBlk.get_dy(), self.left + tmp_currBlk.get_dx())

            test1 = tmp_currBlk.get_array()
            test2 = tmp_tempBlk.get_array()
            length = len(test1)

            for y in range(length):
                for x in range(length):
                    if (test1[y][x] != 0) and (test2[y][x] != 0):
                        self.state = TetrisState.Finished
                        self.oScreen = Matrix(self.iScreen)
                        return self.state

        self.state = TetrisState.Running
        
        if key == 'a':
            self.left -= 1
        elif key == 'd':
            self.left += 1
        elif key == 's':
            self.top += 1
        elif key == 'w':
            self.idxBlockDegree = (self.idxBlockDegree + 1) % Tetris.nBlockDegrees
        elif key == ' ':
            crash = False
            while crash == False:
                self.top += 1
                self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())

                test1 = self.tempBlk.get_array()
                test2 = self.currBlk.get_array()
                length = len(test1)

                for y in range(length):
                    for x in range(length):
                        if (test1[y][x] != 0) and (test2[y][x] != 0):
                            crash = True
                            self.top -= 1
                            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
                            self.tempBlk = self.tempBlk + self.currBlk
                            self.state = TetrisState.NewBlock
                            break
                    if crash == True:
                        break
        elif key in ['00', '01', '02', '03', '04', '05', '06']:
            pass
        else:
            print("Wrong key!")

        self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())

        test1 = self.tempBlk.get_array()
        test2 = self.currBlk.get_array()
        length = len(test1)

        crash = False
        for y in range(length):
            for x in range(length):
                if (test1[y][x] != 0) and (test2[y][x] != 0):
                    crash = True
                    break
            if crash == True:
               break

        if crash == True:
            if key == 'a':
                self.left += 1
            elif key == 'd':
                self.left -= 1
            elif key == 's':
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'w':
                self.idxBlockDegree = (self.idxBlockDegree - 1) % Tetris.nBlockDegrees
            elif key == ' ':
                print("wrong!")
            
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())

        self.tempBlk = self.tempBlk + self.currBlk

        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)

        if self.state == TetrisState.NewBlock:
            self.oScreen = self.deleteFullLines()
            self.iScreen = Matrix(self.oScreen)
            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
            self.idxBlockDegree = 0

        return self.state

### end of class Tetris():
    
