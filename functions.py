# File: cachesimulator.py
# Author(s): Trey Wells
# Date: 11/28/2021
# Section: 505
# E-mail(s): wells.t.2024@tamu.edu
# Description:
#   This file contains the helping functions for the cache simulator

import sys
from copy import deepcopy
from math import log2
from random import randint

def getCommandLineArgs():
    ##
    # Gets the command line argument that is the input text file
    # @param None
    # @returns filename of the input text file
    
    
    # returns the first commandline arg that ends with ".txt"
    arguments = sys.argv
    for arg in arguments:
        # If argument is not .txt file, get next argument
        if arg[-4:] != ".txt":
            continue
        else:
            return arg

def initializeRAM(filename):
    ##
    # The 2d list will hold 8 byte blocks as the elements.
    # The index of the list is the RAM address in decimal divided 8
    # @param filename 
    # @returns A fully initalized RAM represented as a 2d array
        
    # Print the starting message
    print('initialize the RAM:')
    
    # Take in the inputs for the RAM size
    sizeConstraints = str(input('init-ram '))
    
    upperBound = sizeConstraints[-4:]
    
    # Stores how many data bytes to transferred into the ram from input.txt
    numOfBytes = int(upperBound,16) + 1
    
    # initially store the input data as a list with each byte as an element
    ifs = open(filename)
    data = ifs.read().split('\n')
    
    RAM = [['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00'],
           ['00','00','00','00','00','00','00','00']]
    
    # Stores the number of bytes transferred so far
    bytesTransferred = 0
    rowCounter = 0
    
    # Extract 8 bytes of data from the file and store in a list
    #  then add it to the RAM list and repeat until the file is exhausted
    while bytesTransferred < numOfBytes:
        # Row holds the next 8 bytes of data for the RAM
        row =  []
        
        for i in range(8):
            if bytesTransferred == numOfBytes:
                break
            
            row.append(data.pop(0))
            bytesTransferred+=1
            
        while len(row) < 8:
            row.append('00')
            
        # Add the 8 bytes to the RAM as a row
        RAM[rowCounter] = row
        
        rowCounter += 1
        
    # Print ending messages
    print('RAM successfully initialized!')
        
    return RAM

def initalizeCache():
    ##
    # Request user to input cache parameters, then configures the cold cache accordingly
    # @param None
    # @returns Configured Cache as 2d array
        
    # Print starting message
    print('configure the cache:')
    
    # Take in all the cache input parameters
    cacheSize = int(input('cache size: '))
    while cacheSize < 8 or cacheSize > 256:
        print("Error, Size of cache must be between 8 and 256")
        cacheSize = int(input('cache size: '))
    blockSize = int(input('data block size: '))
    while blockSize > cacheSize:
        print("Error, the block size cannot be bigger than the cache itself.")
        blockSize = int(input('data block size: '))
    associativity = int(input('associativity: '))
    while associativity != 1 and associativity != 2 and associativity != 4:
        print('Error, associativity must be either 1,2, or 4')
        associativity = int(input('associativity: '))
    replacementPolicy = int(input('replacement policy: '))
    while replacementPolicy < 1 or replacementPolicy > 3:
        print('Error, replacement policy must be either 1,2, or 3')
        replacementPolicy = int(input('replacement policy: '))
    hitPolicy = int(input('write hit policy: '))
    while hitPolicy < 1 or hitPolicy > 2:
        print('Error, write hit policy must be either 1 or 2')
        hitPolicy = int(input('write hit policy: '))
    missPolicy = int(input('write miss policy: '))
    while missPolicy < 1 or missPolicy > 2:
        print('Error, write miss policy must be either 1 or 2')
        missPolicy = int(input('write miss policy: '))
    
    # Create empty templates to create the cache with
    emptyBlock = '00'
    
    # Each line has a list of blocks
    emptyLine = {'valid bit': 0,
                 'dirty bit': 0,
                 'tag' : '00',
                 'data' : [],
                 'frequency' : 0,
                 'last used' : 0,
                 'addressUsed' : '00'}  # 'addressUsed' was the address call that brought that block into the cache
    
    # Each set is a list of lines
    cacheSet = []
    
    # Each cache is a list of sets
    cache = []
    
    # Create the cold cache
    for i in range(blockSize):
        emptyLine['data'].append(deepcopy(emptyBlock))
        
    for i in range(associativity):
        cacheSet.append(deepcopy(emptyLine))
        
    for i in range(int(cacheSize / blockSize / associativity)):
        cache.append(deepcopy(cacheSet))
        
    replacementPolicies = ['random_replacement','least_recently_used','least_frequently_used']
    hitPolicies = ['write_through','write_back']
    missPolicies = ['write_allocate','no_write_allocate']
        
    cacheInfo = {'cache size' : cacheSize,
                'block size' : blockSize,
                'associativity' : associativity,
                'replacement policy' : [replacementPolicy, replacementPolicies[replacementPolicy-1]],
                'write hit policy' : [hitPolicy, hitPolicies[hitPolicy-1]],
                'write miss policy' : [missPolicy, missPolicies[missPolicy-1]],
                'hits' : 0,
                'misses' : 0}
    
    cache.append(deepcopy(cacheInfo))
        
    # Print Ending Message
    print('cache successfully configured!')
    
    return cache

