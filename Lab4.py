#student name:      Idil Bil

import threading

def sortingWorker(firstHalf: bool) -> None:
    """
       If param firstHalf is True, the method
       takes the first half of the shared list testcase,
       and stores the sorted version of it in the shared 
       variable sortedFirstHalf.
       Otherwise, it takes the second half of the shared list
       testcase, and stores the sorted version of it in 
       the shared variable sortedSecondHalf.
       The sorting is ascending and you can choose any
       sorting algorithm of your choice and code it.
    """
    tempFirstHalf = testcase[:int(len(testcase)/2)]          #list for sorting the first half
    tempSecondHalf = testcase[int(len(testcase)/2):]         #list for sorting the second half

    if firstHalf == True:
        while len(tempFirstHalf) != 0:
            minFirstHalf = tempFirstHalf[0]                  #temporary minimum value until a smaller one is found
            for index_1 in range(len(tempFirstHalf)):        #goes until the list is empty
                if tempFirstHalf[index_1] <= minFirstHalf:   #compares the indexes to the temporary minimum value
                    minFirstHalf = tempFirstHalf[index_1]    #if the value is smaller the minimum is changed
            sortedFirstHalf.append(minFirstHalf)             #the new minimum value is added to the sortedFirstHalf list
            tempFirstHalf.remove(minFirstHalf)               #and it's removed from the tempFirstHalf list
    else:                                                    #same thing for the second half
        while len(tempSecondHalf) != 0:
            minSecondHalf = tempSecondHalf[0]                
            for index_2 in range(len(tempSecondHalf)):
                if tempSecondHalf[index_2] <= minSecondHalf: 
                    minSecondHalf = tempSecondHalf[index_2]  
            sortedSecondHalf.append(minSecondHalf)          
            tempSecondHalf.remove(minSecondHalf)             

def mergingWorker() -> None:
    """ This function uses the two shared variables 
        sortedFirstHalf and sortedSecondHalf, and merges/sorts
        them into a single sorted list that is stored in
        the shared variable sortedFullList.
    """
    while(len(sortedFirstHalf) != 0 and len(sortedSecondHalf) != 0):    #in a loop until one of the lists are completely empty
        if(sortedFirstHalf[0] <= sortedSecondHalf[0]):                  #compares the first element of the lists
            SortedFullList.append(sortedFirstHalf[0])                   #if the element in the first list is smaller adds that to the SortedFullList
            sortedFirstHalf.remove(sortedFirstHalf[0])                  #deletes that element
        else:
            SortedFullList.append(sortedSecondHalf[0])                  #if the element in the first list is smaller adds that to the SortedFullList
            sortedSecondHalf.remove(sortedSecondHalf[0])                #deletes that element

    if len(sortedFirstHalf) != 0:                                       #checks if sortedFirstHalf is empty after the while loop
        for n in range(len(sortedFirstHalf)):
            SortedFullList.append(sortedFirstHalf[n])                   #if so adds all those elemenst one by one into SortedFullList
    else:                                                               #if not adds the leftover elements from sortedSecondHalf to the SortedFullList
        for n in range(len(sortedSecondHalf)):                          
            SortedFullList.append(sortedSecondHalf[n])                  

if __name__ == "__main__":
    #shared variables
    testcase = [8,5,7,7,4,1,3,2]
    sortedFirstHalf: list = []
    sortedSecondHalf: list = []
    SortedFullList: list = []

    #initializing the threads
    firstThread = threading.Thread(target=sortingWorker, args=(True,))
    secondThread = threading.Thread(target=sortingWorker, args=(False,))
    mergeThread = threading.Thread(target=mergingWorker)

    #start and join commands for the sortingWorker
    firstThread.start()
    secondThread.start()
    firstThread.join()
    secondThread.join()

    #start and join command for the mergingWorker after sorting
    mergeThread.start()
    mergeThread.join()

    #as a simple test, printing the final sorted list
    print("The final sorted list is ", SortedFullList)