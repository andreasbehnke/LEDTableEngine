from PIL import Image, ImageDraw
import time

class BaseController(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.createFrame()
        self.input = None
        self.appStack = []
        self.queuedInsertions = []

    def setInputHandler(self, input):
        self.input = input
        self.input.setController(self)

    def createFrame(self):
        self.frame = Image.new('RGB', [self.width, self.height], (0,0,0));
        self.draw = ImageDraw.Draw(self.frame)

    def clearFrame(self, clearColor=(0,0,0)):
        self.draw.rectangle([(0, 0), (self.width, self.height)],fill=clearColor)

    def getTime(self):
        return int(round(time.time() * 1000))

    def addApplication(self, application, queueInsertion=False):
        if not queueInsertion:
            if len(self.appStack) > 0:
                self.appStack[-1].pauseApp(self)
            self.appStack.insert(len(self.appStack),application)
            application.initialize()
        else:
            self.queuedInsertions.insert(len(self.queuedInsertions),application)


    def run(self, FPS=50):
        if not self.input:
            print "Input controller not set!"
            return

        FPS_ms = 1000.0/FPS
        last_time = new_time =  self.getTime()

        if not self.showFrame():
            return
        if len(self.appStack) > 0:
            self.appStack[-1].continueApp(self)

        while(len(self.appStack) > 0):

            inputs = self.input.pollKeys()

            if len(inputs) > 0:
                print "Inputs", inputs

            #print "FrameTime: {} ms".format(new_time - last_time)
            self.appStack[-1].processInput(self, inputs, new_time - last_time)

            self.appStack[-1].draw(self, self.frame, self.draw, new_time - last_time)

            self.showFrame()

            if len(self.queuedInsertions) > 0:
                for i in self.queuedInsertions:
                    if len(self.appStack) > 0:
                        self.appStack[-1].pauseApp(self)
                    self.appStack.insert(len(self.appStack),i)
                    i.initialize()
                self.queuedInsertions = ()

            if self.appStack[-1].hasFinished():
                self.appStack.pop()
                if len(self.appStack) > 0:
                    self.appStack[-1].continueApp(self)

            new_time = self.getTime()

            if(new_time - last_time < FPS_ms):
                #print "Sleep time: {} ms".format( FPS_ms - (new_time - last_time))
                time.sleep((FPS_ms - (new_time - last_time))/1000.0)
                new_time = self.getTime()

            last_time = new_time

        self.onExit()

    def onExit(self):
        raise NotImplementedError("Please Implement this method")

    def showFrame(self):
        raise NotImplementedError("Please Implement this method")

class Application(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pause = False
        self.finished = False

    # This function is called once, after the application has been added
    # to the application stack.
    def initialize(self):
        raise NotImplementedError("Please Implement this method")

    # This function is called for each frame, before "draw" is called
    # controller: Reference to the controller object to get time e.g.
    # key_list: List of keys that are currently pressed (see BaseInput)
    # delta_time: Time that has passed since the last call
    def processInput(self, controller, key_list, delta_time):
        raise NotImplementedError("Please Implement this method")

    # This function is called for each frame, after "processInput" is called
    # controller: Reference to the controller object to clear the frame buffer
    # frame: Reference to the frame buffer (Pillow Image)
    # draw: Reference to the draw object, that is used to draw the image (ImageDraw)
    # delta_time: Time that has passed since the last call
    def draw(self, controller, frame, draw, delta_time):
        raise NotImplementedError("Please Implement this method")

    # Returns true if the application has finished processing.
    # Afterwards the application is removed from the stack
    def hasFinished(self):
        return self.finished

    # Is called if the app now running and the previous application has been stopped
    def continueApp(self, controller):
        self.pause = False

    # This is called if the app has launched a new app and the current app is now longer
    # the active one
    def pauseApp(self, controller):
        self.pause = True

class BaseInput(object):
    def __init__(self):
        self.supportedKeys = ["up", "left", "right", "down", "enter"]

    def setController(self, controller):
        self.controller = controller

    def pollKeys():
        raise NotImplementedError("Please Implement this method")

class KeyEvents(object):
    def __init__(self, name, state=""):
        self.name = name
        self.state = state

    def __repr__(self):
        return self.name