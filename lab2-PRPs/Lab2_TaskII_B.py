import binascii

Block_Size = 16

def countReps(ciphertext, blockSize=Block_Size):
    blocks = []
    for i in range(0, len(ciphertext), blockSize):
        blocks.append(ciphertext[i:i+blockSize])

    numReps = len(blocks) - len(set(blocks))
    result = {
        'ciphertext': ciphertext,
        'reps': numReps
    }
    return result

def Lab2_TaskII_B():
    file = open("Lab2.TaskII.B.txt", "rb")
    cipherReps = []

    for line in file:
        unhexed = binascii.unhexlify(line.strip())
        cipherReps.append(countReps(unhexed[54:]))

    mostRep = sorted(cipherReps, key=lambda x: x['reps'], reverse=True)[0]
    print("{}".format(mostRep['ciphertext']))