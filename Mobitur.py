from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class TourCalculatorApp(App):
    def build(self):
        self.title = "Калькулятор туриста"
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Поле для взрослых
        self.create_section(root, "Взрослые", self.on_adults_input)
        root.add_widget(Label(size_hint_y=None, height=20))

        # Поле для детей
        self.create_section(root, "Дети", self.on_children_input)
        root.add_widget(Label(size_hint_y=None, height=20))

        # Кнопка расчёта
        self.calc_btn = Button(text="Рассчитать", size_hint_y=None, height=50)
        self.calc_btn.bind(on_press=self.calculate)
        root.add_widget(self.calc_btn)

        # Результат
        self.result_label = Label(text="Итого: —", size_hint_y=None, height=50, font_size=18)
        root.add_widget(self.result_label)

        return root

    def create_section(self, parent, title, callback):
        parent.add_widget(Label(text=title, size_hint_y=None, height=30, bold=True))
        labels = ["Кол-во:", "Дни:", "Проживание:", "Трансфер:", "Питание:", "Доп.услуги:"]
        defaults = {
            "Взрослые": ["2", "2", "2500", "1200", "1200", "3000"],
            "Дети": ["2", "2", "1700", "800", "900", "2000"]
        }
        vals = defaults[title]
        self.inputs = getattr(self, 'inputs', {})
        self.inputs[title] = []
        for i, (lbl, val) in enumerate(zip(labels, vals)):
            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(Label(text=lbl, size_hint_x=0.4))
            ti = TextInput(text=val, multiline=False, input_filter='float', size_hint_x=0.6)
            ti.bind(text=callback)
            row.add_widget(ti)
            self.inputs[title].append(ti)
            parent.add_widget(row)

    def on_adults_input(self, instance, value):
        pass
    def on_children_input(self, instance, value):
        pass

    def get_values(self, section):
        return [float(inp.text or '0') for inp in self.inputs[section]]

    def calculate(self, instance):
        try:
            a = self.get_values("Взрослые")
            c = self.get_values("Дети")

            total_adults = a[0] * (a[1] * a[2] + a[3] + a[1] * a[4] + a[5])
            total_children = c[0] * (c[1] * c[2] + c[3] + c[1] * c[4] + c[5])
            total = total_adults + total_children

            # Согласно Excel: итоговое значение
            self.result_label.text = f"Итого: {total:,.0f}"
        except Exception:
            self.result_label.text = "Ошибка ввода"


TourCalculatorApp().run()