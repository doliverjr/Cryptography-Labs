from hashlib import sha256
import json

#Class for each block
    #index = the position in the chain
    #transaction = transaction, 1 per block
    #prev = prev blocks hash
    #nonce = nonce for the transaction

class Block:
    def __init__(self, index, transaction, prev, nonce=0):
        self.index = index
        self.transaction = transaction
        self.prev = prev
        self.nonce = nonce

    #creates hash based off of block data
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    #printing a block will output its transaction
    def __str__(self):
        return str(self.transaction)


#Class for the blockchain
    #uncomfirmed = new transaction to add
    #chain = chain of blocks

class Blockchain:
    #affects how much work the proof is
    difficulty = 2

    def __init__(self):
        self.unconfirmed = ""
        self.chain = []
        self.create_genesis_block()

    # creates initial block
    def create_genesis_block(self):
        genesis_block = Block(0, "GENESIS", "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.compute_hash()
        if previous_hash != block.prev:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    #call to add a transaction to the blockchain
    def add_new_transaction(self, transaction):
        self.unconfirmed = transaction
        self.mine()

    #adds the new transactiona and confirms its valid
    def mine(self):
        if not self.unconfirmed:
            return 0

        last_block = self.last_block
        new_block = Block(index = last_block.index +1,
                          transaction = self.unconfirmed,
                          prev = last_block.compute_hash())

        proof = self.proof_of_work(new_block)
        was_added = self.add_block(new_block, proof)
        self.unconfirmed = ""
        return new_block.index

    def print_chain(self):
        chain_transactions = []
        chain_nonce = []

        for i in self.chain:
            chain_transactions.append(i.transaction)
            chain_nonce.append(i.nonce)

        print("\n-----BLOCKCHAIN PRINT OUT-----\n")
        print("-----Nonce Values-----\n{}\n".format(chain_nonce))
        print("-----Transactions-----")
        for i in chain_transactions:
            print(i)