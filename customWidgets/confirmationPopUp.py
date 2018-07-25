"""Confirmation Pop-up"""
import functools
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.lang.builder import Builder


Builder.load_string('''
<ConfirmationPopup>:
    auto_dismiss: False
    title: 'Are you sure?'
    result: None
    size_hint: (.7,.7)
    description: ''
    button_continue_text: 'Continue'
    button_cancel_text: 'Cancel'

    BoxLayout:
        orientation: 'vertical'

        Label:
            text: root.description
            text_size: self.size
            padding_y: sp(20)
            font_size: sp(20)
            halign: 'left'
            valign: 'top'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: .25
            pos_hint: {'y': 0}
            Button:
                text: root.button_continue_text
                on_release:
                    root.result = 'continue'
                    root.dismiss()
            Button:
                text: root.button_cancel_text
                on_release:
                    root.result = 'cancel'
                    root.dismiss()
''')


class ConfirmationPopup(Popup):
    """Confirmation Pop-up widget, inherit from Popup class.

    To open it, just call the `open` method. To get the user
    answer bind a method to the `on_dismiss` event and check
    the `result` property.

    # Attributes
        title: str, optional, default 'Are you sure?'; - 
            title of the pop-up
        description: str, optional, default '' - 
            text located in the body of the pop-up
        button_continue_text: str, optional, 'Continue' -
            text of the continue button (left button)
        button_cancel_text: str, optional, 'Cancel'
            text of the cancel button (right button)

    # Property
        result: str, 'continue', 'cancel' or None, default None -
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
    """
    title = StringProperty('')
    description = StringProperty(None)
    button_continue_text = StringProperty(None)
    button_cancel_text = StringProperty(None)


class ConfirmationPopupDecorator:
    """Confirmation Popup Decorator

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
    """
    
    def __init__(self, klass=ConfirmationPopup, **kw):
        self._a_func = {}
        self._kw_func = {}
        self._self_func = None
        self.popup = None

        self._kw_config = kw
        self._cls = klass

    def __call__(self, func=None):
        self._func = func
        return functools.partialmethod(ConfirmationPopupDecorator.decorator, self)

    @staticmethod
    def decorator(func_self, self, *a, **kw):
        self._a_func = a
        self._kw_func = kw
        self._self_func = func_self
        self.popup = self._cls(**self._kw_config)
        self.popup.bind(on_dismiss=self.on_dismiss)
        self.popup.open()

    def on_dismiss(self, widget):
        if self.popup.result == 'continue':
            self._func(self._self_func, *self._a_func, **self._kw_func)

    