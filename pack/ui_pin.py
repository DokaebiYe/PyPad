import kivy.uix.widget as widget
from kivy.uix import button,label
from kivy.graphics import Line,Rectangle,Color
from kivy.core.text import LabelBase
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp



class PortBase(widget.Widget):
    def __init__(self, **kwargs):
        super(PortBase, self).__init__(**kwargs)
        self.size = [15,15]
        self.type = 'None'
        self.name = 'attr'
        self.direction = 'left'
        self.__is_selected = False
        self.__children = []
        self.__enum_button = None
        self.__enum_dropdown = None
        self._node_parent = None
        self._scene_parent = None
        self._lineStartPos = [0,0]
        self._lineEndPos = [0,0]
        self._connectPin = None
        self._connectType = 0 # 0:input 1:output
        self.render_frame()

    def build(self):
        if type(self.type) == list:
            self.enum_attr()

    def process_children(self):
        for child in self.__children:
            child[2].pos = (self.x + child[0], self.y + child[1])
            self.remove_widget(child[2])
            self.add_widget(child[2])

    def enum_attr(self):
        dropdown = DropDown()
        for enum in self.type:
            btn = Button(text=str(enum), size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        pos = (self.x, self.y)
        if self.direction == 'right':
            pos = (self.x - 100,self.y)
        mainbutton = Button(text=str(self.type[0]),pos=pos,size=(100,20))
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', str(x)))
        self.__children.append([mainbutton.x - self.x, mainbutton.y - self.y, mainbutton])
        self.__enum_button = mainbutton
        self.__enum_dropdown = dropdown

    def on_touch_down(self, touch):
        if self.__enum_button:
            if self.__enum_button.collide_point(touch.x, touch.y):
                self.__enum_dropdown.open(self.__enum_button)
        if self.collide_point(*touch.pos):
            self.__is_selected = True
            self._scene_parent._selectedPin = self
            self._scene_parent.attr_set_lock(True)
            self._node_parent.attr_set_lock(True)
        else:
            if self._scene_parent.attr_get_lock() and self.__is_selected:
                self._scene_parent.attr_set_lock(False)
            if self._node_parent.attr_get_lock() and self.__is_selected:
                self._node_parent.attr_set_lock(False)
            self.__is_selected = False

    def on_touch_move(self, touch):
        self._lineStartPos = self.pos
        self._lineEndPos = touch.pos
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self._scene_parent._selectedPin:
            if self.collide_point(*touch.pos):
                self._connectPin = self._scene_parent._selectedPin
                self._scene_parent._selectedPin._connectPin = self
                self._scene_parent._selectedPin._connectType = 1
                self._connectType = 0
        return super().on_touch_up(touch)


    def render_frame(self):
        self.canvas.clear()
        with self.canvas:
            Color(*self.hexColor("#6cb854"))
            if self.type == 'None':
                Color(*self.hexColor("#000000"))
            elif self.type == 'string':
                Color(*self.hexColor("#ffe46d"))
            elif self.type == 'int':
                Color(*self.hexColor("#2fd5e5"))
            elif self.type == 'float':
                Color(*self.hexColor("#2237b0"))
            elif self.type == 'bool':
                Color(*self.hexColor("#ff5d8d"))
            elif self.type == 'list':
                Color(*self.hexColor("#63ebc9"))
            elif self.type == 'dict':
                Color(*self.hexColor("#da30d6"))
            elif self.type == 'tuple':
                Color(*self.hexColor("#45b0d3"))
            elif self.type == 'set':
                Color(*self.hexColor("#f1f1f1"))
            elif self.type == 'object':
                Color(*self.hexColor("#6cb854"))
            elif self.type == 'bytes':
                Color(*self.hexColor("#8825f5"))
            elif type(self.type) == list:
                Color(*self.hexColor("#6cb854"))

            Rectangle(pos=self.pos, size=self.size)

            # 画线
            if self.__is_selected:
                if self._lineStartPos != [0,0] and self._lineEndPos != [0,0]:
                    Color(*self.hexColor("#ff0000"))
                    Line(points=[self._lineStartPos[0],self._lineStartPos[1],self._lineEndPos[0],self._lineEndPos[1]], width=1)

            if self._connectPin and self._connectType == 0:
                Color(*self.hexColor("#ff0000"))
                Line(points=[self.x,self.y,self._connectPin.x,self._connectPin.y], width=1)
        
        self.process_children()

    def hexColor(self, hexColor):
        if hexColor[0] == '#':
            hexColor = hexColor[1:]
        r=hexColor[0:2]
        g=hexColor[2:4]
        b=hexColor[4:6]
        return [int(r,16)/255,int(g,16)/255,int(b,16)/255,1]
