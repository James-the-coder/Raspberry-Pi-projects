from sense_hat import SenseHat
import time

import pygame

#assigning variables
sense = SenseHat()
sense.clear()
pressure = sense.get_pressure()
pressure = int(pressure)
humid = sense.get_humidity()
humid = int(humid)
temp = sense.get_temperature()
temp = int(temp)





width = 500
length = 500
fps = 60
count = 0

x = width / 2
y = length / 2

green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 255, 255)
yellow = (255, 255, 0)
font_name = pygame.font.match_font('arial')

pygame.init()
screen = pygame.display.set_mode((width, length))
pygame.display.set_caption("Weather Station")
clock = pygame.time.Clock()

# draw_text is a function that puts text onto the screen


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



'''getting the information and displaying it on the screen and then appending the data to a file'''
try:
    while True:

        

        clock.tick(fps)
        
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # getting temperature readings    
        new_temp = float(sense.get_temperature())
        new_temp = float("{0:.1f}".format(new_temp))
        
        
        
        # modify humidy reading from sensor to approx. calibrate to real value
        new_humid = int((sense.get_humidity()-15.4)/1.889)
        
        
        
        # getting pressure readings
        new_pressure = int(sense.get_pressure())
        
        

        screen.fill(blue)
        draw_text(screen, "The temperature is           degrees celsius", 25, x, y)
        draw_text(screen, str(new_temp), 25, x + 15, y)

        draw_text(screen, "The humidity is         %", 25, x, y + 30)
        draw_text(screen, str(new_humid), 25, x + 70, y + 30)

        draw_text(screen, "The pressure is            millibars", 25, x, y - 30)
        draw_text(screen, str(new_pressure), 25, x + 40, y - 30)
        pygame.display.flip()

        
        time.sleep(1)
        
        
   

        data = new_pressure, new_humid, new_temp
        #saveFile is the variable used to store my data
        saveFile = open("/home/pi/Documents/Sense hat/Weather data/Data.txt", "a")
        saveFile.write("\n")
        saveFile.write(str(data))
        saveFile.close()
        
except KeyboardInterrupt:
    sense.clear()
    pygame.quit()
    quit()


