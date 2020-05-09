
def old_setup():
    # First Motor Output
    GPIO.setup(3, GPIO.OUT)# Forward Trigger
    GPIO.setup(5, GPIO.OUT)# Reverse Trigger
    GPIO.setup(7, GPIO.OUT)# Enable/PWM
    
    
    # Second Motor Output
    GPIO.setup(11, GPIO.OUT) # Forward Trigger
    GPIO.setup(13, GPIO.OUT) # Reverse Trigger
    GPIO.setup(15, GPIO.OUT) # Enable/ PWM Generator

