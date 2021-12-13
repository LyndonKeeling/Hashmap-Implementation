# Description: Implementation of hash maps. Utilizes previously built out (but provided) linked list and dynamic array
# implementations. Portfolio project for CS261 at Oregon State University.


# Import pre-written DynamicArray and LinkedList classes
from helper_hashmap import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out


    def clear(self) -> None:
        """
        Removes contents of the buckets, resets size to 0
        """
        prev_capacity = self.capacity
        new_hash_map = HashMap(self.capacity, self.hash_function)
        self.buckets = new_hash_map.buckets
        self.capacity = prev_capacity
        self.size = 0


    def get(self, key: str) -> object:
        """
        Returns the value associated with a given key. If the key is not present, the method will return None.
        """
        hash_value = self.hash_function(key)
        index = hash_value % self.capacity
        current_bucket = self.buckets.get_at_index(index)

        if current_bucket.contains(key):
            return current_bucket.contains(key).value


    def put(self, key: str, value: object) -> None:
        """
        Inputs key/value into the hash map. Converts key into hash value and determines placement. If key already exists
        replace the value.
        """
        hash_value = self.hash_function(key)
        index = hash_value % self.capacity
        current_bucket = self.buckets.get_at_index(index)

        if current_bucket.length() == 0:
            current_bucket.insert(key, value)
            self.size += 1
        if current_bucket.contains(key):
            to_be_replaced = current_bucket.contains(key)
            to_be_replaced.value = value
        else:
            current_bucket.insert(key, value)
            self.size += 1


    def remove(self, key: str) -> None:
        """
        Removes a passed key and associated value from the hashmap. If it is not found, no exception is raised.
        """
        hash_value = self.hash_function(key)
        index = hash_value % self.capacity
        current_bucket = self.buckets.get_at_index(index)

        if current_bucket.contains(key) is not None:
            current_bucket.remove(key)
            self.size -= 1


    def contains_key(self, key: str) -> bool:
        """
        Determines whether the hash map contains a passed key. Returns a true/false boolean.
        """
        hash_value = self.hash_function(key)
        index = hash_value % self.capacity
        current_bucket = self.buckets.get_at_index(index)

        if current_bucket.length() == 0:
            return False
        if current_bucket.contains(key) is not None:
            return True
        return False


    def empty_buckets(self) -> int:
        """
        Determines the amount of empty buckets in the hashmap.
        """
        empty = 0
        for i in range(self.capacity):
            current_bucket = self.buckets.get_at_index(i)
            if current_bucket.length() == 0:
                empty += 1
        return empty


    def table_load(self) -> float:
        """
        Calculates table load which is The load factor is a measure of how full the hash table is allowed to get
        before its capacity is automatically increased.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table given. All current hash table elements must be rehashed.
        """
        # base case
        if new_capacity < 1:
            return None

        prev_size = self.size
        new_hash_map = HashMap(new_capacity, self.hash_function)
        i = 0
        while self.size != 0:
            current_bucket = self.buckets.get_at_index(i)
            if current_bucket.length() != 0:
                for node in current_bucket:
                    new_hash_map.put(node.key, node.value)
                    self.size -= 1
            i += 1

        self.size = prev_size
        self.buckets = new_hash_map.buckets
        self.capacity = new_capacity


    def get_keys(self) -> DynamicArray:
        """
        Returns key values from the hash map stored within a dynamic array.
        """
        new_da = DynamicArray()
        i = 0

        while new_da.length() != self.size:
            current_bucket = self.buckets.get_at_index(i)
            if current_bucket.length() != 0:
                for node in current_bucket:
                    new_da.append(node.key)
            i += 1
        return new_da


# BASIC TESTING
# if __name__ == "__main__":
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)

    # #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         result &= m.contains_key(str(key))
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    #
    # m.resize_table(1)
    # print(m.get_keys())
    #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
