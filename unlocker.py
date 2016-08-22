import pyautogui as pyg
import os
import time
import base64
from Crypto.Cipher import XOR
from simplecrypt import encrypt, decrypt

# Utilities
def encrypt(key, plaintext):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(key, ciphertext):
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext))


# Program Functions
def unlock(intended_use=''):
    if(intended_use == 'Master'):
        print("Move mouse to upper-right-hand-corner to begin entering master password")
    elif(intended_use == 'Generate'):
        print("Move mouse to upper-right-hand corner to begin listening to mouse, then move it around randomly to generate a random password.")
    else:
        print("Move mouse to upper-right-hand corner to begin listening to mouse.")
    listening = False
    
    while not listening:
        current_pos = pyg.position()
        if current_pos[0] == 0 and current_pos[1] == 0:
            listening = True
            
    prevpos = (0,0)
    all_positions = list()
    wasnt_there = True
    
    while listening:
        current_pos = pyg.position()
        if current_pos == prevpos and wasnt_there:
            all_positions.append(current_pos)
            wasnt_there = False
            if(intended_use == 'Generate'):
                time.sleep(0.01)
            else:
                print('Ding')
                time.sleep(1)
        elif current_pos != prevpos and wasnt_there == False:
            wasnt_there = True
        if current_pos[0] == 0 and current_pos[1] == 0 and wasnt_there:
            break
        prevpos = current_pos

    if(intended_use == 'Master'):
        print("Done listening to mouse. Quadrantizing it now.")
        quad = list()
        for position in all_positions:
            endval = [99,99]
    
            #Separate the entries into quadrants
            for x in range(2):
                if(position[x] <= (pyg.size()[x]) / 3):
                     endval[x] = 0
                elif(position[x] <= (pyg.size()[x]) * 2 / 3):
                    endval[x] = 1
                else: endval[x] = 2
            quad.append(endval)
    
        quadstring = ''.join(map(str,quad)).replace('[','').replace(']','').replace(' ','').replace(',','').replace('(','').replace(')','') # Sorry, I am writing this late at night and can't be bothered to write a better way to do this.

        return base64.b64encode(quadstring.encode('ascii')).decode('utf-8').replace('M','').encode('ascii')[:32] # Same as above comment.
    else:
        all_positions = ''.join(map(str,all_positions)).replace('[','').replace(']','').replace(' ','').replace(',','').replace('(','').replace(')','') # Sorry, I am writing this late at night and can't be bothered to write a better way to do this.
        return base64.b64encode(all_positions.encode('ascii')).decode('utf-8').replace('M','').encode('ascii') # Same as above comment.




master_pass = ''
quit = False

def generatePassword():
    if(master_pass != ''):
        size = input("How big do you want the password: ")
        intended_site = input("What site is it for: ")
        with open('encrypted_passwords', 'a') as password_file:
            password_file.write(encrypt(master_pass, unlock('Generate').decode('utf-8')[:int(size)] + ' ' + intended_site).decode('utf-8'))
    else:
        print("You haven't entered the Master Password yet!")

def decodePasswords():
    if(master_pass != ''):
        with open('encrypted_passwords', 'r') as password_file:
            for line in password_file:
                if line[0] != '#':  # Allowing comments of the password file. Probably a bad idea, but I'm doing it anyways.
                    print(decrypt(master_pass, line.rstrip()))
                else:
                    print(line.rstrip())
        input("Press Enter to return to the main menu.")
    else:
        input("You haven't entered the Master Password yet! Press Enter to return to the main menu.")

os.system('clear')
print("Welcome to Keychain.")
while(quit != True):
    os.system('clear')
    print("Please select what you want to do.\n")
    print(" 1. Enter Master Password\n 2. Unlock passwords\n 3. Generate new password\n 4. Quit Keychain\n")
    user_selection = input("Please select: ")
    if(user_selection == '1'):
        master_pass = unlock('Master')
    elif(user_selection == '2'):
        decodePasswords()
    elif(user_selection == '3'):
        generatePassword()
    elif(user_selection == '4'):
        print("Thanks for using Keychain! Have a nice day!")
        quit = True
    else: 
        print("That was not a valid selection. Please choose between 1, 2, 3, or 4.")
