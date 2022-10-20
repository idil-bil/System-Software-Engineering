#student name:  Idil Bil

import threading
import random #is used to cause some randomness 
import time   #is used to cause some delay in item production/consumption

class circularBuffer: 
    """ 
        This class implement a barebone circular buffer.
        Use as is.
    """
    def __init__ (self, size: int):
        """ 
            The size of the buffer is set by the initializer 
            and remains fixed.
        """
        self._buffer = [0] * size   #initilize a list of length size
                                    #all zeroed (initial value doesn't matter)
        self._in_index = 0   #the in reference point
        self._out_index = 0  #the out reference point

    def insert(self, item: int):
        """ 
            Inserts the item in the buffer.
            The safeguard to make sure the item can be inserted
            is done externally.
        """
        self._buffer[self._in_index] = item
        self._in_index = (self._in_index + 1) % SIZE

    def remove(self) -> int:
        """ 
            Removes an item from the buffer and returns it.
            The safeguard to make sure an item can be removed
            is done externally.
        """
        item = self._buffer[self._out_index]
        self._out_index = (self._out_index + 1) % SIZE
        return item

def producer() -> None:
    """
        Implement the producer function to be used by the producer thread.
        It must correctly use full, empty and mutex.
    """
    def waitForItemToBeProduced() -> int: #inner function; use as is
        time.sleep(round(random.uniform(.1, .3), 2)) #a random delay (100 to 300 ms)
        return random.randint(1, 99)  #an item is produced

    for _ in range(SIZE * 2): #we just produce twice the buffer size for testing
        item = waitForItemToBeProduced()  #wait for an item to be produced
        print(f"DEBUG: {item} produced")

        empty.acquire()       #producer thread acquires the number of empty slots, decreases them by one and goes until theres none left
        
        mutex.acquire()       #lock on, in critical section
        buffer.insert(item)   #stores the produced item in the circular buffer
        mutex.release()       #lock off    
        
        full.release()        #increases the number of full slots by one    

def consumer() -> None:
    """
        Implement the consumer function to be used by the consumer thread.
        It must correctly use full, empty and mutex.
    """
    for _ in range(SIZE * 2): #we just consume twice the buffer size for testing

        full.acquire()          #consumer thread acquires the number of full slots, decreases them one by one and goes until theres none left
        
        mutex.acquire()         #lock on, in critical section 
        item = buffer.remove()  #removes the item from the circular buffer
        mutex.release()         #lock off
        
        empty.release()         #increases the number of empty slots by one

        #use the following code as is
        def waitForItemToBeConsumed(item) -> None: #inner function; use as is
            time.sleep(round(random.uniform(.1, .3), 2)) #a random delay (100 to 300 ms)
            #to simulate consumption, item is thrown away here by just ignoring it
        waitForItemToBeConsumed(item)  #wait for the item to be consumed
        print(f"DEBUG: {item} consumed")

if __name__ == "__main__":
    SIZE = 5  #buffer size
    buffer = circularBuffer(SIZE)  #initialize the buffer

    full = threading.Semaphore(0)         #full semaphore: number of full buffers
                                          #initial value set to 0
    empty = threading.Semaphore(SIZE)     #empty semaphore: number of empty buffers
                                          #initial value set to SIZE
    mutex = threading.Lock()  #lock for protecting data on insertion or removal

    #the producer-consumer thread creation
    producerThread = threading.Thread(target=producer)
    consumerThread = threading.Thread(target=consumer)

    #start and join commands for the producer-consumer threads
    producerThread.start()
    consumerThread.start()
    producerThread.join()
    consumerThread.join()
