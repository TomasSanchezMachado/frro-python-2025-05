from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty

from PIL import Image as PILImage
import os
import uuid


class MainScreen():
    selected_image = StringProperty("")
    image_path = StringProperty("")

    def abrir_popup(self, base_widget):
        self.ids.file_popup.open()

    def selecciona_archivo(self, selection):
        if selection:
            self.selected_image = selection[0]
        else:
            self.ids.status_label.text = "No se seleccionó ningún archivo."

    def abrir_archivo(self, selection):
        if selection:
            try:
                with PILImage.open(selection[0]) as img:
                    img.thumbnail((800, 800))
                    temp_path = f"_temp_display_image_{uuid.uuid4().hex[:8]}.png"
                    img.save(temp_path)
                    self.image_path = temp_path  # esto ahora sí actualiza la Image
                self.ids.status_label.text = "Imagen cargada correctamente."
            except Exception as e:
                self.ids.status_label.text = f"Error: {e}"
        else:
            self.ids.status_label.text = "No se seleccionó ningún archivo."


class FileChooserApp(App):
    def build(self):
        Window.size = (800, 600)
        return MainScreen()


if __name__ == "__main__":
    FileChooserApp().run()
