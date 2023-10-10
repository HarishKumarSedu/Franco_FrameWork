
import json

class pathFindLogic:

    def __init__(self,pathData) -> None:
        self.pathData = pathData



    def path(self,pathBegin,pathBnd):
        path = []
        while True:
          path.append(pathBegin)  
        pass


if __name__ == '__main__':

    try :
        with open('SignalPath.json') as f:
            pathData = json.load(f)
        findPath = pathFindLogic(pathData=pathData)

        findPath.path(pathBegin='X1',pathBnd='C2')

    except KeyboardInterrupt:
        pass
            
