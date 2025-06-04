from kivy.app import App
import os
import uuid
from PIL import Image as PILImage

class FileChooserApp(App):
    selected_image = ""

    def abrir_archivo(self, path):
        if not path:
            return ""
        with PILImage.open(path) as img:
            img.thumbnail((800, 800))
            temp_path = f"_temp_display_image_{uuid.uuid4().hex[:8]}.png"
            img.save(temp_path)
            self.selected_image = temp_path
        return temp_path

if __name__ == "__main__":
    app = FileChooserApp()
    app.run()
    