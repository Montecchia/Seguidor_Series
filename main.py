import toga
from toga.style import Pack
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW
import adbb
import relleno

user = "montecchiacorp"
password = "k-gpQzCw-uU5zQf"
sql = "sqlite:///adbb.db"

adbb.init(sql, user, password, debug=True)
Session = adbb.get_session()

animes = Session.query(adbb.db.AnimeTable.aid).all()
ids = [numero[0] for numero in animes]


def agregar_serie(tabla_series, nombre):
    anime = adbb.Anime(nombre)
    capitulos_relleno = 0
    titulo_anime = anime.title
    for titulo in anime.titles:
        if titulo.lang == "eng" and titulo.titletype == "official":
            titulo_anime = titulo.title
            break

    link_relleno = relleno.buscar_serie(titulo_anime)

    if link_relleno is not None:
        capitulos_relleno = len(list(filter(lambda x: x < anime.highest_episode_number,
                                            relleno.lista_relleno(link_relleno))))

    tabla_series.data.append({"título": titulo_anime,
                              "capítulos": anime.highest_episode_number,
                              "relleno": capitulos_relleno,
                              "link": link_relleno})


def llenar_capitulos(tabla_capitulos, nombre_anime, url_relleno, filtrar_relleno, barra_carga):
    anime = adbb.Anime(nombre_anime)
    lista_relleno = relleno.lista_relleno(url_relleno)
    barra_carga.max = anime.highest_episode_number+1
    for numero in range(1, anime.highest_episode_number+1):
        barra_carga.value = numero
        es_relleno = "Canon"
        episodio = adbb.Episode(anime=anime, epno=numero)
        if numero in lista_relleno:
                es_relleno = "Relleno"
                if filtrar_relleno:
                    continue
        tabla_capitulos.data.append([episodio.epno, episodio.title_eng, False, es_relleno])
        tabla_capitulos.refresh()


class SeguidorSeries (toga.App):
    current_row = None

    def cargar_capitulos(self, *args, row):
        if row is not None:
            self.tabla_capitulos.data.clear()
            self.barra_carga.start()
            llenar_capitulos(self.tabla_capitulos,
                             row.título, row.link,
                             self.filtrar_relleno.value,
                             self.barra_carga)
            self.barra_carga.value = 0
            self.barra_carga.stop()
            self.current_row = row

    def alternar_visto(self, *args, row):
        if row.visto:
            row.visto = False
        else:
            row.visto = True
        self.tabla_capitulos.refresh()

    def filtrar_relleno(self, *args):
        self.cargar_capitulos(row=self.current_row)

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        box_ingresos = toga.Box(style=Pack(direction=COLUMN, flex=1, height=100))
        box_tablas = toga.Box(style=Pack(direction=ROW, flex=5))

        self.tabla_capitulos = toga.Table(
            headings=["Capítulo", "Título", "Visto", "Tipo"],
            style=Pack(flex=2, direction=ROW),
            on_activate=self.alternar_visto)

        self.tabla_series = toga.Table(
            headings=["Título", "Capítulos", "Relleno"],
            data=[],
            style=Pack(flex=1, direction=ROW),
            on_activate=self.cargar_capitulos,
            multiple_select=False)

        for anime in ids:
            agregar_serie(self.tabla_series, anime)

        box_tablas.add(self.tabla_series)
        box_tablas.add(self.tabla_capitulos)

        box_nombre = toga.Box(style=Pack(direction=ROW, padding=5))
        input_nombre = toga.TextInput(value="ejemplo.txt", style=Pack(flex=25, padding=3, alignment=RIGHT, width=500))
        label_nombre = toga.Label("Nombre de la serie:  ", style=Pack(padding=5))
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

        input_button = toga.Button("Iniciar", on_press=iniciar(), style=Pack(flex=1, padding=7, alignment=RIGHT))

        self.filtrar_relleno = toga.Switch(
            "Ocultar relleno",
            value=False,
            on_change=self.filtrar_relleno)

        self.barra_carga = toga.ProgressBar(style=Pack(flex=1))

        box_checks = toga.Box(style=Pack(direction=ROW, padding=2))
        box_input = toga.Box(style=Pack(direction=ROW, padding=2))

        separador1 = toga.Divider(style=Pack(padding=5))

        box_input.add(box_nombre)
        box_input.add(input_button)
        box_checks.add(self.filtrar_relleno)
        box_checks.add(self.barra_carga)
        box_ingresos.add(box_input)
        box_ingresos.add(separador1)
        box_ingresos.add(box_checks)

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
