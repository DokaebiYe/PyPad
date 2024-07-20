import kivy.uix.widget as widget
from kivy.uix import button,label
from kivy.graphics import Line,Rectangle,Color
from kivy.core.text import LabelBase
from kivy.uix.label import Label

class NodeBase(widget.Widget):
    def __init__(self, **kwargs):
        super(NodeBase, self).__init__(**kwargs)
        self._parentView = None
        self._size = [self.width,self.height]
        self._is_selected = False
        self._borderWidth = 3
        self._borderColorDefault = '#461b04'
        self._borderColorHover = '#ff930a'
        self._bgColor = '#191919'
        self._titleBarColor = '#222222'
        self._titleColor = '#ffffff'
        self._titleHeight = 30
        self._pinInterval = 15
        self._parentView = None
        self._titleTextInstance = None
        self._lock = False
        self._leftPins = {
            "str0":[1,2,3,4],
            "str1":"string",
            "args2":"int",
            "args3":"bool",
            "args4":"float",
            "args5":"list",
            "args6":"dict",
            "args7":"tuple",
            "args8":"set",
            "args9":"bytes",
            "args10":"object"
        }
        self._rightPins = {
            "o_str1":"string",
            "o_args2":"int",
            "o_args3":"bool",
            "o_args4":"float",
            "o_args5":"list",
            "o_args6":"dict",
            "o_args7":"tuple",
            "o_args8":"set",
            "o_args9":"bytes",
            "o_args10":"object",
            "o_args11":"None",
            "o_args12":["enum1","enum2",'enum3']
        }

        self._children = []
        self._pinSlots = {}

        self.render_frame()

    def attr_set_lock(self, value):
        self._lock = value

    def attr_get_lock(self):
        return self._lock


    def process_frame(self):
        for childData in self._children:
            child = childData[2]
            child.pos = (self.x+childData[0],self.y+childData[1])
            self.remove_widget(child)
            self.add_widget(child)
            if hasattr(child, 'render_frame'):
                child.render_frame()


    def render_frame(self):
        self.canvas.clear()
        with self.canvas:

            Color(*self.hexColor(self._borderColorDefault))
            # 边框选择
            if self._is_selected:
                Color(*self.hexColor(self._borderColorHover))

            Rectangle(pos=self.pos, size=(self.width,self.height))

            # 背景
            Color(*self.hexColor(self._bgColor))
            Rectangle(pos=(self.x+self._borderWidth,self.y+self._borderWidth), size=(self.width-self._borderWidth*2,self.height-self._borderWidth*2))

            # 标题
            Color(*self.hexColor(self._titleBarColor))
            Rectangle(pos=(self.x+self._borderWidth,self.y+self.height-self._titleHeight - self._borderWidth), size=(self.width-self._borderWidth*2,self._titleHeight))
        self.process_frame()


    def build(self):
        from . import ui_pin
        self.height = max(len(self._leftPins),len(self._rightPins)) * (20 + self._pinInterval) + self._titleHeight + self._borderWidth*2 + 50
        bottomHeight = 30
        # 左侧Pin
        self.width += 50
        tmp = 0
        for k,v in self._leftPins.items():
            textPos = (self.x +self._borderWidth,self.y+tmp*(20 + self._pinInterval) + bottomHeight)
            textIns = Label(text=f'{k} : {v}',pos=textPos,size=(20,20),halign='center',valign='middle')
            self.add_widget(textIns)
            self._children.append([textPos[0] - self.x, textPos[1] - self.y, textIns])
            tmp += 1
            self._pinSlots[f'left_{tmp}'] = [textPos,k,v]
            pinIns = ui_pin.PortBase()
            pinIns.pos = textPos
            self.add_widget(pinIns)
            self._children.append([textPos[0] - self.x, textPos[1] - self.y, pinIns])
            pinIns.type = v
            pinIns.name = k
            pinIns.direction = 'left'
            pinIns._node_parent = self
            pinIns._scene_parent = self._parentView
            pinIns.build()


        # 右侧Pin
        self.width += 50
        tmp = 0
        for k,v in self._rightPins.items():
            textPos = (self.x +self.width-self._borderWidth-20,self.y+tmp*(20 + self._pinInterval) + bottomHeight)
            textIns = Label(text=f'{k} : {v}',pos=textPos,size=(20,20),halign='center',valign='middle')
            self.add_widget(textIns)
            self._children.append([textPos[0] - self.x, textPos[1] - self.y, textIns])
            tmp += 1
            self._pinSlots[f'right_{tmp}'] = [textPos,k,v]
            pinIns = ui_pin.PortBase()
            pinIns.pos = textPos
            self.add_widget(pinIns)
            self._children.append([textPos[0] - self.x, textPos[1] - self.y, pinIns])
            pinIns.type = v
            pinIns.name = k
            pinIns.direction = 'right'
            pinIns._node_parent = self
            pinIns._scene_parent = self._parentView
            pinIns.build()

        self._titleTextInstance = Label(text='Node',pos=(self.x+self._borderWidth,self.y+self.height-self._titleHeight-self._borderWidth),size=(self.width-self._borderWidth*2,self._titleHeight),color=self.hexColor(self._titleColor),halign='center',valign='middle')
        self.add_widget(self._titleTextInstance)
        self._children.append([self._titleTextInstance.x - self.x, self._titleTextInstance.y - self.y, self._titleTextInstance])



    # 事件
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._is_selected = True
            self.render_frame()
            if self._parentView:
                self._parentView.attr_set_lock(True)
        else:
            if self._parentView and self._is_selected:
                self._is_selected = False
                self._parentView.attr_set_lock(False)
        return super(NodeBase, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self._is_selected and not self._lock:
            self.pos[0] += touch.dpos[0]
            self.pos[1] += touch.dpos[1]
        self.render_frame()
        return super().on_touch_move(touch)




    def hexColor(self, hexColor):
        if hexColor[0] == '#':
            hexColor = hexColor[1:]
        r=hexColor[0:2]
        g=hexColor[2:4]
        b=hexColor[4:6]
        return [int(r,16)/255,int(g,16)/255,int(b,16)/255,1]
