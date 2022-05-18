# class passManObject:
import hashlib
import json
import os
import random
import pyperclip

SRandInt = random.SystemRandom().randint
def pasteTextFromClipboard():
    return pyperclip.paste()

def pasteTextToClipboard(text):
    pyperclip.copy(text)
    return True

def dec_to_base(num,base=None, special_chars=False):  #Maximum base - 36
    new_num    = ""
    char_set_2  =['!@#$%^&*()_-;:<>?/\|', 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '0123456789']
    char_set    = char_set_2[0:] if special_chars else char_set_2[1:]
    chrs        =''.join(char_set)
    if base is None:
        base    = len(chrs)
    while num>0:
        dig     = int(num%base)
        new_num = chrs[dig % len(chrs)] + new_num
        num     //= base
    new_num = new_num[::-1]  #To reverse the string
    return new_num

def getHash(string):
    return int(int(hashlib.sha256(string.encode('utf-8')).hexdigest(), 16)**2)

def getSeed(n=1000):
    return ''.join([str(SRandInt(0, 9)) for I in range(n)])

def add_passDict_to_passFile(passDict, passFile):
    index = max([int(k) for k in passFile['passwords'].keys()]) + 1 if len(passFile['passwords'].keys()) > 0 else 1
    passFile['passwords'][index] = passDict
    return passFile

def get_passFile(fileName='pass.json'):
    passFile = None
    seed=getSeed()
    if not os.path.isfile(fileName):
        with open(fileName, 'w') as f:
            json.dump({'seed': seed, 'passwords': {}}, f)
    with open(fileName, 'r') as f:
        passFile = json.load(f)
    return passFile

def DeletePassFile(fileName='pass.json'):
    if os.path.isfile(fileName):
        os.remove(fileName)
        return True
    else:
        return False

def add_to_passFile(passDicts=[], fileName='pass.json'):
    passFile        = get_passFile(fileName)    
    for passDict in passDicts:
        passFile = add_passDict_to_passFile(passDict, passFile)

    with open(fileName, 'w') as f:
        json.dump(passFile, f)
    return passFile

def create_pwd_dict(username, website, special_chars=False, length=14):
    return {'username': username, 'website': website, 'length': length, 'special_chars': special_chars}

def get_password(index, passFile, website=None, username=None):
    if type(index) is int:
        index = str(index)
    username, website, seed = passFile['passwords'][index]['username'], passFile['passwords'][index]['website'], passFile['seed']
    hStr = username + website + str(index) + str(getHash(seed)) + seed + seed[::-1]
    return dec_to_base(getHash(hStr), special_chars=passFile['passwords'][index]['special_chars'])[:passFile['passwords'][index]['length']]

def passFile_to_list(passFile, website=None):    
    if website is None:
        return [[passFile['passwords'][k]['website'] , passFile['passwords'][k]['username'],get_password(k, passFile)] for k in passFile['passwords'].keys()]
    l = passFile_to_list(passFile)
    return [i for i in l if website in i[0]]

def get_login_list(passFile, website=None):    
    if website is None:
        return [[passFile['passwords'][k]['website'] , passFile['passwords'][k]['username'], k] for k in passFile['passwords'].keys()]
    l = get_login_list(passFile)
    return [i for i in l if website in i[0]]

def get_password_for_website(website, passFile=None):
    if passFile is None:
        passFile = get_passFile()
    return passFile_to_list(passFile=passFile, website=website)


def delete_password(index, passFile):
    del passFile['passwords'][index]
    return passFile

def save_passFile(passFile, fileName='pass.json'):
    with open(fileName, 'w') as f:
        json.dump(passFile, f)
    return True