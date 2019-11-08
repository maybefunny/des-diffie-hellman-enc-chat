import math
from random import seed
from random import randint
from datetime import datetime

class diffiehellman:
    def __init__(self, pubkey1, pubkey2, privatekey=None):
        self.public_key1 = pubkey1
        self.public_key2 = pubkey2

        if(privatekey == None):
            seed(datetime.now())
            n = randint(1000, 5000)
            self.private_key = self.nthprime(n)
        else:
            self.private_key = privatekey
        self.full_key = None
        self.partial_key = None

    def generate_partial_key(self):
        partial_key = pow(self.public_key1,self.private_key, self.public_key2)
        self.partial_key = partial_key
        return self.partial_key

    def generate_full_key(self, partial_key_r):
        full_key = pow(partial_key_r,self.private_key, self.public_key2)
        self.full_key = full_key
        return full_key

    def get_full_key(self):
        if(self.full_key != None):
            return self.full_key
        return None

    def get_partial_key(self):
        if(self.partial_key != None):
            return self.partial_key
        return None

    def nthprime(self, n):
        start = 2
        count = 0
        while True:
            if all([start % i for i in range(2, int(math.sqrt(start)) + 1)]) != 0:
                count += 1
                if count == n:
                    return start
            start += 1 