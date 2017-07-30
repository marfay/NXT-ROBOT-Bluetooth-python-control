from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib.pyplot as plt
import socket,sys

from kivy.graphics import *
#from kivy.core.window import Window
import numpy as np
import threading
import pickle
from kivy.clock import Clock
import testt
import bluetooth
from nxt.bluesock import BlueSock
import nxt.bluesock as bb
import nxt.motor as m
import bluetooth
import nxt.brick
import nxt.locator
import threading
import time


class MainWindow(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.MY_BRICK_ID='00:16:53:13:C6:DE'
        self.start=time.time()
        self.count=0
        global xx
        xx=5

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):

            if ((touch.x-self.ids.sm1.x)>self.ids.display.x and (touch.x-self.ids.sm1.x) < (self.ids.display.x+self.ids.display.width)) and ((touch.y-self.ids.sm1.y) > self.ids.display.y and (touch.y-self.ids.sm1.y) < (self.ids.display.y + self.ids.display.height)):
                #self.ids.textt.text=str(touch.x)+' '+str(touch.y)
                if self.ids.sm1.current == 'control':  # Pokud je otevreno platno - Control stranka
                    #print(self.ids.sm1.current)

                    self.draw_vector_x_y(touch.x,touch.y)
        print('STLACENO')
        return super(MainWindow, self).on_touch_down(touch)

    def on_touch_move(self, touch):

        if self.collide_point(touch.x, touch.y):

            if ((touch.x - self.ids.sm1.x) > self.ids.display.x and (touch.x - self.ids.sm1.x) < (
                self.ids.display.x + self.ids.display.width)) and (
                    (touch.y - self.ids.sm1.y) > self.ids.display.y and (touch.y - self.ids.sm1.y) < (
                self.ids.display.y + self.ids.display.height)):
                #self.ids.textt.text = str(touch.x) + ' ' + str(touch.y)
                if self.ids.sm1.current == 'control':  # Pokud je otevreno platno - Control stranka
                    #print(self.ids.sm1.current)

                    self.draw_vector_x_y(touch.x,touch.y)
        return super(MainWindow, self).on_touch_down(touch)

    def draw_vector_x_y(self, touchX,touchY):

        global power_LEFT,power_RIGHT
        display = self.ids.display
        display.canvas.clear()

        centerX = display.width / 2
        centerY = display.height / 2

        posX = touchX - self.ids.sm1.x - self.ids.display.x  # display.x = 0
        posY = touchY - self.ids.sm1.y - display.y

        ##
        self.xt = posX - centerX
        self.yt = posY - centerY

        vector_x_y = np.sqrt((self.xt ** 2) + (self.yt ** 2))


        self.uhel = 1
        if self.xt >= 0 and self.yt >= 0: ## kvadrant 1
            self.uhel = np.arcsin(-self.yt / vector_x_y) * (-180) / np.pi
        if self.xt >= 0 and self.yt <= 0: #kvadrant 3
            self.uhel = 360 - np.arcsin(self.yt / vector_x_y) * (-180) / np.pi
        if self.xt <= 0 and self.yt < 0: #kvadrant 4
            self.uhel = 180 + np.arcsin(self.yt / vector_x_y) * (-180) / np.pi
        if self.xt <= 0 and self.yt > 0:    #kvadrant 2
            self.uhel = 180 - np.arcsin(self.yt / vector_x_y) * 180 / np.pi
        # UHEL zacina 3. hodinou a toci se proti smeru hodinovych rucicek, to znamena, ze 270 stupnu je v 6 hodin
        #print(self.uhel)


        try:
            freq = round(self.uhel, 2)  # neni treba
            #self.ids.vel.text = str(freq / 15)  # neni treba
        except:
            pass

        # threading.Thread(target=MainWindow.connecting(self, HOSTNAME), kwargs={'HOSTNAME': HOSTNAME})

        if self.ids.display.width >= self.ids.display.height:
            fix_r = self.ids.display.height / 3.5
        if self.ids.display.width <= self.ids.display.height:
            fix_r = self.ids.display.width / 3.5

        self.count += 1
        if self.count == 100:
            print('FPS: ' + str(self.count / (time.time() - self.start)))
            self.count = 0
            self.start = time.time()

        power = round(100 * vector_x_y / fix_r, 2)

        if power > 100:
            power = 100
        if power < -100:
            power = -100

        if self.yt <= 0:
            power = -power

        if self.xt >= 0 and self.yt >= 0:  ## kvadrant 1
            vector_u = self.xt / np.cos(self.uhel * np.pi / 180)
            self.xtp = (fix_r * np.cos(self.uhel * np.pi / 180))
            if self.xt >= self.xtp:
                self.xt = self.xtp
        if self.xt <= 0 and self.yt > 0:  # kvadrant 2
            vector_u = (self.xt / np.cos(180 * np.pi / 180 - self.uhel * np.pi / 180))
            self.xtp = (fix_r * np.cos(180 * np.pi / 180 - self.uhel * np.pi / 180))
            if self.xt >= self.xtp:
                self.xt = self.xtp
        if self.xt <= 0 and self.yt < 0:  # kvadrant 3
            vector_u = (self.xt / np.cos(self.uhel * np.pi / 180 - np.pi))
            self.xtp = (fix_r * np.cos(self.uhel * np.pi / 180 - np.pi))
            if self.xt >= (self.xtp):
                self.xt = self.xtp
        if self.xt >= 0 and self.yt <= 0:  # kvadrant 4
            vector_u = self.xt / np.cos(360 * np.pi / 180 - self.uhel * np.pi / 180)
            self.xtp = (fix_r * np.cos(360 * np.pi / 180 - self.uhel * np.pi / 180))
            if self.xt >= self.xtp:
                self.xt = self.xtp
        if self.xt >= self.xtp:
            self.xt = self.xtp

        # print(self.xt,self.xtp)
        power_x = round(100 * self.xt / fix_r, 2)

        if power_x >= 100:
            power_x = 100
        if power_x <= -100:
            power_x = -100

        ## MOTORS Mechanics+
        if self.yt >= 0:
            if power_x >= 0:
                power_LEFT = power
                power_RIGHT = power - power_x

            if power_x <= 0:
                power_LEFT = power + power_x
                power_RIGHT = power
        if self.yt < 0:
            if power_x >= 0:
                power_LEFT = power
                power_RIGHT = power + power_x

            if power_x <= 0:
                power_LEFT = power - power_x
                power_RIGHT = power

        power_LEFT = round(power_LEFT, 2)
        power_RIGHT = round(power_RIGHT, 2)
        ##################### CONTROL LOGIC - THROUGH GRAPHICS #######################\
        #print(power_LEFT,power_RIGHT)
        self.draw_screen(display,centerX,centerY,fix_r,posX,posY)

    def draw_screen(self,display,centerX,centerY,fix_r,posX,posY):
        with display.canvas:

            bar_weight=0.15
            bar_relative_pos=0.8
            Rectangle(pos=(centerX-abs(centerX*bar_relative_pos),centerY),size=(centerX*bar_weight,(float(power_LEFT/100))*fix_r))
            Rectangle(pos=(centerX +abs(centerX * (bar_relative_pos-bar_weight)), centerY),size=(centerX * bar_weight, (float(power_RIGHT / 100)) * fix_r))

            #positions
            xleft=centerX-abs(centerX*bar_relative_pos)
            xright=centerX +abs(centerX * (bar_relative_pos-bar_weight))
            b_width = centerX*bar_weight
            b_height = fix_r
            Line(points=[xleft, centerY-b_height, xleft, centerY+b_height,xleft+b_width,centerY+b_height,xleft+b_width,centerY-b_height], width=0.5, close=True, joint='round')
            Line(points=[xright, centerY-b_height, xright, centerY+b_height,xright+b_width,centerY+b_height,xright+b_width,centerY-b_height], width=0.5, close=True, joint='round')

            #### END OF POWER MOTORS MECHANICHS
            z=[]
            widget3=Label(text='[b]' + 'Power ' + str(round(power_LEFT, 1)) + ' % ' + '[/b]', pos=(xleft*1.1,centerY+fix_r*1.1),
                            size=[1, 1],
                            font_size='16sp', markup=True)

            widget2 = Label(text='[b]' + 'Power ' + str(round(power_RIGHT, 1)) + ' % ' + '[/b]',
                            pos=(xright, centerY + fix_r * 1.1),
                            size=[1, 1],
                            font_size='16sp', markup=True)

            widget4 = Label(text='[b]' + 'Forward ' + '[/b]',
                            pos=(centerX, centerY + fix_r * 1.1),
                            size=[1, 1],
                            font_size='20sp', markup=True)

            widget5 = Label(text='[b]' + 'Backward ' + '[/b]',
                            pos=(centerX, centerY - fix_r * 1.1),
                            size=[1, 1],
                            font_size='20sp', markup=True)

            z.append([widget2,widget3,widget4,widget5])

            self.z = z




            Color(0, 0, 0, 0)
            Rectangle(pos=(0, 0), size=display.size)

            Color(1, 1, 1, 1)
            Line(points=[centerX, centerY, posX, posY], width=1.3, close=True, joint='round')

            Color(1, 1, 1, 1)
            Line(circle=(centerX, centerY, fix_r * 1.01, 0, 360), width=1.3)
            Line(circle=(centerX, centerY, fix_r * 0.53, 0, 360), width=0.9)

            #Line(points=[centerX, centerY, centerX, centerY + fix_r], width=0.5, close=True, joint='round')
            Line(points=[centerX, centerY, centerX + fix_r, centerY], width=0.5, close=True, joint='round')
            Line(points=[centerX, centerY, centerX - fix_r, centerY], width=0.5, close=True, joint='round')


            ##### LABELS IN THE CIRCLES PUSHMATRIX a POPMATRIX zapricini ze prikaz rotace se neuplatni v celem canvas ale jen mezi temito dvema prikazy
            z = []
            PushMatrix()
            r = Rotate()
            r.angle = 0

            widget = Label(text='[b]' + 'Puls' + '[/b]', pos=[centerX, centerY - fix_r * 0.7], size=[1, 1],
                           font_size='20sp', markup=True, )
            z.append(widget)
            PopMatrix()

            global xx


            Color(3 / 255, 152 / 255, 1, 0.5)

            # Color(1, 1, 1, velocity / fix_r)
            #Ellipse(
            #    pos=(0 - fix_r + self.ids.display.width / 2, 0 - fix_r + self.ids.display.height / 2),
            #    size=(fix_r * 2, fix_r * 2),
            #    angle_start=0, angle_end=xx)



            # PushMatrix()
            # r = Rotate()
            # r.angle = 45 / 2 - 90
            # pozice = [float(round(centerX + np.cos((45 / 2) * np.pi / 180) * fix_r * 0.7, 2)),
            #          float(round(centerY + np.sin((45 / 2) * np.pi / 180) * fix_r * 0.7, 2))]
            ## print(type(float(pozice[0])))
            # r.origin = pozice
            # widget2 = Label(text='[b]' + 'False' + '[/b]', pos=pozice, size=[1, 1],
            #                font_size='20sp', markup=True)
            # z.append(widget2)
            # PopMatrix()





    def start_motors(self):
        threading.Thread(target=self.motor_instructions).start()

    def motor_instructions(self):
        while True:
            self.motorA.run(power_LEFT)
            self.motorB.run(power_RIGHT)
            time.sleep(0.05)

    def on_touch_up(self, touch): ## Automaticky vrati polohu mysi do stredu obrazovky
        if self.ids.sm1.current == 'control':
            display=self.ids.display
            centerX = display.width / 2
            centerY = display.height / 2
            self.draw_vector_x_y(centerX,centerY)


    def STOP(self):
        self.motorA.run(0)

        self.motorB.run(0)

    def thread_connect(self):
        threading.Thread(target=self.connect).start()

    def connect(self):
        self.connect_constant = True
        threading.Thread(target=self.connecting_wait).start()
        try:
            BRICK_ID = str(self.ids.id_for_bluetooth.text) # read from TextInput
            print(BRICK_ID)
            self.sock=BlueSock(BRICK_ID)
            self.brick = self.sock.connect()
            self.motorA = m.Motor(self.brick, m.PORT_A)
            self.motorB = m.Motor(self.brick, m.PORT_B)
            print('Connected')
            self.connect_constant = False
        except:
            self.connect_constant = False
            print('Not Connected')
    def connecting_wait(self):
        while self.connect_constant == True:
            print('jsem tu',self.ids.pb_con.value)

            self.ids.pb_con.value += 1
            if self.ids.pb_con.value >= 99:
                self.ids.pb_con.value=0
            time.sleep(0.01)
        self.ids.pb_con.value = 0

    def function_jump(self):
        try:
            self.motorA.run(-100)
            self.motorB.run(-100)
            time.sleep(0.12)
            self.motorA.run(100)
            self.motorB.run(100)
        except:
            pass

    def disconnect(self):
        self.sock.close()
        print('Disconnected')



    def discovering_wait(self):
        while self.discover_constant == True:
            self.ids.pb_discover.value += 1
            if self.ids.pb_discover.value >= 99:
                self.ids.pb_discover.value=0
            time.sleep(0.01)
        self.ids.pb_discover.value = 0

    def dis_dev(self):
        self.discover_constant = True
        threading.Thread(target=self.discover_devices).start()

    def discover_devices(self):
        threading.Thread(target=self.discovering_wait).start()
        try:
            list_of_devices = {}
            names_of_devices=[]
            x = bluetooth.discover_devices()
            for i in x:
                i_name=bluetooth.lookup_name(i)

                list_of_devices[str(i_name)]=i
                names_of_devices.append(i_name)
                self.ids.devices.values=names_of_devices
            print(list_of_devices)
            self.discover_constant = False

            ### List of devices
            self.DEVICES = list_of_devices
            self.ids.devices.text = names_of_devices[0]

        except:
            print('Nenalezeny, zkuste se pripojit zarizenim k robotu a pote az pres GUI')
            self.discover_constant = False
    def set_device_id(self):
        ### corresponding ID to its name from Dictionary
        try:
            ID_FROM_THE_LIST = self.DEVICES[self.ids.devices.text]
            self.ids.id_for_bluetooth.text = ID_FROM_THE_LIST
        except:
            pass

    def sensor_ultrasonic(self):
        #self.Four=nxt.get_sensor(self.brick,nxt.PORT_4)
        #self.Three=nxt.sensor.Sound(self.brick,nxt.PORT_3)
        #self.Two = nxt.get_sensor(self.brick, nxt.PORT_2)
        #self.One=nxt.get_sensor(self.brick,nxt.PORT_1)
        #self.One=nxt.sensor.Touch(self.brick,nxt.PORT_1)
        threading.Thread(target=self.get_distance).start()
        #Clock.unschedule(self.update)
        #Clock.schedule_interval(self.get_distance, 1.0 / 1.0)

    def get_distance(self):
        One=nxt.sensor.HTGyro(self.brick,nxt.PORT_4)
        Two = nxt.Sound(self.brick,nxt.PORT_1)
        print(Two)
        global xx
        while True:
            print(One.get_rotation_speed())


class guiApp(App):
    pass
if __name__ == '__main__':
    guiApp().run()
