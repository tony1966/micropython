#myapp.py
from machine import Pin,PWM

def main():
    #application codes are placed here  
    pwm2=PWM(Pin(2), freq=1, duty=512)

if __name__ == "__main__":  
    main()  