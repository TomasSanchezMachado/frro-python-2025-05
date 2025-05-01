from kivy.app import App
from kivy.properties import StringProperty  
from kivy.uix.boxlayout import BoxLayout
from PIL import Image as PILImage
import uuid
import os


class MainScreen(BoxLayout):
    image_path = StringProperty("") 
    initial_path = StringProperty(os.path.expanduser("~"))  # Cambia esto a la ruta inicial deseada
    # esto se hace porque sino, al seleccionar una imagen se abre sin apretar cargar imagen
    def selecciona_archivo(self, selection):
        if selection:
            self.selected_image = selection[0]

    def abrir_archivo(self, selection):
        if selection:
            with PILImage.open(self.selected_image) as img:
                img.thumbnail((800, 800))
                temp_path = f"_temp_display_image_{uuid.uuid4().hex[:8]}.png"
                img.save(temp_path)
                self.image_path = temp_path  # esto ahora sí actualiza la Image

        

class FileChooserApp(App):
    pass


if __name__ == "__main__":
    FileChooserApp().run()
