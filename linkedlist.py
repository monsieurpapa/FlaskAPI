
class Node:
    def __init__(self, data=None, next_node =None):
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head =None
        self.last_node = None
    
    def to_list(self):
        l = []
        if self.head is None:
            return l
        node = self.head
        while node:
            l.append(node.data)
            node = node.next_node 
        return l

    def print_ll(self):
        ll_string = ""
        node =self.head
        if node is None:
            print(None)
        while node:
            ll_string += f"{str(node.data)} ->"
            if node.next_node is None:
                ll_string +=" None"
            node = node.next_node
        print(ll_string) 

# ll = LinkedList()
# node4 = Node("data4",None)
# node3 =Node("data3",node4)
# node2 = Node("data2",node3)
# node1 = Node("data1",node2)
# ll.head = node1
# ll.print_ll()
    def insert_beginning(self,data):
        if self.head is None:
            self.head = Node(data,None)
            self.last_node = self.head
        new_node = Node(data,self.head)
        self.head = new_node

# ll = LinkedList()
# ll.insert_beginning("data")
# ll.insert_beginning("not data")
# ll.insert_beginning("cow")
# ll.print_ll()
    def insert_at_end(self,data):
        if self.head is None:
            self.insert_beginning(data)
            return

        # if self.last_node is None:
        #     print("last node is none")
        #     node = self.head
        #     # while node.next_node:
        #     #     print("iter",node.data)
        #     #     node = node.next_node
        #     node.next_node = Node(data,None)
        #     self.last_node = node.next_node
        #else:
        self.last_node.next_node = Node(data,None)
        self.last_node =self.last_node.next_node

# ll = LinkedList()
# ll.insert_beginning("data") 
# ll.insert_at_end("end")
# ll.insert_at_end("end2")
# ll.print_ll()
    def get_user_by_id(self,user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id): #"id" is a dictionary key that is pushed to the database using the insert_beginning() function
                return node.data
            node = node.next_node
        return None
        