def printMenu():
    ##
    # Prints the menu options to the console
    # @param None
    # @returns Prints out the selection menu. Nothing physically returned
        
    # Print welcome message
    print('*** Cache simulator menu ***')
    print('type one command:\n1. cache-read\n2. cache-write\n3. cache-flush\n4. cache-view')
    print('5. memory-view\n6. cache-dump\n7. memory-dump\n8. quit')
    print('****************************')
    
def cacheRead(cache, RAM, hexAddress):
    ##
    # Attempt to read data from cache.
    #   If hit, return data byte\n
    # If miss, use replacement method and return the data byte
    # @param Cache 
    # @param RAM
    # @param Address - in hexidecimal
    # @returns Prints out cache read information. Nothing physically returned
            
    # Initalize return data for testing purposes
    data = '0x00'
    
    # Convert the hex address to binary
    binaryAddress = bin(int(hexAddress,16))[2:]
    
    # Extract tag, set index, and block offset        
    tag, setIndex, blockOffset = expandAddress(cache, hexAddress)
    
    # If it is a hit, return the data 
    for line in cache[int(setIndex,2)]:
        if line['tag'] == tag and line['valid bit'] == 1:
            # Increase cache hits
            cache[len(cache)-1]['hits']+=1
            
            # Increase the frequency for that line
            line['frequency']+=1
            
            # Update least recently used for the set
            updateLeastRecentlyUsed(cache,setIndex,tag)
            
            # Print out cache-read information for a hit and then break out of function
            print('set:{}'.format(int(setIndex,2)))
            print('tag:{}'.format(tag))
            print('hit:yes')
            print('eviction_line:-1')
            print('ram_address:-1')
            print('data:{}'.format('0x'+line['data'][int(blockOffset,2)]))
            return
        
    # Use replacement method since it is a miss if got this far in function
    #  This will also return the correct byte
    replacementMethod = cache[len(cache)-1]['replacement policy'][1]
    
    # Increase cache misses
    cache[len(cache)-1]['misses']+=1
    
    if replacementMethod == 'random_replacement':
        data = randomReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress)
    elif replacementMethod == 'least_recently_used':
        data = leastRecentlyUsedReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress)
    else:
        data = leastFrequentlyUsedReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress)
        
    # Print out cache-read information for a miss and then break out of function
    print('set:{}'.format(int(setIndex,2)))
    print('tag:{}'.format(tag))
    print('hit:no')
    print('eviction_line:{}'.format(data[1]))
    print('ram_address:{}'.format(data[2]))
    print('data:{}'.format('0x'+data[0]))
    return  

def updateLeastRecentlyUsed(cache,setIndex,tag):
    ##
    # Updates the 'last used' for the line by making it the max + 1 of the set
    # @param Cache
    # @param SetIndex - in binary
    # @param Tag - in hex
    # @returns None
        
    # The current max for "last used" for any given line in the set    
    setMax = 0
    
    # Go through each line in the set and find the max "last used"
    for line in cache[int(setIndex,2)]:
        if line['last used'] > setMax:
            setMax = line['last used']
            
    # Now make the current line's 'last used' equal to setMax+1
    for line in cache[int(setIndex,2)]:
        if line['tag'] == tag[-2:]:
            line['last used'] = setMax + 1
            return
       
def randomReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress):
    ##
    # Uses random replacement to change the cache.
    # First checks for invalid lines to replace, then uses random replacement policy
    # @param Cache
    # @param Ram
    # @param Tag - in hex
    # @param SetIndex - in binary
    # @param BlockOffset - in binary
    # @param Address - address of cache-read in binary
    # @returns Byte to be read, line evicted, ram address in hex
        
    # This is the line to randomly replace, if neccessary
    lineToReplace = randint(0, cache[len(cache)-1]['associativity']-1)
    
    # Stores the line number if that line is an invalid line
    lineCounter = 0
        
    # Change the line to replace to be the first invalid line in a set if possible
    for line in cache[int(setIndex,2)]:
        # If the line is invalid
        if line['valid bit'] == 0:
            # Make the invalid lien the one to replace and then stop searching
            lineToReplace = lineCounter  
            break
        lineCounter+=1
    
    # Index of RAM 2d array that contains correct block in decimal
    ramIndex = int(binaryAddress,2) // 8
    
    # Index of RAM 2d array in hex
    hexRamIndex = hex(int(binaryAddress,2)).upper()
    if len(hexRamIndex) == 3:
        hexRamIndex = '0x0'+hexRamIndex[-1]
    hexRamIndex = hexRamIndex[0] + 'x' + hexRamIndex[-2:]
                
    # Now use the random line for replacement even if there is an invalid line
    
    # Update valid bit
    cache[int(setIndex,2)][lineToReplace]['valid bit'] = 1
    # Update the tag
    cache[int(setIndex,2)][lineToReplace]['tag'] = tag
    # Update the data block
    
    # First Check if the dirty bit is set, then write to ram if it is
    if cache[int(setIndex,2)][lineToReplace]['dirty bit'] == 1:
        # Access the ram and replace the word
        updateRam(RAM, cache[int(setIndex,2)][lineToReplace]['data'], cache[int(setIndex,2)][lineToReplace]['addressUsed'])
    
    # Update the dirty bit
    cache[int(setIndex,2)][lineToReplace]['dirty bit'] = 0
    
    # Update the address that pulled it in
    cache[int(setIndex,2)][lineToReplace]['addressUsed'] = hexRamIndex[-2:]
    
    # Determine where to start in the ram address
    blockIndex = (int(binaryAddress,2) % 8) // cache[len(cache)-1]['block size'] * cache[len(cache)-1]['block size']
    
    data = []
    
    # Pull the correct amount of bytes from ram
    for i in range(cache[len(cache)-1]['block size']):
        data.append(deepcopy(RAM[ramIndex][blockIndex + i]))
        
    cache[int(setIndex,2)][lineToReplace]['data'] = data
    # Finally return the byte
    return cache[int(setIndex,2)][lineToReplace]['data'][int(blockOffset,2)], lineToReplace, hexRamIndex
    
def leastRecentlyUsedReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress):
    ##
    # Evicts the least recently used line in a set when a cache-read miss occurs
    # @param Cache
    # @param RAM
    # @param Tag - in hex
    # @param SetIndex - in binary
    # @param BlockOffset - in binary
    # @param Address - Address of the cache-read in binary
    # @returns Byte to be read, line evicted, ram address in hex
        
    # Stores the value for the min of the "last used" variables for all lines in a set
    setMin = cache[int(setIndex,2)][0]['last used']
    
    # Index of RAM 2d array that contains correct block in decimal
    ramIndex = int(binaryAddress,2) // 8
    
    # Index of RAM 2d array in hex
    hexRamIndex = hex(int(binaryAddress,2)).upper()
    if len(hexRamIndex) == 3:
        hexRamIndex = '0x0'+hexRamIndex[-1]
    # Decapitalize the 'X' in the hex address
    hexRamIndex = hexRamIndex[0] + 'x' + hexRamIndex[-2:]
    
    # Find the smallest "last used" in the set
    for line in cache[int(setIndex,2)]:
        if line['last used'] < setMin:
            setMin = line['last used']
            
    # Used to know which line is evicted
    lineCounter = 0
    
    # Naviage to the line which contains the min "last used"
    for line in cache[int(setIndex,2)]:
        # If last used line is found
        if line['last used'] == setMin:
            
            # First Check if the dirty bit is set, then write to ram if it is
            if line['dirty bit'] == 1:
                # Access the ram and replace the word
                updateRam(RAM, line['data'], line['addressUsed'])
                
            # Update valid bit
            line['valid bit'] = 1
            # Update tag
            line['tag'] = tag
            # Update dirty bit
            line['dirty bit'] = 0
            # Update the address that pulled it in
            line['addressUsed'] = hexRamIndex[-2:]
            # Update block
            # Determine where to start in the ram address
            blockIndex = (int(binaryAddress,2) % 8) // cache[len(cache)-1]['block size'] * cache[len(cache)-1]['block size']
            
            data = []
            
            # Pull the correct amount of bytes from ram
            for i in range(cache[len(cache)-1]['block size']):
                data.append(deepcopy(RAM[ramIndex][blockIndex + i]))
                
            line['data'] = data
            # Update the 'last used' of this new line
            updateLeastRecentlyUsed(cache, setIndex, line['tag'])
            
            # Return the data used to print
            return line['data'][int(blockOffset,2)], lineCounter, hexRamIndex
            
        lineCounter+=1
    
def leastFrequentlyUsedReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress):
    ##
    # Evicts the least frequently used line in a set when a cache-read miss is seen
    # @param Cache
    # @param RAM
    # @param Tag - in hex
    # @param SetIndex - in binary
    # @param BlockOffset - in binary
    # @param Address - Address of cache-read in binary
    # @returns Byte to be read, line evicted, ram address in hex
        
    # Index of RAM 2d array that contains correct block in decimal
    ramIndex = int(binaryAddress,2) // 8
    
    # Index of RAM 2d array in hex
    hexRamIndex = hex(int(binaryAddress,2)).upper()
    if len(hexRamIndex) == 3:
        hexRamIndex = '0x0'+hexRamIndex[-1]
    hexRamIndex = hexRamIndex[0] + 'x' + hexRamIndex[-2:]
    
    # Store the min frequency of the set
    minFrequency = cache[int(setIndex,2)][0]['frequency']
    
    # Finds the min frequency of the set
    for line in cache[int(setIndex,2)]:
        if line['frequency'] < minFrequency:
            minFrequency = line['frequency']
            
    # Used to know which line is evicted
    lineCounter = 0
            
    # Finds the line with the min frequency of the set
    for line in cache[int(setIndex,2)]:
        if line['frequency'] == minFrequency:
            # Update valid bit
            line['valid bit'] = 1
            # Update tag
            line['tag'] = tag
            # First Check if the dirty bit is set, then write to ram if it is
            if line['dirty bit'] == 1:
                # Access the ram and replace the word
                updateRam(RAM, line['data'], line['addressUsed'])
                
            # Update dirty bit
            line['dirty bit'] = 0
            
            # Determine where to start in the ram address
            blockIndex = (int(binaryAddress,2) % 8) // cache[len(cache)-1]['block size'] * cache[len(cache)-1]['block size']
            
            data = []
            
            # Pull the correct amount of bytes from ram
            for i in range(cache[len(cache)-1]['block size']):
                data.append(deepcopy(RAM[ramIndex][blockIndex + i]))
                
            line['data'] = data
            
            # Update the 'frequency' of this new line
            line['frequency'] = 1
            
            # Update the address that pulled it in
            line['addressUsed'] = hexRamIndex[-2:]
            
            # Return the data used to print
            return line['data'][int(blockOffset,2)], lineCounter, hexRamIndex
        
        lineCounter+=1
        
