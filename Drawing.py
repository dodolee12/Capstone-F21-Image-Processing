from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
import drawfile


class MyPaintWidget(Widget):
    def __init__(self):

        self.down_x = 0
        self.down_y = 0
        super().__init__()

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            self.down_x = touch.x
            self.down_y = touch.y
            f = open('out.log', 'a')
            f.write("pen down\n")
            f.write("{}, {} \n".format(round(touch.x), round(touch.y)))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        f = open('out.log', 'a')
        f.write("{}, {} \n".format(round(touch.x), round(touch.y)))
        print(touch.x, touch.y)

    def on_touch_up(self, touch):
        if(pow(touch.x - self.down_x,2) + pow(touch.y - self.down_y,2) > 20):
            print('ok')
            return

        with self.canvas:
            Color(1, 1, 0)
            d = 10.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            f = open('out.log', 'a')
            f.write("pen up\n")
            f.write("{}, {} \n".format(round(touch.x), round(touch.y)))
            print(touch.x, touch.y)

class MyPaintApp(App):

    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()

        # clear btn
        clearbtn = Button(text='Clear', pos =(200, 0))
        clearbtn.bind(on_release=self.clear_canvas)

        # send button
        sendbtn = Button(text='Sendout', pos = (100, 0))
        sendbtn.bind(on_release=self.send_out)

        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(sendbtn)

        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        out_log = open("out.log", "w")
        out_log.truncate()
        out_log.close()

    def send_out(self,obj):
        print('hello')
        drawfile.plot_file()
        # need to work logic here

if __name__ == '__main__':
    MyPaintApp().run()