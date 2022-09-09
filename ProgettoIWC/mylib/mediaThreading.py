from datetime import datetime
from threading import Thread, Timer, Event


class MyTimer():

    def __init__(self, nTime=1, func=None, bVerbose=False):

        ''' nTime: delay between one execution of the timer and the next one '''
        ''' func: is the function that the timer repeat every n second '''
        ''' nTime = delay between one execution of the timer and the next one '''

        self.nTime, self.func, self.bVerbose = nTime, func, bVerbose
        self.timer_run = False

        ''' initialize the class timer of the library threading '''

        self.thread = Timer(self.nTime, self.exec_funct)

    def start_timer(self):

        try:

            if self.timer_run:
                self.sError = "Timer alredy start"
                return -1

            self.timer_run = True
            self.thread.start()

        except Exception as inst:

            self.sError = inst
            return -1

        return 0

    def exec_funct(self):

        try:

            if self.bVerbose:
                print("Exec timer in:", datetime.now())

            ''' Stop the timer before execute the function pass to the timer '''

            self.thread.cancel()

            ''' Execute the main function of the timer '''

            self.func()

            ''' Re-create and start the timer '''

            self.thread = Timer(self.nTime, self.exec_funct)
            self.thread.start()

        except Exception as inst:

            if self.bVerbose:
                print(inst)

    def stop_timer(self):

        try:

            if not self.timer_run:
                self.sError = "Timer alredy Stop"
                return -1

            self.thread.cancel()
            self.timer_run = False

        except Exception as inst:

            self.sError = inst
            return -1

        return 0

    def get_last_error(self):

        ''' Return the last error that the class make '''
        return self.sError