def updateRam(RAM, data, hexAddress):
    ##
    # Called when a dirty line is evicted so the data block is written to ram
    # @param RAM
    # @param Data - to replace (list of bytes)
    # @param Address - The address which pulled data parameter in, in hex (w/o '0x')
    # @returns Writes the data to the RAM. Nothing physically returned
        
    # The index of the line in the ram to replace
    ramIndex = int(hexAddress,16) // 8
    
    # The index of the byte in the line to start replacing
    lineIndex = int(hexAddress,16) % len(data) // len(data) * len(data)
    
    # The number of bytes transferred from the cache to the ram
    byteCounter = 0
    
    for i in range(lineIndex,len(data)):
        RAM[ramIndex][i] = data[byteCounter]
        byteCounter+=1
    
        
def cacheWrite(cache, RAM, hexAddress, byte):
    ##
    # Either writes the byte to cache and RAM or just RAM depending on policies
    # @param Cache
    # @param RAM
    # @param Address - Address of cache-write in hex (w/o '0x')
    # @param Byte - Byte of cache-write in hex (w/o '0x')
    # @returns Prints out cache write information. Nothing physically returned
        
    # Extract the tag, set index, and block offset    
    tag,setIndex,blockOffset = expandAddress(cache,hexAddress)
    
    # Convert the hex address to binary
    binaryAddress = bin(int(hexAddress,16))[2:]
    
    # Check for a write-hit
    for line in cache[int(setIndex,2)]:
        # If the tag matches and the line is valid, then write hit
        if line['tag'] == tag and line['valid bit'] == 1:
            # Increase the amount of cache hits
            cache[len(cache)-1]['hits']+=1

            # If the write hit policy is write_through
            if cache[len(cache)-1]['write hit policy'][0] == 1:
                
                # Write the data byte to both the cache and the ram
                writeThrough(cache, RAM, hexAddress, byte, True)
               
            # If the write hit policy is write_back 
            else:
                
                # Write the data byte only to the cache and set dirty bit
                writeBack(cache, hexAddress, byte, True) 
                
            # Break out of the function
            return
        
    # This is a write-miss if got this far in function
    cache[len(cache)-1]['misses']+=1
    
    # If the write miss policy is write_allocate
    if cache[len(cache)-1]['write miss policy'][1] == 'write_allocate':
        # Store the replacement policy
        replacementMethod = cache[len(cache)-1]['replacement policy'][1]
        
        # Use the replacement policy to store the data
        if replacementMethod == 'random_replacement':
            data = randomReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress)
        elif replacementMethod == 'least_recently_used':
            data = leastRecentlyUsedReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress)
        else:
            data = leastFrequentlyUsedReplacement(cache,RAM,tag,setIndex,blockOffset,binaryAddress)
            
        # If the write hit policy is write_through
        if cache[len(cache)-1]['write hit policy'][0] == 1:
            
            # Write the data byte to both the cache and the ram
            writeThrough(cache, RAM, hexAddress, byte, False)
            
        # If the write hit policy is write_back 
        else:
            
            # Write the data byte only to the cache and set dirty bit
            writeBack(cache, hexAddress, byte, False) 
            
        # Print out the information for the write-hit
        print('set:{}'.format(int(setIndex,16)))
        print('tag:{}'.format(tag))
        print('write_hit:no')
        print('eviction_line:{}'.format(data[1]))
        print('ram_address:{}'.format('0x'+hexAddress))
        print('data:{}'.format('0x'+byte))
        print('dirty_bit:{}'.format(cache[int(setIndex,2)][data[1]]['dirty bit']))
        
    # If the write miss policy is no_write_allocate
    else:
        # Find the correct index for the 2d array of the ram
        ramIndex = int(hexAddress,16) // 8

        # Update the ram
        RAM[ramIndex][int(blockOffset,2)] = byte
        
        ### ASK TA ###
        # Print out the information for the write-hit
        print('set:{}'.format(int(setIndex,16)))
        print('tag:{}'.format(tag))
        print('write_hit:no')
        print('eviction_line:-1')
        print('ram_address:{}'.format('0x'+hexAddress))
        print('data:{}'.format('0x'+byte))
        print('dirty_bit:-1')
        
