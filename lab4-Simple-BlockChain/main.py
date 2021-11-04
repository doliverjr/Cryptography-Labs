import json
from blockChain import Blockchain
from verifyingNode import *
from hashlib import sha256
import random

#each block contains 1 transaction
#Transaction format
    #"id" = sha256 hash
    #"type" = Merge, Trans, or Join
    #"input" = pointer to 1 or more prior transaction outputs
    #"output" = transaction output (public key-coin values)
    #"signatures"

#public/private key pairs from https://learnmeabitcoin.com/technical/public-key-hash
pubk1 = "03d518bced8fd71a000fccabe9f4590c77affd653cbaf96ece8a6d84ddfdcde5c6"
privk1 = "f992698eb3ac15e4bc2d45ac1721d0ef8e2c428d35dd7a61d09a6c07673d0619"
pubk2 = "03c4330ce26c4433e42a6554c4cd405ccab2264aa454633fe6be216555fbba8a9b"
privk2 = "418ef56996ed8e8cb80677d7b014d90b12b7663469b357df182649c09dcb0086"
pubk3 = "020df70143ddbb90da02cfd24f150fb5863980ae086527f7e092443d93fb5d4291"
privk3 = "575a36b704bc32617cae30bf303a0d7b6d669a9ad3678c88295dd317873ebf8f"
pubk4 = "021e296f1a975234ed2bd383c4f16293236b377d3c766ca4b034d62ba3131d59a8"
privk4 = "b2a90730999673f3009fec0ef46f4ec3788e8a09be693f35e0f24170d45a9e7a"
pubk5 = "02702a629019a668d170df75d2ded656923a38134503a403724f638561ab94f67c"
privk5 = "5959d20c52d9ae4382369dc7f9d993f83dbb9bc988f5db186aaabc4f42bea0e9"

def createTransaction(id, type, input, output, signature):
    transaction = {"id":id, "type":type, "input":input, "output":output, "signature":signature}
    transaction = json.dumps(transaction)
    return json.loads(transaction)

def transfer(blockchain, id, input, output, signature):
    transaction = createTransaction(id, "TRANS", input, output, signature)
    blockchain.add_new_transaction(transaction)

def merge(id, input, output, signature):
    transaction = createTransaction(id, "MERGE", input, output, signature)
    blockchain.add_new_transaction(transaction)

def join(id, input, output, signature):
    transaction = createTransaction(id, "JOIN", input, output, signature)
    blockchain.add_new_transaction(transaction)

#hash of the id field to put into json object
def get_hash_id(input, output, signature):
    data = {
        "input": input,
        "output": output,
        "signature": signature
    }

    to_hash = json.dumps(data)

    return sha256(to_hash.encode()).hexdigest()

#hash of the signature field to put into json object
def get_hash_signature(type, input, output):
    data = {
        "type": type,
        "input": input,
        "output": output
    }

    to_hash = json.dumps(data)

    return sha256(to_hash.encode()).hexdigest()

def generate_genesis_block():
    input = None
    output = [{'coin': 25, 'person': "03d518bced8fd71a000fccabe9f4590c77affd653cbaf96ece8a6d84ddfdcde5c6"}]
    type = "GENESIS"

    write_transaction_to_file(type, input, output)

def write_transaction_to_file(type, input, output):
    f = open("transactionFile.json", "a")

    signature = get_hash_signature(type, input, output)
    id = get_hash_id(input, output, signature)

    data = {
        'id': id,
        'type': type,
        'input': input,
        'output': output,
        'signature': signature
    }

    output = json.dump(data, f)

    #print(data)
    #print(output)
    #f.write(output)
    f.write("\n")

    f.close()

#need at least 1 malicious transaction (double spending) and 1 invalid transaction
#at least 10 total transactions, with at least one of each: JOIN, MERGE, TRANS
def generate_transactions():
    f = open("transactionFile.json", "a")

    #chooses a random number 1-3 to choose either JOIN, MERGE, or TRANS
    r = random.randint(1, 4)

    #need to change the input and output values each time
    if r == 1:
        #TRANS
        input = [{'coin': 1, 'person': pubk3}] #from
        output = [{'coin': 1, 'person': pubk5}] #to
        type = "TRANS"
        write_transaction_to_file(type, input, output)
    elif r == 2:
        #MERGE
        input = [{'coin': 15, 'person': pubk2}, {'coin': 1, 'person': pubk3}]
        output = [{'coin': 16, 'person': pubk4}]
        type = "MERGE"
        write_transaction_to_file(type, input, output)
    else:
        #JOIN
        input = [{'coin': 2, 'person': pubk2}]
        output = [{'coin': 1, 'person': pubk1}, {'coin': 1, 'person': pubk2}]
        type = "JOIN"
        write_transaction_to_file(type, input, output)

    #invalid transaction (line 6 in transactionFile.json)
    '''
    input = [{'coin': 3, 'person': pubk3}]
    output = [{'coin': 5, 'person': pubk4}]
    type = "TRANS"

    write_transaction_to_file(type, input, output)
    '''

    #malicious transition (idk how double spending works)
    '''
    write transation here
    '''
    f.close()


if __name__ == '__main__':
    blockchain = Blockchain()

    #generate_genesis_block()
    #generate_transactions()
    #blockchain.print_chain()

    UTP = []
    with open('transactionFile.json') as f:
        for line in f:
            temp = json.dumps(line.strip('\n'))
            UTP.append(json.loads(temp))

    for i in range(len(UTP)):
        UTP[i] = json.loads(UTP[i])

    verify_UTP(UTP)

