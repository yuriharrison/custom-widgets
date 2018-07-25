from kivy.factory import Factory
from kivy.properties import BooleanProperty
from kivy.uix.button import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

# TODO: implement the ScrollView inside the SelectionBox widget
# TODO: implement `clean` method, remove all itens and reset the box

Builder.load_string('''
<SelectionBox>:
    orientation: 'vertical'
    size_hint_y: None if self.orientation == 'vertical' else 1
    size_hint_x: None if self.orientation == 'horizontal' else 1
    height: self.minimum_height
    width: self.minimum_width
    spacing: sp(5)
    model: 'SelectionBoxItem'

<SelectionBoxItem>:
    size_hint_y: None if self.box.orientation == 'vertical' else 1
    size_hint_x: None if self.box.orientation == 'horizontal' else 1
    height: sp(60)
    width: sp(60)
    color_normal: (.4,.4,.4,1)
    color_selected: (.6,.6,.6,1)

    canvas:
        Color:
            rgba: self.color_selected if self.selected else self.color_normal
        Rectangle:
            size: self.size
            pos: 0,0
''')


class SelectionBoxItem(ButtonBehavior, RelativeLayout):
    """Selection Box Item is the widget generated for each
    item setted in the `data` attribute of `SelectionBox`.

    # Attributes
        color_normal: background color of the item
        color_selected: background color of the item when selected

    # Property
        index: int, index of the item in the SelectionBox
        data: object, respective data item from `SelectionBox.data`
    """
    selected = BooleanProperty(False)
    
    def __init__(self, box=None, data=None):
        self.box = box
        self.data = data
        super().__init__()


class SelectionBox(BoxLayout):
    """Selection Box is a widget which creates a box with
    a list of `SelectionBoxItem` widgets generated from a
    given set of items and allow simple or multiple selection.

    It's necessary to load the itens after set the `data`. To do
    that you have to call the method `load_items`.

    # Attributes
        orientation: str, optional, default 'vertical'
        spacing: NumericProperty, optional, default sp(5)
        multi_selection: bool, optional, default False -
            set it to True to allow multi selection
        model: str, optional, default 'SelectionBoxItem' -
            name of the item `SelectionBoxItem` object
        data: list, required to generate the widget items -
            list of any kind of object

    # Property
        selected_item: `SelectionBoxItem` widget or a list of
            `SelectionBoxItem` objects if multi selection is allowed
        previous_item: `SelectionBoxItem` widget, previous selected item
        selected_index: int, index of the last item selected
        previous_index: int, index of the previous item selected

    # Events
        on_selection_changed: called every time a item is selected or
            unselected
            - add a function using the kivy bind method
            - args: item
                - item - `SelectionBoxItem` widget selected
    
    ### Examples

    **Python file**

    ```python
    from kivy.uix.relativelayout import RelativeLayout
    from kivy.properties import ObjectProperty

    class DataItem:
        def __init__(self, text):
            self.text = text

    Builder.load_file('main.kv')
    class MainScreen(RelativeLayout):
        selection_box = ObjectProperty(None)

        def on_selection_box(self, i, selection_box):
            text = 'Item '
            data = [DataItem(text + str(i)) for i in range(10)]

            selection_box.data = data
            selection_box.load_items()
            selection_box.bind(on_selection_changed=self.on_selection_changed)
        
        def on_selection_changed(self, sb, item):
            msg = '[Item clicked]: Index - {} Text - "{}"'.format(item.index, item.data.text)
            print(msg)

    class MainApp(App):

        def build(self):
            return MainScreen()


    if __name__ == "__main__":
        MainApp().run()
    ```

    **Kivy file**

    ```kivy
    #:kivy 1.0.0

    <SelectionBoxItem>:
        # size_hint_y: None
        height: sp(80)
        color_normal: (.0,.2,.3,1) # dark blue
        color_selected: (.0,.3,1,1) # bright blue
        
        Label:
            color: 0,0,0,1
            text: root.data.text


    <MainScreen>:
        selection_box: sb

        RelativeLayout:
            size_hint: (.3,.7)
            pos_hint: {'center_x': .5, 'center_y': .5}

            ScrollView:
                canvas.before:
                    Color:
                        rgba: 1,1,1,1
                    Rectangle:
                        size: self.size
                        pos: 0,0

                SelectionBox:
                    id: sb
                    # spacing: sp(15)
    ```

    **Custom item `SelectionBoxItem` widget**

    ```kivy
    <CustomItem@SelectionBoxItem>:
        # customization...

        
    <MainScreen>:
        selection_box: sb

        RelativeLayout:
            # ...

            ScrollView:
                # ...
                SelectionBox:
                    id: sb
                    model: 'CustomItem'
    ```

    """
    multi_selection = BooleanProperty(False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.register_event_type('on_selection_changed')
        self.silent = False
        self.data = []
        self.items = []
        self._selection_changed_events = []
        self.reset()

    @property
    def selected_item(self):
        if self.multi_selection:
            return [self.items[index] for index in self.selected_index_ls]
        else:
            return self.items[self.selected_index]
    
    @property
    def previous_item(self):
        return self.items[self.previous_index]

    def select(self, value, silent=False):
        """Select an item in the box by informing the index
        or the `SelectionBoxItem` widget direcly.

        # Arguments
            value: index or `SelectionBoxItem`, required
            silent: bool, optional, default False -
                select the item quietly, without dispatch the 
                `on_selection_changed` event

        # Exception
            ValueError: raise when the `value`:
                - index - index out of range
                - `SelectionBoxItem` - object don't match
                    any item in the box
        """
        self.silent = silent
        tp = type(value)
        
        if tp is int:
            item = self.items[value]
        elif value in self.items:
            item = value
        else:
            raise ValueError('{} don\'t contain {}'.format(type(self), value))
        
        item.dispatch(event_type='on_press')

    def load_items(self):
        """Generate `SelectionBoxItem` widgets with the
        data setted on `self.data`. The widgets are added to
        the box.
        """
        self.items = []

        for i, data_item in enumerate(self.data):
            widget = self._new_item(data_item)
            widget.index = i
            self.add_widget(widget)
            self.items.append(widget)
    
    def on_selection_changed(self, item):
        pass

    def reset(self):
        """Reset the index variables and unselect all items."""
        self.selected_index = None
        self.selected_index_ls = []
        self.previous_index = None

        for item in self.items:
            item.selected = False


    def _new_item(self, item):
        model = Factory.classes[self.model]['cls']
        instance = model(box=self, data=item)
        instance.bind(on_press=self._on_item_press)
        return instance
    
    def _on_item_press(self, item):
        if not item.selected:
            item.selected = True

            self.previous_index = self.selected_index
            self.selected_index = item.index

            if self.multi_selection:
                self.selected_index_ls.append(item.index)
            elif self.previous_index is not None:
                self.items[self.previous_index].selected = False

        elif self.multi_selection:
            item.selected = False
            self.selected_index_ls.remove(item.index)

        if not self.silent:
            self.dispatch('on_selection_changed', item)
        else:
            self.silent = False
