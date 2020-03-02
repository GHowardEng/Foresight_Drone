import serial
import time

# Function to reverse bits of positive  
# integer number


chan = 0
data = 1600
phase = 1

# may need to use latin-1 string encoding

# look into using bytearray

ser = serial.Serial(
"/dev/ttyS0",
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS 
)
ser.baudrate = 115200

UPPER = 0xFF00
LOWER = 0x00FF

def makeWord(phase, chan, data):
    PHASE = 15
    CHANNEL = 11
    
    word = (phase << PHASE) | (chan << CHANNEL) | (data)
    #upper = (word & UPPER) >> 8
    #lower = (word & LOWER)
    #ser.write(chr(upper))
    #ser.write(chr(lower))
    #print(bin(word))
    #txDat = (reverseBits(word,16))
    #print(bin(txDat))
    #upper = chr((txDat & UPPER) >> 8)
    #lower = chr((txDat & LOWER))
    return word
    
def reverseBits(num,bitSize): 
  
     # convert number into binary representation 
     # output will be like bin(10) = '0b10101' 
     binary = bin(num) 
  
     # skip first two characters of binary 
     # representation string and reverse 
     # remaining string and then append zeros 
     # after it. binary[-1:1:-1]  --> start 
     # from last character and reverse it until 
     # second last character from left 
     reverse = binary[-1:1:-1] 
     reverse = reverse + (bitSize - len(reverse))*'0'
  
     # converts reversed binary string into integer 
     #print int(reverse,2)
     return int(reverse,2)
    

try:
    #Channel (Servo) data
    data = 1500;

    while(1):
        #print(bin(makeWord(1,5,1000)))
        #print(bin(makeWord(0,11,1800)))
        

        
        # Generate first 16-Byte packet:
        # Ch0 is throttle
        # Ch1 is aileron (roll)
        # Ch2 is elevator (pitch)
        # Ch3 is rudder (yaw)
        # Ch4 is aux1
        # Ch5 is aux2
        # Ch6 is aux3
        
        #Header bytes:
        # First byte is fades(?)
        # Second byte is protocol type - 0xB2 for Spektrum 2048 in our case
        
        dataString = "" + chr(5) + chr(178)
        for i in range(7):
            if (i == 4):
                dataWord = makeWord(0,i,2000)
            else:
                dataWord = makeWord(0,i,data)
            upper = chr((dataWord & UPPER) >> 8)
            lower = chr((dataWord & LOWER))
            dataString = dataString + upper + lower
            
        # Send 16 bytes over serial bus to flight controller
        ser.write(dataString)
        time.sleep(0.008)
        
        # Generate second 16-Byte packet - we chose to retransmitt the same data as first packet
        # But the phase bit of the first channel word is set to 1 to indicate the second packet
        #but the 
        
        #Header bytes
        dataString = "" + chr(5) + chr(178)
        
        data = data + 1
        for i in range(7):
            if(i == 0):
                phase = 1
            else:
                phase = 0
            if(i == 4):
                dataWord = makeWord(phase,i,2000)
            else:
                dataWord = makeWord(phase,i,data)
            upper = chr((dataWord & UPPER) >> 8)
            lower = chr((dataWord & LOWER))
            dataString = dataString + upper + lower
            
        ser.write(dataString)
        time.sleep(0.008)
        
        # Incr
        data = data + 1
        if(data > 2000):
            data = 0
    
except Exception as e:
    print(e)
    
finally:
    ser.close()

    

