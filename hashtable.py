
class Node:  # just an instance of a Node having a head and a pointer to the next node 
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node =next_node


class Data: #what is passed to our node
    def __init__(self,key,value):
        self.key =key
        self.value =value

class HashTable:
    def __init__(self, table_size):  #there has to be a size because the hash to be created has to be within the bounds of the Hashtable
        self.table_size = table_size
        self.hash_table = [None] * table_size   # if table_size is 3 : [None, None , None]
    
    def custom_hash(self, key):
        hash_value =0
        for i in key:
            hash_value += ord(i) #ord takes the integer representation of each character, the hash_value is the result of their sum
            #the remainder can never be larger than the number we are diving by 
            hash_value = (hash_value *ord(i)) % self.table_size  # assures the hash value does not exceed the table size
            #hash value never equals to an index greater than the final index of the table
        return hash_value  #this value is basically an integer that represents an index in the hastable's list of indexes
    

    def add_key_value(self, key, value):
        hashed_key = self.custom_hash(key) 
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key,value),None) # add new node at the returned hash index with key,value as data, pointing to None since there was Nothing at that index
            
            #the collusion has to be avoided whereby there already exists a node at the returned hash index
        else:
            node = self.hash_table[hashed_key]
            while node.next_node:
                node = node.next_node
            node.next_node = Node(Data(key,value),None)
    

    def get_value(self, key):
        hashed_key = self.custom_hash(key) #custom_hash always returms the same hash for the same key
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.next_node is None:
                return node.data.value
            while node.next_node: #otherwise traverse the entire linkedlist
                if key ==node.data.key:
                    return node.data.value
                node =node.next_node #jump to the next node until the given key matches the node's data key
            
            if key== node.data.key:
                 return node.data.value
        return None
    

    def print_table(self):
        print("{")
        for i, val in enumerate(self.hash_table):
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string+=(
                            str(node.data.key) + " : " + str(node.data.value) + " -->"
                        )
                        node = node.next_node
                    llist_string +=(
                        str(node.data.key)+ " : " + str(node.data.value) + " --> None"
                    )
                    print (f" [{i}] {llist_string}")
                else:
                    print(f" [{i} {val.data.key} : {val.data.value}")
            else:
                print(f" [{i}] {val}")
        print("}")

ht = HashTable(4)
ht.add_key_value("Dieudo", "Munganga")
ht.add_key_value("Hi", "There")
ht.print_table()