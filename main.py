import tkinter
import threading
import queue
from digi.xbee.devices import XBeeDevice
import time

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM7"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

class ReadData(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q;

    def run(self):
        print(" +-----------------------------------------+")
        print(" | XBee Python Library Receive Data Sample |")
        print(" +-----------------------------------------+\n")

        device = XBeeDevice(PORT, BAUD_RATE)
        try:
            device.open()
            device.flush_queues()

            print("Waiting for data...\n")

            while True:
                xbee_message = device.read_data()  # 데이터 읽기
                if xbee_message is not None:
                    data_receive = xbee_message.data.decode()
                    print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(), data_receive))
                    self.q.put(data_receive)  # 큐에 받은 데이터 삽입
                    time.sleep(1)

        finally:
            if device is not None and device.is_open():
                device.close()

class GUI(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

        self.q=queue.Queue(10)
        self.geometry("600x300+100+100")
        self.resizable(False,False)
        self.title("RGB Sensing Device")
        self.imageTitle = tkinter.PhotoImage(file="rgb_title.png")
        self.labelTitle = tkinter.Label(self, image=self.imageTitle)
        self.labelTitle.pack(side="top")
        self.imageLogo = tkinter.PhotoImage(file="rgb_img.png")
        self.labelLogo = tkinter.Label(self, image=self.imageLogo)
        self.labelLogo.place(x=45, y=80)
        self.textCCT = tkinter.Label(self, text="CCT")
        self.textLux = tkinter.Label(self, text="LUX")
        self.textR = tkinter.Label(self, text="R")
        self.textG = tkinter.Label(self, text="G")
        self.textB = tkinter.Label(self, text="B")
        self.textCCT.place(x=290, y=90)
        self.textLux.place(x=450, y=90)
        self.textR.place(x=280, y=190)
        self.textG.place(x=380, y=190)
        self.textB.place(x=480, y=190)

        self.valueCCT = tkinter.Label(self, borderwidth=5, width=10, text="cct")
        self.valueCCT['fg'] = '#0000ff'
        self.valueCCT.place(x=265, y=120)

        self.valueLux = tkinter.Label(self, borderwidth=5, width=10, text="lux")
        self.valueLux['fg'] = '#0000ff'
        self.valueLux.place(x=425, y=120)

        self.valueR = tkinter.Label(self, borderwidth=5, width=10, text="r")
        self.valueR['fg'] = '#0000ff'
        self.valueR.place(x=245, y=220)

        self.valueG = tkinter.Label(self, borderwidth=5, width=10, text="g")
        self.valueG['fg'] = '#0000ff'
        self.valueG.place(x=345, y=220)

        self.valueB = tkinter.Label(self, borderwidth=5, width=10, text="b")
        self.valueB['fg'] = '#0000ff'
        self.valueB.place(x=445, y=220)

        self.button=tkinter.Button(self,text="start",command=self.start_thread)
        self.button.place(x=100, y=230)


    def start_thread(self):
        ReadData(self.q).start()
        self.after(0,self.read_queue)

    def read_queue(self):
        try:
            data_queue = self.q.get(0);
            data_split = data_queue.split(',')
            cct = data_split[0]
            lux = data_split[1]
            r = data_split[2]
            g = data_split[3]
            b = data_split[4]
            self.valueCCT=tkinter.Label(self, borderwidth=5, width=10, text=cct)
            self.valueCCT['fg'] = '#0000ff'
            self.valueCCT.place(x=265, y=120)
            self.valueLux=tkinter.Label(self, borderwidth=5, width=10, text=lux)
            self.valueLux['fg'] = '#0000ff'
            self.valueLux.place(x=425, y=120)
            self.valueR=tkinter.Label(self, borderwidth=5, width=10, text=r)
            self.valueR['fg'] = '#0000ff'
            self.valueR.place(x=245, y=220)
            self.valueG=tkinter.Label(self, borderwidth=5, width=10, text=g)
            self.valueG['fg'] = '#0000ff'
            self.valueG.place(x=345, y=220)
            self.valueB=tkinter.Label(self, borderwidth=5, width=10, text=b)
            self.valueB['fg'] = '#0000ff'
            self.valueB.place(x=445, y=220)

        except queue.Empty:
            # It's ok if there's no data to read.
            # We'll just check again later.
            pass
            # Schedule read_queue again in one second.
        finally:
            self.after(1000, self.read_queue)

root=GUI()
root.mainloop()