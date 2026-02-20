from airtest.core.api import *
from start_parts import *


def cycle_click(attack_type):
        t = 0
        while 1:            
            if attack_type == 0:
                click((0.5,0.65))
            elif attack_type == 1:
                click((0.5,0.65))
                t += 1
                if t >= 100:
                    t = 0
                    sleep(1)
                    click((0.5,0.95))
                    sleep(0.5)
                    click((0.5,0.95))      
            elif attack_type == 2:
                click((624,810))
            else:            
                click((624,810))    
                t += 1
                if t >= 100:
                    t = 0
                    sleep(1)
                    click((0.5,0.95))
                    sleep(0.5)
                    click((0.5,0.95))                    
            sleep(0.15)

