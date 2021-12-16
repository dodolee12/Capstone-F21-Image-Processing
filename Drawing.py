from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
import drawfile
from send_commands_through_bluetooth import send_coordinates, address
import asyncio
from kivy.core.window import Window
Window.size = (500, 700)
Window.clearcolor = (1, 1, 1, 1)

class MyPaintWidget(Widget):
    def __init__(self):

        self.down_x = 0
        self.down_y = 0
        super().__init__()

    def on_touch_down(self, touch):
        if (touch.x < 0 or touch.x > 500 or touch.y < 0 or touch.y > 600): return
        with self.canvas:
            Color(0,0,0)
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            self.down_x = touch.x
            self.down_y = touch.y
            f = open('out.log', 'a')
            f.write("pen down\n")
            f.write("({},{})\n".format(round(touch.x), round(touch.y)))

    def on_touch_move(self, touch):
        if (touch.x < 0 or touch.x > 500 or touch.y < 0 or touch.y > 600): return
        touch.ud['line'].points += [touch.x, touch.y]
        f = open('out.log', 'a')
        f.write("({},{})\n".format(round(touch.x), round(touch.y)))
        print(touch.x, touch.y)

    def on_touch_up(self, touch):
        if (touch.x < 0 or touch.x > 500 or touch.y < 0 or touch.y > 600): return
        if(pow(touch.x - self.down_x,2) + pow(touch.y - self.down_y,2) > 20):
            print('ok')
            return

        with self.canvas:
            Color(0,0,0)
            d = 10.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            f = open('out.log', 'a')
            f.write("pen up\n")
            f.write("({},{})\n".format(round(touch.x), round(touch.y)))
            print(touch.x, touch.y)

class MyPaintApp(App):

    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()

        # clear btn
        clearbtn = Button(text='Clear', pos =(300, 600))
        clearbtn.bind(on_release=self.clear_canvas)

        # send button
        sendbtn = Button(text='Sendout', pos = (400, 600))
        sendbtn.bind(on_release=self.send_out)

        l = Label(text='[b]Triple Tangent \n Project 2022[/b]', markup=True, font_size=30, color=(0,0,0), pos=(100,600))


        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(sendbtn)
        parent.add_widget(l)


        self.clear_canvas("obj")

        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        out_log = open("out.log", "w")
        out_log.truncate()
        out_log.close()

    def send_out(self,obj):
        print('hello')
        #drawfile.plot_file()
        # need to work logic here
        f = open('out.log', 'r')
        commands = ["Start"]
        for i in f.readlines():
            if i.strip() == 'pen down' or i.strip() == 'pen up':
                commands.append("Lift Pen")
                continue
            a = i.strip("\n()").split(",")
            x = int(a[0])
            y = int(a[1])
            commands.append(str((3*x,3*y)))
        commands.append("Finish")
        print(commands)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_coordinates(address, commands))
        f.close()
        self.clear_canvas("obj")

if __name__ == '__main__':
    out_log = open("out.log", "w")
    out_log.truncate()
    out_log.close()
    MyPaintApp().run()