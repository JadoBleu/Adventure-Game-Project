'''clear screen and rng generator'''
# Imports
import random, subprocess, platform


def clear_screen():
    ''' Clear the screen'''
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate() #I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine 
    else: #Linux and Mac
        print("\033c", end="")

def rng(dividend=50, divisor=100):
    '''Calculate the chance of activation randomly
    * returns boolean'''
    result = random.randint(0, divisor)
    return bool(result < dividend)
