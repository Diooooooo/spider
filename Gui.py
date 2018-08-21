import tkinter

from Rabbitmq import RabbitMq
from concurrent.futures import ThreadPoolExecutor

display_info_text = 'Dio'
mq = RabbitMq()
chan = mq.channel()


def get_rabbitmq():
    chan.queue_declare(queue=mq.routing_key, durable=True)
    chan.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        global display_info_text
        display_info_text = str(body, 'utf-8')
        print(str(body, 'utf-8'))

    chan.basic_consume(callback, queue=mq.routing_key, no_ack=False)
    chan.start_consuming()


class FindLocation(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("出票分销Beta1.0版")
        self.root.wm_minsize(1000, 800)
        self.label = tkinter.Label(self.root, text=display_info_text, font='Helvetica 40', fg='#90A691')
        self.success_button = tkinter.Button(self.root, command=self.finished, font='Helvetica 20', text="出票成功",
                                             fg='white', bg='green',
                                             activeforeground='white', activebackground='#f17c67')
        self.error_button = tkinter.Button(self.root, command=self.finished, font='Helvetica 20', text="出票失败",
                                           fg='white', bg='red',
                                           activeforeground='white', activebackground='#90A691')
        self.next_button = tkinter.Button(self.root, command=self.next, font='Helvetica 20', text="下一条",
                                          fg='white', bg='#008573',
                                          activeforeground='black', activebackground='yellow')

    def gui_arrang(self):
        self.label.pack(fill=tkinter.X)
        self.success_button.pack(fill=tkinter.X, padx=100, ipady=4, ipadx=8, side=tkinter.LEFT)
        self.error_button.pack(padx=100, ipady=4, ipadx=8, side=tkinter.LEFT)
        self.next_button.pack(padx=100, ipady=4, ipadx=22, side=tkinter.LEFT)

    def finished(self):
        chan.stop_consuming()
        self.root.destroy()

    def next(self):
        global chan
        self.label.config(text=display_info_text, font='Helvetica 40', fg='#90A691')
        chan.basic_ack(True)

        chan.queue_declare(queue=mq.routing_key, durable=True)
        chan.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            global display_info_text
            display_info_text = str(body, 'utf-8')
            print(str(body, 'utf-8'))

        chan.basic_consume(consumer_callback=callback, queue=mq.routing_key, no_ack=False)

    def find_position(self):
        pass


def main():
    FL = FindLocation()
    FL.gui_arrang()
    tpe = ThreadPoolExecutor(3)
    tpe.submit(get_rabbitmq)
    tkinter.mainloop()


if __name__ == "__main__":
    main()
