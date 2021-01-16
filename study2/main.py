from tetris import *
from random import *
import threading

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
    arrayBlks = [  [ [ 0, 0, 2, 0 ],     # ㅁ
                    [ 0, 0, 2, 0 ],     # ㅁ
                    [ 0, 0, 2, 0 ],     # ㅁ
                    [ 0, 0, 2, 0 ] ],   # ㅁ
                  [ [0, 3, 0],              
                    [3, 3, 3],          # ㅗ
                    [0, 0, 0] ],
                  [ [4, 0, 0],
                    [4, 4, 4],          # ㄴ
                    [0, 0, 0] ],
                  [ [0, 0, 5],          #    ㅁ
                    [5, 5, 5],          # ㅁㅁㅁ 
                    [0, 0, 0] ],        #
                  [ [6, 6],             # ㅁ
                    [6, 6] ],           
                  [ [0, 7, 7],          #   ㅁㅁ
                    [7, 7, 0],          # ㅁㅁ 
                    [0, 0, 0] ],        #
                  [ [8, 8, 0],          # ㅁㅁ
                    [0, 8, 8],          #   ㅁㅁ
                    [0, 0, 0] ]         #
                ]

    nBlocks = len(arrayBlks)
    setOfBlockArrays = [[0] * 4 for _ in range(nBlocks)]

    for idxBlockType in range(nBlocks):
        for idxBlockDegree in range(4):
            rotate_matrix = rotate(arrayBlks[idxBlockType], idxBlockDegree)
            setOfBlockArrays[idxBlockType][idxBlockDegree] = rotate_matrix

    return setOfBlockArrays
    
if __name__ == "__main__":
    #LED_init()
    setOfBlockArrays = initSetOfBlockArrays()

    Tetris.init(setOfBlockArrays)
    board = Tetris(32, 16)

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
              if(state == TetrisState.Finished):
                  board.printScreen()
                  print('Game Over!!!')
                  break
              board.printScreen()
        else:
          print('Game aborted...')
          break
    
    print('Program terminated...')

### end of pytet.py
