import uuid
import csv
import json

fields = ['Name', 'Branch', 'Quantity', 'ID', 'X', 'Y', 'Correct Position']

################## ITEM #######################
qrcode_items_reads = []
qrcode_location_reads = []
random_uuid = str(uuid.uuid4())
counter = 1

correct_items = [[1, 'Vazio'], [2, 'Iogurte'], [3, 'Margarina'], [4, 'Suco de Laranja'], [5, 'Coca Cola']]
################## ITEM #######################

def existsInList(item):
    global qrcode_items_reads
    global qrcode_location_reads

    for code in qrcode_items_reads:
        if (item == code):
            return True
    
    for code in qrcode_location_reads:
        if (item == code):
            return True
    return False

def isCorrectPosition(id, name):
    global correct_items

    for item in correct_items:
        if item[0] == id and item[1] == name:
            return True
    return False

# Abrindo o CSV
with open(random_uuid + '.csv', 'w') as csvfile:
    # Criando o cabeçalho do CSV
    csvwriter = csv.writer(csvfile)
 
    # writing the fields
    csvwriter.writerow(fields)

def createReport(codigos_qr):
    global counter

    for codigo in codigos_qr:  
        rawJson = json.loads(codigo.data.decode('utf-8'))

        #Checando se o QRCODE lido é referente a um item de prateleite
        if (rawJson['data']['object'] is not None):
            name = rawJson['data']['object']['name']
            branch = rawJson['data']['object']['branch']
            quantity = rawJson['data']['quantity']
            id = rawJson['data']['position']['id']
            x = rawJson['data']['position']['x']
            y = rawJson['data']['position']['y']

            if (existsInList(id)):
                break

            print('Identificado QRCODE de um item de prateleita! ' + name)

            qrcode_items_reads.append(id)

            with open(random_uuid + '.csv', 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                
                correct = isCorrectPosition(counter, name)

                csvwriter.writerow([name, branch, quantity, id, x, y, correct])

            counter += 1
        elif (rawJson['data']['location'] is not None):
            print('sou posicao')
        else:
            print('Este tipo de QRCODE não faz parte deste projeto!')
            break