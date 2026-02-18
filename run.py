import multiprocessing
import os
import eel
# Entry point, spawns two processes: Jarvis (main) + hotword detection

# to run jarvis
def startJarvis():
    print("Process 1 is running")
    from main import start
    start()

#to run hotword
def listenHotWord():
    print("Process 2 is running")
    from engine.features import hotWord
    hotWord()

# start the process
if __name__ == '__main__':
    p1 = multiprocessing.Process(target = startJarvis)
    p2 = multiprocessing.Process(target = listenHotWord)
    p1.start()
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()
    
    print("system stop")