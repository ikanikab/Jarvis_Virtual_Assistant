import multiprocessing
import keyboard
import sys
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

def shutdown_listener(p1, p2):
    keyboard.wait('q')
    print("Q pressed → shutting down system")

    if p1.is_alive():
        p1.terminate()
    if p2.is_alive():
        p2.terminate()

    print("System stopped")
    sys.exit(0)


# start the process
if __name__ == '__main__':
    p1 = multiprocessing.Process(target = startJarvis)
    p2 = multiprocessing.Process(target = listenHotWord)
    p1.start()
    p2.start()
    shutdown_listener(p1, p2)