
#!/usr/bin/env python
from wavebender import *
from io import BytesIO
from pygame import mixer
from getch import getch

from scale import scale
scale = {str(n):n.frequency for n in scale}
print(scale)

# gameplay settings. Sets the lowest octave, highest octave and whether to include flat notes.
# possible octaves go from 0 to 10 but they are kinda broken below 4 and above 6
bottomOctave = 5
topOctave = 5
usingAccidentals = False

playTone={}
mixedScale ={}

def generate_tone(tone,amplitude=0.5):
    # simulates a violin playing G.
    channels = ((damped_wave(tone, amplitude=0.76*amplitude, length=44100 * 5),
           ),)

    samples = compute_samples(channels, 44100)


    foo = BytesIO()
    write_wavefile(foo, samples, 1, nchannels=1)
    foo.seek(0)
    soundblob = mixer.Sound(foo)
    del foo
    return soundblob

def getUserInput(tone):
    userGuess = getch()
    if userGuess.lower() == tone[0].lower():
        print("Yay! It was {}, {}, ".format(tone,scale[tone])),
        playTone[tone]()
        return('correct')
    elif userGuess.lower() == 'r':
        playTone[tone]()
        return(getUserInput(tone))
    elif userGuess.lower() == 'q':
        print("bye~")
        return('quit')
    else:
        #print("nope, it was {}, {},".format(tone,scale[tone])),
        playTone[userGuess.upper()+"5"]()
        return(getUserInput(tone))
        #return('incorrect')

def appendStatus(tone,correct,left,guesses):
    #playTone[tone]()
    print("   {0} correct, {1} left, {2} guesses".format(correct,left,guesses))
    time.sleep(1)

def addToneToScales(tone):
    if tone in scale:
        mixedScale[tone] = generate_tone(scale[tone])
        playTone[tone] = mixedScale[tone].play
        print("{}".format(tone))
        playTone["{}".format(tone)]()

import time
import random
from datetime import datetime
def startGame():
    mixer.init()


    for octave in range(bottomOctave,topOctave+1):
        for key in ['C','D','E','F','G','A','B',]:
            if usingAccidentals:
                addToneToScales("{}{}{}".format(key,octave,'b'))
            addToneToScales("{}{}".format(key,octave))

    playing = True
    while playing:
        log = open("stats.csv",'a')
        gameScale = [key for key in mixedScale]
        correct=0
        guesses=0
        while playing and len(gameScale)>0:
            tone = random.choice(gameScale)
            playTone[tone]()

            userInput = getUserInput(tone)

            if userInput == 'correct':
                gameScale.remove(tone)
                correct+=1
                guesses+=1
                appendStatus(tone,correct,len(gameScale),guesses)
            elif userInput == 'incorrect':
                guesses+=1
                appendStatus(tone,correct,len(gameScale),guesses)
            elif userInput == 'quit':
                playing=False
                break

        if playing:
            log.write("{},{},{}\n".format(datetime.now(),correct,guesses))
            print("A winner is you!")
    log.close()
        

if __name__ == "__main__":
    startGame()
