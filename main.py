

from engine.desktop import DesktopController, DesktopInput

from applications.testpattern import TestPattern
from applications.snake import Snake
from applications.bubbleshooter import BubbleShooter
from applications.menu import Menu

DISPLAY_WIDTH = 20
DISPLAY_HEIGHT = 15

if __name__ == '__main__':

    r = DesktopController(DISPLAY_WIDTH,DISPLAY_HEIGHT, upscale=30)
    test = TestPattern(DISPLAY_WIDTH,DISPLAY_HEIGHT, mode=0)
    snake = Snake(DISPLAY_WIDTH,DISPLAY_HEIGHT)
    shoot = BubbleShooter(DISPLAY_WIDTH,DISPLAY_HEIGHT)

    menu2 = Menu(DISPLAY_WIDTH,DISPLAY_HEIGHT,isClosable=True)
    menu2.setMenuItemsAndApps(
        [("Entry1",0)])

    menu = Menu(DISPLAY_WIDTH,DISPLAY_HEIGHT,isClosable=True)
    menu.setMenuItemsAndApps(
        [("Test Pattern",test),
         ("Snake",snake),
         ("Bubbleshooter", shoot),
         ("Submenu",menu2)])

    input = DesktopInput(debouncedInput = True)
    r.setInputHandler(input)
    r.addApplication(menu)

    r.run(FPS=40)