def writeThrough(cache, RAM, hexAddress, byte, hit):
    ##
    # Writes the byte to the correct Ram and cache address.
    # Hit parameter is true if called from a write hit, otherwise it is false
    # @param Cache
    # @param RAM
    # @param Address - Address of cache-write in hex (w/o '0x')
    # @param Byte - Byte of cache-write in hex (w/o '0x')
    # @param Hit - as boolean
    # @returns Updates the cache and Ram correctly. Nothing physically returned
        
    # Extract the tag, set index, and block offset
    tag, setIndex, blockOffset = expandAddress(cache, hexAddress)
    
    # Find the correct line in the cache
    for line in cache[int(setIndex,2)]:
        if line['tag'] == tag and line['valid bit'] == 1:  # Correct line is found
            # Update the data block
            line['data'][int(blockOffset,2)] = byte
            
            if hit:
                # Print out the information for the write-hit
                print('set:{}'.format(int(setIndex,16)))
                print('tag:{}'.format(tag))
                print('write_hit:yes')
                print('eviction_line:-1')
                print('ram_address:{}'.format('0x'+hexAddress))
                print('data:{}'.format('0x'+byte))
                print('dirty_bit:{}'.format(line['dirty bit']))
            
            break
            
    # Find the correct index for the 2d array of the ram
    ramIndex = int(hexAddress,16) // 8

    # Update the ram
    RAM[ramIndex][int(blockOffset,2)] = byte
    

def writeBack(cache, hexAddress, byte, hit):
    ##
    # Writes the byte to the correct cache address and set dirty bit.
    # Hit parameter is true if called from a write hit, otherwise it is false 
    # @param Cache
    # @param RAM
    # @param Address - Address of cache-write in hex (w/o '0x')
    # @param Byte - Byte of cache-write in hex (w/o '0x')
    # @param Hit - as boolean
    # @returns Updates the cache and Ram correctly. Nothing physically returned
        
    # Extract the tag, set index, and block offset
    tag, setIndex, blockOffset = expandAddress(cache, hexAddress)
    
    # Find the correct line in the cache
    for line in cache[int(setIndex,2)]:
        if line['tag'] == tag and line['valid bit'] == 1:  # Correct line is found
            # Update the data block
            line['data'][int(blockOffset,2)] = byte
            # Set the dirty bit
            line['dirty bit'] = 1
            
            if hit:
                # Print out the information for the write-hit
                print('set:{}'.format(int(setIndex,16)))
                print('tag:{}'.format(tag))
                print('write_hit:yes')
                print('eviction_line:-1')
                print('ram_address:{}'.format('0x'+hexAddress))
                print('data:{}'.format('0x'+byte))
                print('dirty_bit:{}'.format(line['dirty bit']))
            
            break

def cacheFlush(cache):
    ##
    # Creates a cold cache with the same policies and hit rate
    # @param Cache
    # @returns Cold Cache with the same policies and hit rate
        
    # Stores all the information about the cache
    cacheInformation = deepcopy(cache[len(cache)-1])
    
    cacheSize = cacheInformation['cache size']
    blockSize = cacheInformation['block size']
    associativity = cacheInformation['associativity']
    
    # Create empty templates to create the cache with
    emptyBlock = '00'
    
    # Each line has a list of blocks
    emptyLine = {'valid bit': 0,
                 'dirty bit': 0,
                 'tag' : '00',
                 'data' : [],
                 'frequency' : 0,
                 'last used' : 0}
    
    # Each set is a list of lines
    cacheSet = []
    
    # Each cache is a list of sets
    newCache = []
    
    # Create the cold cache
    for i in range(blockSize):
        emptyLine['data'].append(deepcopy(emptyBlock))
        
    for i in range(associativity):
        cacheSet.append(deepcopy(emptyLine))
        
    for i in range(int(cacheSize / blockSize / associativity)):
        newCache.append(deepcopy(cacheSet))
        
    # Add in the cache information
    newCache.append(cacheInformation)
    
    # Print ending message
    print('cache_cleared')
    
    return newCache                 
        
