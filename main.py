import toga
from toga.sources import ListSource
from toga.style import Pack
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW
import adbb
from adbb import Anime
import sqlalchemy
from sqlalchemy import create_engine


user = "montecchiacorp"
password = "k-gpQzCw-uU5zQf"
sql = "sqlite:///adbb.db"

adbb.init(sql, user, password, debug=True)
Session = adbb.get_session()

animes = Session.query(adbb.db.AnimeTable.aid).all()
ids = [numero[0] for numero in animes]


def agregar_serie(tabla_series, nombre):
    anime = adbb.Anime(nombre)
    tabla_series.data.append([anime.title, anime.highest_episode_number])


def llenar_capitulos(tabla_capitulos, nombre_anime):
    anime = adbb.Anime(nombre_anime)
    for numero in range(1, anime.highest_episode_number+1):
        episodio = adbb.Episode(anime=anime, epno=numero)
        tabla_capitulos.data.append([episodio.epno, episodio.title_eng, False])


class SeguidorSeries (toga.App):

    def cargar_capitulos(self, *args, row):
        self.tabla_capitulos.data.clear()
        llenar_capitulos(self.tabla_capitulos, row.título)

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        box_ingresos = toga.Box(style=Pack(direction=COLUMN, flex=1))
        box_tablas = toga.Box(style=Pack(direction=ROW, flex=2))

        self.tabla_capitulos = toga.Table(
            headings=["Capítulo", "Título", "Visto"],
            style=Pack(flex=1, direction=ROW))


        self.tabla_series = toga.Table(
            headings=["Título", "Capítulos"],
            style=Pack(flex=1, direction=ROW),
            on_activate=self.cargar_capitulos,
            multiple_select=False)

        for anime in ids:
            agregar_serie(self.tabla_series, anime)

        box_tablas.add(self.tabla_series)
        box_tablas.add(self.tabla_capitulos)

        box_nombre = toga.Box(style=Pack(direction=ROW, padding=5))
        input_nombre = toga.TextInput(value="ejemplo.txt", style=Pack(flex=1))
        label_nombre = toga.Label("Nombre de la serie:                    ")
        box_nombre.add(label_nombre)
        box_nombre.add(input_nombre)

        def iniciar():
            def on_press(input_button):
                try:
                    return agregar_serie(self.tabla_series,
                                         input_nombre.value)
                except Exception as e:
                    print(str(e))

            return on_press

        input_button = toga.Button("Iniciar", on_press=iniciar())

        box_ingresos.add(box_nombre)
        box_ingresos.add(input_button)

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
