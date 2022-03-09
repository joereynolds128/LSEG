import re
import sys

#LSEG LightShow Coding Challenge - Part 1

class Light(object):
    def __init__(self,xCoord,yCoord):
        self.brightness = 0
        self.xCoord = xCoord
        self.yCoord = yCoord
    def on(self):
        self.brightness = 1
    def off(self):
        self.brightness = 0
    def toggle(self):
        self.brightness = 1 - self.brightness
    def getbrightness(self):
        return(self.brightness)


        
def validateInputs(linenum,splitline,xMax,yMax):
                
        if not len(splitline) == 4:
            sys.exit('Error - Wrong number of arguements in input file line:' + str(linenum+1) )
                            
        
        if not ((splitline[0] == 'on') or (splitline[0] == 'off') or (splitline[0] == 'toggle')or (splitline[2] == 'through')):
            sys.exit('Error on line:' + str(linenum+1))

                
        #Check coordinates are in correct format
        for TestInput in [splitline[1],splitline[3]]:
            if not re.match("\d+,\d+", TestInput):
                sys.exit('Cordinate error on line:' + str(linenum+1)) 
                
        #get the first and second coordinates for both x and y
        
        xStart=int(splitline[1].split(",")[0])
        xStop=int(splitline[3].split(",")[0])
        yStart=int(splitline[1].split(",")[1])
        yStop=int(splitline[3].split(",")[1])
    
        
        if (xStart >= xStop) or (yStart >= yStop) or (xStop > xMax-1) or (yStop > yMax-1):
            sys.exit('Cordinate error on line:' + str(linenum+1))         
    
        return xStart,xStop,yStart,yStop


def instantiateLights(xMax,yMax):
    
    Display=[]
    for x in range(xMax):
        for y in range(yMax):
            Display.append(Light(x,y))
    return Display


def sumBrightness(Display):
    #Get brightness
    
    brightnesstotal = 0
    
    for light in Display:
        brightnesstotal += light.getbrightness()
                    
    return(brightnesstotal)


def runFile(inputFilePath,xMax,yMax,Display):
    try:
        with open(inputFilePath) as f:
            for linenum, line in enumerate(f):
                
                splitline = line.split(" ")
                
                #remove first value if length = 5 e.g turn on = on, toggle remains the same
                #first value used to call Light methods,on, off, toggle 
                
                if len(splitline) == 5:
                    splitline.pop(0)
                
                #Validate Inputs and get affected coords
                xStart,xStop,yStart,yStop  = validateInputs(linenum,splitline,xMax,yMax)
                
                #Perform Line action
                for light in Display:
                    
                    if (xStart <= light.xCoord <= xStop) and (yStart <= light.yCoord <= yStop): 
                        getattr(light, splitline[0])() #Call method based on first value in line: on, off, toggle
    except IOError:
        sys.exit("Could not read file:"+ inputFilePath ) 


def main(inputFilePath,xMax,yMax):    

    #instantiate all lights
    
    Display= instantiateLights(xMax,yMax)
        
    #Read file and perform line actions
    
    runFile(inputFilePath,xMax,yMax,Display)
                 
    #Get brightness & print
        
    TotalBrightness = sumBrightness(Display)
                    
    print('Brightness:' + str(TotalBrightness))
    
    return (TotalBrightness)

if __name__ == "__main__":
    
    inputFilePath= r'D:\LSE\coding_challenge_input.txt'  
    xMax = 1000
    yMax = 1000
    
    main(inputFilePath,xMax,yMax)

'''Unit Tests'''
'''


class Tests(object):
    def testMain(self,ScenarioResult):
        #Test the whole program using provided scenario
        assert main(r'D:\LSE\Test_Scenario.txt',1000,1000) == ScenarioResult
        print('Pass')
    
    def testValidateInputs(self):
          
        TestStrings= []  
        
        #wrong number of arguements
        TestStrings.append("Wrong num of args test",)
        #wrong 'action' i.e. not 'turn on' 'turn off' 'toggle'    
        TestStrings.append("turn aaa 499,499 through 500,500")
        #wrong 'action' i.e. not 'turn on' 'turn off' 'toggle    
        TestStrings.append("turn aaa 499,499 through 500,500")
        #'through' not correct  
        TestStrings.append("turn off 499,499 aaa 500,500")
        #Coord wrong format
        TestStrings.append("turn off 12,34,56 through 12,34,56")
        #Coord not a number
        TestStrings.append("turn off aaa,499 through 500,500")
        #Coord negative      
        TestStrings.append("turn off -123,499 through 500,500")
        #Coord OOR
        TestStrings.append("turn off 1000,499 through 500,500")          
        #Coord Start>Stop
        TestStrings.append("turn off 1000,499 through 500,500")
        
        for TestString in TestStrings:
            try:
                validateInputs(1,TestString,1000,1000)
            except SystemExit:
                pass
            except Exception:
                self.fail('unexpected exception raised')
            else:
                self.fail('expected exception not raised')    
        print('Pass')
        
        

Test = Tests()

Test.testMain(998004) #Result From Coding challenge.pdf
Test.testValidateInputs()
'''