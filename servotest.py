import RPi.GPIO as GPIO  
from time import sleep




import pigpio


#GPIO.setmode(GPIO.BOARD) 

# GPIO.setup(13, GPIO.OUT) 
# GPIO.setup(12, GPIO.OUT) 
# p1 = GPIO.PWM(13, 50)   
# p2 = GPIO.PWM(12, 50)
pi = pigpio.pi()
#try:
    
while True:
    
     #먼저 사용할 pigpio.pi를 매칭해줍니다.



    pi.set_servo_pulsewidth(13, 0) #18번 채널에연결된 서보모터를 꺼줍니다. 

    sleep(1) 

    pi.set_servo_pulsewidth(13, 600) #18번채널에 연결된 서보모터를 0도로 이동

    sleep(1)

    pi.set_servo_pulsewidth(13, 1500) # 가운데로 이동 90도

    sleep(1)

    pi.set_servo_pulsewidth(13, 2400) # 180도 끝으로 이동. 

    sleep(1)
        
#         p1.start(2)            
#         p2.start(8)            
#         
#         p1.ChangeDutyCycle(2) 
#         p2.ChangeDutyCycle(8) 
#         sleep(1)
#         p1.ChangeDutyCycle(8)
#         p2.ChangeDutyCycle(2)
#         sleep(1)
# finally:
#     GPIO.cleanup()

# import RPi.GPIO as GPIO
# import time
# 
# 
# #Set function to calculate percent from angle
# def angle_to_percent (angle) :
#     if angle > 180 or angle < 0 :
#         return False
# 
#     start = 2
#     end = 12
#     ratio = (end - start)/180 #Calcul ratio from angle to percent
# 
#     angle_as_percent = angle * ratio
# 
#     return start + angle_as_percent
# 
# 
# GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
# GPIO.setwarnings(False) #Disable warnings
# 
# #Use pin 12 for PWM signal
# pwm_gpio = 13
# frequence = 50
# GPIO.setup(pwm_gpio, GPIO.OUT)
# pwm = GPIO.PWM(pwm_gpio, frequence)
# 
# while True:
#     #Init at 0°
#     pwm.start(angle_to_percent(0))
#     time.sleep(1)
# 
# #Go at 90°
#     pwm.ChangeDutyCycle(angle_to_percent(90))
#     time.sleep(1)
#     if 
# 
# 
# #Close GPIO & cleanup
# pwm.stop()
# GPIO.cleanup()