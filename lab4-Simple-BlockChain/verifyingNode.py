from blockChain import Block, Blockchain
import time
import secrets
import json


def verify_UTP(UTP):
    VTP = []

    #Generate blockchain with genesis transaction
    block_chain = Blockchain()
    gen_transaction = UTP[0]
    block_chain.add_new_transaction(gen_transaction)
    pools = pool_update(UTP, VTP, gen_transaction)
    UTP = pools[0]
    VTP = pools[1]

    while len(UTP):
        block = Block(0, secrets.choice(UTP), 0)
        pools = verify_transaction(block_chain, block, UTP, VTP)
        UTP = pools[0]
        VTP = pools[1]

   #block_chain.print_chain()


def verify_transaction(chain, block, UTP, VTP):
    """
    :param block: a random transaction from a global Unverified Transaction Pool (UTP)
    :return: discards transaction from network and prints out error if invalid due to double-spending
             if input doesn't exist yet, return to UTP

             if valid block, returns a block_chain that is the Global Verified Pool
    """

    #holds verifying nodes for the transaction of the block in UTP
    valid = True

    pools = [UTP, VTP]
    if len(block.transaction['input']) == 0:
        #input doesn't exist yet, return it to UTP
        print("Input does not exist yet")
        valid = False

    if check_double_spending(block.transaction, VTP):
        print("Double spending, removing from UTP")
        UTP.remove(block.transaction)
        valid = False

    if not check_signature(block):
        print("Invalid Signature, removing from UTP")
        UTP.remove(block.transaction)
        valid = False

    if not check_amount_of_coins(block):
        print("Invalid Input-Output Coin Amount, removing from UTP")
        UTP.remove(block.transaction)
        valid = False

    if check_input(block) and valid:
        #valid block
        chain.add_new_transaction(block.transaction)
        pools = pool_update(UTP, VTP, block.transaction)

        if not len(UTP):
            time.sleep(5)

    else:
        print("input: {}".format(check_input(block)))
        print("sig: {}".format(check_input(block)))
        print("amount: {}".format(check_input(block)))
        for i in UTP:
            print(i)

    return pools


def pool_update(UTP, VTP, transaction):
    '''
    :param UTP: unverified transaction pool
    :param VTP: verified transaction pool
    :return: updated transaction pools
    '''
    print("Trying to remove from UTP:\n{}".format(transaction['id']))
    UTP.remove(transaction)
    print("Removed Succesfully!!!\n")
    VTP.append(transaction)
    print("Printing VTP:")
    for i in VTP:
        print(i)
    return [UTP, VTP]


def check_double_spending(transaction, VTP):
    """
    :param transaction: a transaction to check for double spending
    :return: True if input is already in VTP
    """
    for i in VTP:
        if i["input"] == transaction["input"]:
            return True

    return False


def check_signature(block):
    """
    :param block: a random transaction from UTP
    :return: True if there's a signature
    """
    if not block.transaction['signature']:
        return False

    return True


def check_input(block):
    """
    :param block: a random transaction from UTP
    :return: True if all the inputs in transaction are unique
    """
    if len(block.transaction['input']) == 1:
        return True

    check_list = []
    for i in range(len(block.transaction['input'])):
        check_list.append(block.transaction['input'][i]['person'])

    unique = set(check_list)

    if len(unique) == len(check_list):
        #all unique inputs
        return True

    return False


def check_amount_of_coins(block):
    """
    :param block: a random transaction from UTP
    :return: True if the amount of coins in output are equal to the amount of coins in input
             else False
    """
    total_input_coins = 0
    total_output_coins = 0

    #transaction json block takes input as a list of dictionaries with the key being the amount of coins
    #and the value being the 'person' the coins are being sent o
    for i in range(len(block.transaction['input'])):
        coin_list = block.transaction['input'][i]
        #print(coin_list)
        total_input_coins += int(coin_list['coin'])

    for i in range(len(block.transaction['output'])):
        coin = block.transaction['output'][i]
        total_output_coins += int(coin['coin'])

    if total_output_coins == total_input_coins:
        return True

    return False