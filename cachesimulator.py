# File: cachesimulator.py
# Author(s): Trey Wells
# Date: 11/28/2021
# Section: 505
# E-mail(s): wells.t.2024@tamu.edu
# Description:
#   This file contains the main function for the cache simulator


from functions import *
from copy import deepcopy

def main():
    ##
    # Driver function for the cache simulator
    
    # Print welcome message
    print('*** Welcome to the cache simulator ***')
    
    # Initalize the RAM
    RAM = initializeRAM(getCommandLineArgs())
    
    # Initalize the Cache
    cache = initalizeCache()
    
    # Print the menu and receive the first command
    printMenu()
    command = input()
    
    # Continue to execute commands and get the next command while command != 8
    while command != 'quit':
        if 'cache-read' in command:
            # Extract the address from the user input
            address = command[command.find('x')+1:]
            cacheRead(cache, RAM, address)
            
        elif 'cache-write' in command:
            # Extract the hexidecimals from the user input
            hexs = command[command.find(' ')+1:]
            
            # Extract the address from the hexidecimals
            address = hexs[hexs.find('x')+1:hexs.find(' ')]
            hexs = hexs[hexs.find(' ')+1:]
            
            # Extract the data byte from the hexs
            byte = hexs[hexs.find('x')+1:]
            
            # Pass in the address and byte in hex without the '0x'
            cacheWrite(cache, RAM, address, byte)
        
        elif command == 'cache-flush':
            cache = cacheFlush(cache)
        elif command == 'cache-view':
            viewCache(cache)
        elif command == 'memory-view':
            viewMemory(RAM)
        elif command == 'cache-dump':
            cacheDump(cache)
        elif command == 'memory-dump':
            memoryDump(RAM)
        else:
            print("Please enter a valid command")
            
        printMenu()
        command = input()
      
if __name__ == "__main__":
    main()
    