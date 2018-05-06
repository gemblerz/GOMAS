import time
from tkinter import Tk, Label, StringVar

from utils.rmq import RmqSubscriber
from agent import GorasAgent


class GorasLogger(GorasAgent):
    def __init__(self):
        super().__init__(need_ears=True, what_to_hear='log')
        self.history_path = '/tmp/simulation.history'

    def terminate(self):
        super().terminate()

    def run(self):
        context = Tk()
        label_text = StringVar()
        label = Label(context, textvariable=label_text)
        label.pack()

        with open(self.history_path, 'w') as log:
            while not self.time_to_exit.is_set():
                sentence = self.hear()
                if sentence is not None:
                    print('fuck')
                    print(sentence)
                    sender = sentence.speaker
                    when = sentence.when
                    if sentence.HasField('inform'):
                        formatted = '[%f] %s %s %s\r\n' % (
                            when,
                            sentence.inform.subject,
                            sentence.inform.verb,
                            sentence.inform.object)
                    log.write(formatted)
                    label_text.set(formatted)
                    log.flush()
                else:
                    time.sleep(0.1)
                context.update_idletasks()
                context.update()
