
class Node:
    def __init__(self, value, next) -> None:
        self.value = value
        self.next = next

class LinkedList:
    def __init__(self) -> None:
        self.head = None
    
    def _append(self, value):
        tempHead = self.head
        lastNode : Node| None = None
        
        while tempHead:
            lastNode = tempHead
            tempHead = tempHead.next
        
        if lastNode:
            lastNode.next = Node(value, None)
        else:
            pass
    
    def preppend(self, value):
        new_node = Node(value, self.head)
        self.head = new_node
    
    def print(self):
        tempNode = self.head
        while tempNode:
            print(tempNode.value, "->", end=" ")
            tempNode = tempNode.next
        print("Null")
    
    def __iadd__(self, value):
        self._append(value)
        return self
        
    def __str__(self) -> str:
        output_string = ''
        tempNode = self.head
        while tempNode:
            output_string += str(tempNode.value) + " -> "
            tempNode = tempNode.next
        return output_string + "Null"
    
    

linked_list = LinkedList()
linked_list.preppend(10)
# linked_list.preppend(20)

# linked_list._append(45)
linked_list += 83

print(linked_list)