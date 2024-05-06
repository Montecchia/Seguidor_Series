import toga
from toga.style import Pack
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW
import anidbcli


class Serie:
    nombre = ""
    cantidad_capitulos = 0
    capitulos = []


def agregar_serie(tabla_series, nombre, cantidad_capitulos, capitulos=None):
    serie = Serie()
    serie.nombre = nombre
    serie.cantidad_capitulos = cantidad_capitulos
    if capitulos is not None:
        serie.capitulos = capitulos
    tabla_series.append(serie)


class SeguidorSeries (toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        box_ingresos = toga.Box(style=Pack(direction=COLUMN))
        box_tablas = toga.Box(style=Pack(direction=ROW))

        tabla_series = toga.Table(headings=["Título", "Capítulos"], style=Pack(flex=1, direction=ROW))
        tabla_capitulos = toga.Table(headings=["Capítulo", "Visto"], style=Pack(flex=1, direction=ROW))
        box_tablas.add(tabla_series)
        box_tablas.add(tabla_capitulos)

        box_nombre = toga.Box(style=Pack(direction=ROW, padding=5))
        input_nombre = toga.TextInput(value="ejemplo.txt", style=Pack(flex=1))
        label_nombre = toga.Label("Nombre del archivo:                    ")
        box_nombre.add(label_nombre)
        box_nombre.add(input_nombre)

        box_url = toga.Box(style=Pack(direction=ROW, padding=5))
        input_url = toga.TextInput(value="https://test.com/series/", style=Pack(flex=1))
        label_url = toga.Label("URL del listado de series:             ")
        box_url.add(label_url)
        box_url.add(input_url)

        box_ingresos.add(box_nombre)
        box_ingresos.add(box_url)

        main_box.add(box_tablas)
        main_box.add(box_ingresos)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return SeguidorSeries(formal_name="Extractor de series",
                          app_name="extractor_series",
                          app_id="extractor_series",
                          icon="icono",
                          author="Eduardo Montecchia",
                          description="Versión 0.1.2")


if __name__ == '__main__':
    main().main_loop()
