<span style="float:right;">[[source code]](https://github.com/yuriharrison/custom-widgets/blob/master/customWidgets/confirmationPopUp.py#L46)</span>
## ConfirmationPopup

```python
kivy.uix.modalview.ConfirmationPopup()
```

Confirmation Pop-up widget, inherit from Popup class.

To open it, just call the `open` method. To get the user
answer bind a method to the `on_dismiss` event and check
the `result` property.

__Attributes__

- `title` -  str, optional, default 'Are you sure?'; - 
    title of the pop-up
- `description` -  str, optional, default '' - 
    text located in the body of the pop-up
- `button_continue_text` -  str, optional, 'Continue' -
    text of the continue button (left button)
- `button_cancel_text` -  str, optional, 'Cancel'
    text of the cancel button (right button)

__Property__

- `result` -  str, 'continue', 'cancel' or None, default None -
    user answer to the pop-up
    - `None` - not answered
    - `continue` - left button clicked
    - `cancel` - right button clicked

### Example

**Kivy file**

```kivy
#:kivy 1.0.7
<ConfirmationPopup>:
    description: 'Do you want to close the application?'
    button_continue_text: 'Yes'
    button_cancel_text: 'No'

<MainScreen>:
    Button:
        text: 'Close the application'
        on_press: root.on_button_press()
```

**Python file**

```python
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout


class MainScreen(RelativeLayout):

    def on_button_press(self):
        pup = ConfirmationPopup()
        pup.bind(on_dismiss=self.on_popup_dismiss)
        pup.open()

    def on_popup_dismiss(self, pup):
        if pup.result == 'continue':
            App.get_running_app().stop()
    

class MainApp(App):

    def build(self):
        return MainScreen()


if __name__ == "__main__":
    MainApp().run()
```


----

<span style="float:right;">[[source code]](https://github.com/yuriharrison/custom-widgets/blob/master/customWidgets/confirmationPopUp.py#L122)</span>
## ConfirmationPopupDecorator

```python
confirmationPopUp.ConfirmationPopupDecorator(klass=<class 'confirmationPopUp.ConfirmationPopup'>)
```

Confirmation Popup Decorator

This class apply the ConfirmationPopup functionality to
any method as a decorator.

This decorator can receive kwargs to easily customize the
popup. See the examples bellow.

### Examples

#### Simple aplication

**Kivy file**

```kivy
<ConfirmationPopup>:
    description: 'Do you want to close the application?'
    button_continue_text: 'Yes'
    button_cancel_text: 'No'

<MainScreen>:
    Button:
        text: 'Close the application'
        on_press: root.on_button_press('Closing the app...')
```

**Python file**
```python
class MainScreen(RelativeLayout):
    
    @ConfirmationPopupDecorator()
    def on_button_press(self, msg):
        print(msg)
        import time
        time.sleep(2)

        App.get_running_app().stop()
```

#### Customizing

**Simple customization**

```python
class MainScreen(RelativeLayout):

    @ConfirmationPopupDecorator(title='Closing the app...')
    def on_button_press(self):
        App.get_running_app().stop()
```

**More customization**

```python
class MainScreen(RelativeLayout):
    confirmation_popup = ConfirmationPopupDecorator(
        title='New title',
        description='Description',
        # ... any attribute you want to modiffy
    )

    @confirmation_popup
    def on_button_press(self):
        # ...
```

**Using a custom popup class**

```python
class MyCustomPopup(ConfirmationPopup):
    # ...
    
class MainScreen(RelativeLayout):

    @ConfirmationPopupDecorator(MyCustomPopup)
    def on_button_press(self):
        # ...
```

**Using a custom popup class and new kwargs**

```python
class MyCustomPopup(ConfirmationPopup):

    def __init__(self, new_kwarg=None, **kw):
        super().__init__(**kw)
        # ...
    
class MainScreen(RelativeLayout):
    custom_popup = ConfirmationPopupDecorator(
        klass=MyCustomPopup,
        new_kwarg='value'
    )

    @custom_popup
    def on_button_press(self):
        # ...
```