def viewCache(cache):
    ##
    # Prints the cache to the console
    # @param Cache
    # @returns Prints the cache with cache information at the top. Nothing physiclaly returned
        
    # Print the cache size and policy information
    print('cache_size:{}'.format(cache[len(cache)-1]['cache size']))
    print('data_block_size:{}'.format(cache[len(cache)-1]['block size']))
    print('associativity:{}'.format(cache[len(cache)-1]['associativity']))
    print('replacement_policy:{}'.format(cache[len(cache)-1]['replacement policy'][1]))
    print('write_hit_policy:{}'.format(cache[len(cache)-1]['write hit policy'][1]))
    print('miss_hit_policy:{}'.format(cache[len(cache)-1]['write miss policy'][1]))
    print('number_of_cache_hits:{}'.format(cache[len(cache)-1]['hits']))
    print('number_of_cache_misses:{}'.format(cache[len(cache)-1]['misses']))
    
    # Print the contents of the actual cache
    print('cache_content:')

    for setNumber in range(len(cache)-1):
        for line in cache[setNumber]:
            print('{} {} {} '.format(line['valid bit'], line['dirty bit'], line['tag']),end='')
            for byte in line['data']:
                print('{} '.format(byte),end='')
            print()
            
def viewMemory(RAM):
    ##
    # Prints the RAM to the console
    # @param RAM
    # @returns Prints the RAM with ram information at the top. Nothing physically returned
        
    # Print out the ram information  
    print ("memory_size:{}\nmemory_content:\naddress:data".format(256))
        
    # Print out the ram content
    for i in range(len(RAM)):
        address = hex(i*8).upper()
        
        # Pads one single digit hex number with additional zero
        if len(address) == 3:
            address = address[0:2] + '0' + address[-1]
            
        address = '0x' + address[-2:]
            
        print(address,end=':')
        
        for byte in RAM[i]:
            print(byte,end=' ')
            
        print()
        
def cacheDump(cache):
    ##
    # Writes each line in the cache on a new line in the file
    # @param Cache
    # @returns Dumps all the cache data in cache.txt. Nothing physically returned
        
    # Open cache.txt to write to
    ofs = open('cache.txt','w')
    
    # Write each line on a new line in the file
    for setNumber in range(len(cache)-1):
        for line in cache[setNumber]:
            for byte in line['data']:
                ofs.write(byte+' ')
            ofs.write('\n')
        
def memoryDump(RAM):
    ##
    # Writes each byte on a new line
    # @param RAM
    # @returns Dumps all RAM memory in ram.txt. Nothing physically returned
        
    # Open ram.txt to write to
    ofs = open('ram.txt','w')
    
    for row in RAM:
        for byte in row:
            ofs.write(byte+'\n')
            

def expandAddress(cache, hexAddress):
    ##
    # Breaks down a hex address into the three parts neccessary for the cache
    # @param Cache
    # @param Address - in hex
    # @reutrns Tag in hex (w/o '0x'), Set index in binary, Block offset in binary\n
        
    # Convert the hex address to binary
    binaryAddress = bin(int(hexAddress,16))[2:]
    
    # Pad the binary address with leading zeros if neccessary
    if len(binaryAddress) < 8:
        binaryAddress = '0'*(8 - len(binaryAddress)) + binaryAddress
        
    # Extract the block offset, tag index, and set index bits
    numberOfSetBits = int(log2(len(cache) - 1))
    numberOfOffsetBits =  int(log2(cache[len(cache)-1]['block size']))
    numberOfTagBits = 8 - numberOfSetBits - numberOfOffsetBits
    
    # Extract tag bits
    tag = hex(int(binaryAddress[0:numberOfTagBits],2)).upper()
    binaryAddress = binaryAddress[numberOfTagBits:]
    
    # Format the tag in hex correctly -- Padded with leading zero if necessary
    if len(tag) == 3:
        tag = '0'+tag[-1]
    else:
        tag = tag[-2:]
    
    # Extract set index
    setIndex = binaryAddress[0:numberOfSetBits]
    binaryAddress = binaryAddress[numberOfSetBits:]
    
    # Extract block offset
    blockOffset = binaryAddress[0:numberOfOffsetBits]
    binaryAddress = binaryAddress[numberOfOffsetBits:]
    
    # If only one byte per line, make block offset always 0
    if blockOffset == '':
        blockOffset = '0'
        
    # If fully associativity, make the set index always 0
    if setIndex == '':
        setIndex = '0'
    
    # Return values
    return tag, setIndex, blockOffset
                    