<span style="float:right;">[[source code]](https://github.com/yuriharrison/custom-widgets/blob/master/custom-widgets/selectionBox.py#L58)</span>
## SelectionBox

```python
selectionBox.SelectionBox()
```

Selection Box is a widget which creates a box with
a list of `SelectionBoxItem` widgets generated from a
given set of items and allow simple or multiple selection.

It's necessary to load the itens after set the `data`. To do
that you have to call the method `load_items`.

__Attributes__

- `orientation` -  str, optional, default 'vertical'
- `spacing` -  NumericProperty, optional, default sp(5)
- `multi_selection` -  bool, optional, default False -
    set it to True to allow multi selection
- `model` -  str, optional, default 'SelectionBoxItem' -
    name of the item `SelectionBoxItem` object
- `data` -  list, required to generate the widget items -
    list of any kind of object

__Property__

- `selected_item` -  `SelectionBoxItem` widget or a list of
    `SelectionBoxItem` objects if multi selection is allowed
- `previous_item` -  `SelectionBoxItem` widget, previous selected item
- `selected_index` -  int, index of the last item selected
- `previous_index` -  int, index of the previous item selected

__Events__

- `on_selection_changed` -  called every time a item is selected or
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



---
## SelectionBox methods

### load_items


```python
load_items()
```


Generate `SelectionBoxItem` widgets with the
data setted on `self.data`. The widgets are added to
the box.


---
### select


```python
select(value, silent=False)
```


Select an item in the box by informing the index
or the `SelectionBoxItem` widget direcly.

__Arguments__

- `value` -  index or `SelectionBoxItem`, required
- `silent` -  bool, optional, default False -
    select the item quietly, without dispatch the 
    `on_selection_changed` event

__Exception__

- `ValueError` -  raise when the `value`:
    - index - index out of range
    - `SelectionBoxItem` - object don't match
        any item in the box


---
### reset


```python
reset()
```


Reset the index variables and unselect all items.

----

<span style="float:right;">[[source code]](https://github.com/yuriharrison/custom-widgets/blob/master/custom-widgets/selectionBox.py#L38)</span>
## SelectionBoxItem

```python
selectionBox.SelectionBoxItem(box=None, data=None)
```

Selection Box Item is the widget generated for each
item setted in the `data` attribute of `SelectionBox`.

__Attributes__

- `color_normal` -  background color of the item
- `color_selected` -  background color of the item when selected

__Property__

- `index` -  int, index of the item in the SelectionBox
- `data` -  object, respective data item from `SelectionBox.data`
