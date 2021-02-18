
    def sortList():
    '''
    Merge sort function for linked-list data structures.
    '''
       # return if there are 0 or 1 items in self
       if (self.size < 2):
            return
        else:
            middle = self.splitList()
            # the node after the middle starts the second list
            head_two = middle.next
            # cut the list in half by removing the reference
            middle.next = None

            list_one = self.head
            list_two = head_two

            merge()
            

    def splitList():
    '''
    Finds middle of list for merge sort
    '''
        # Indices for finding middle of linked list
        # Tortise moves one space, hare moves two.
        # When the hare cannot move forward,
        # the location of the tortise is returned.
        tortise = self.head
        hare = self.head

        while(hare.next != None and hare.next.next != None):
              tortise = tortise.next
              hare = hare.next.next

        return tortise.next

    def merge():
