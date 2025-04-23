from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class Calculadora(GridLayout):
    def __init__(self, **kwargs):
        super(Calculadora, self).__init__(**kwargs)
        self.cols = 1

        # Pantalla
        self.resultado = Label(text="0", font_size=40, halign="right", size_hint_y=0.3)
        self.add_widget(self.resultado)

        # Layout botones
        botones_layout = GridLayout(cols=4)

        botones = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "=", "+"
        ]

        for texto in botones:
            boton = Button(text=texto, font_size=32)
            boton.bind(on_press=self.pulsar_boton) #type: ignore
            botones_layout.add_widget(boton)

        self.add_widget(botones_layout)
        self.operacion = ""

    def pulsar_boton(self, instance):
        texto = instance.text

        if texto == "C":
            self.operacion = ""
            self.resultado.text = "0"
        elif texto == "=":
            try:
                self.resultado.text = str(eval(self.operacion))
                self.operacion = self.resultado.text
            except:
                self.resultado.text = "Error"
                self.operacion = ""
        else:
            self.operacion += texto
            self.resultado.text = self.operacion

class CalculadoraApp(App):
    def build(self):
        return Calculadora()

if __name__ == "__main__":
    CalculadoraApp().run()
