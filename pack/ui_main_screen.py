import kivy.uix.widget as widget
from kivy.graphics import Line
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

class NodeView(widget.Widget):
    def __init__(self, **kwargs):
        super(NodeView, self).__init__(**kwargs)
        self.__gridSize = 50
        self.__bgColor = '#191919'
        self.__lineColor = '#222222'
        self.__lineWidth = 2
        self.__defaultZoom = 1
        self.__currentZoom = 1
        self.__offset = [0,0]
        self.__delta_offset = [0,0]
        self.__lockView = False

        self.__nodeInstances = []
        self._selectedPin = None

        # 初始化加载
        self.render_frame()
        self.init_run()


    def init_run(self):
        from . import ui_node
        node = ui_node.NodeBase()
        node._parentView = self
        node.build()
        self.add_widget(node)
        self.__nodeInstances.append(node)

        node2 = ui_node.NodeBase()
        node2.pos = (200,200)
        node2._parentView = self
        node2.build()
        self.add_widget(node2)
        self.__nodeInstances.append(node2)


    def attr_set_lock(self, value):
        self.__lockView = value

    def attr_get_lock(self):
        return self.__lockView



    # 对每个子节点进行每帧处理
    def process_children(self):
        for node in self.__nodeInstances:
            node.render_frame()
            node.pos[0] += self.__delta_offset[0]
            node.pos[1] += self.__delta_offset[1]
            self.remove_widget(node)
            self.add_widget(node)



    # 每一帧渲染
    def render_frame(self):
        self.canvas.clear()
        with self.canvas:
            Color(*self.hexColor(self.__bgColor))
            Rectangle(pos=(0,0), size=(self.width,self.height))
            Color(*self.hexColor(self.__lineColor))
            x_offset = self.__offset[0] % self.__gridSize
            y_offset = self.__offset[1] % self.__gridSize
            for x in range(0, self.width, self.__gridSize):
                x = x % self.width + x_offset
                Line(points=[x ,0,x,self.height], width=self.__lineWidth)
            for y in range(0, self.height, self.__gridSize):
                y = y % self.height + y_offset
                Line(points=[0,y,self.width,y], width=self.__lineWidth)
            
            if 1:
                Label(text=f'{round(self.__offset[0],3)},{round(self.__offset[1],3)}', font_size=14, pos=(10,10))



    # 事件
    def on_touch_move(self, touch):
        if self.__lockView:
            return super().on_touch_move(touch)
        deltaMove = touch.dpos
        self.__offset[0] += deltaMove[0]
        self.__offset[1] += deltaMove[1]
        self.__delta_offset = deltaMove

        self.render_frame()
        self.process_children()
        
        return super().on_touch_move(touch)



    def hexColor(self, hexColor):
        if hexColor[0] == '#':
            hexColor = hexColor[1:]
        r=hexColor[0:2]
        g=hexColor[2:4]
        b=hexColor[4:6]
        return [int(r,16)/255,int(g,16)/255,int(b,16)/255,1]
