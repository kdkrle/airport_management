import datetime as dt

import psycopg2 as pg
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt


class Avioni:
    """Klasa za manipulaciju podacima iz tabele 'avioni'."""
    
    def __init__(self):
        self.con = pg.connect(
            database="aerodrom",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.avioni_df = None

    def avioni_ucitavanje(self):
        """Osvežavanje podataka tabele 'avioni'."""
    
        self.avioni_df = pd.read_sql_query("SELECT * FROM avioni", self.con)


class Linije:
    """Klasa za upravljanje podacima iz tabele 'linije'."""
    
    def __init__(self):
        self.con = pg.connect(
            database="aerodrom",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.linije_df = None
    
    def linije_ucitavanje(self):
        """Osvežavanje podataka tabele 'linije'."""
    
        self.linije_df = pd.read_sql_query("SELECT * FROM linije", self.con)
    
    def time_sort(self):
        """Tabela 'linije' sortirana po polascima."""
        time_sort_df = self.linije_df.sort_values(by=["polazak"])
        return time_sort_df
    
    def indeksi_narednih_letova(self):
        """Dobijanje indeksa pet narednih letova iz tabele 'linije'."""
        
        #Lista indeksa prethodno sortirane tabele.
        sortirana_tbl = linije.time_sort()
        sort_indices = sortirana_tbl.polazak.index.to_list()
        
        #Lista je udvostručena da bi, ukoliko se dođe do samog kraja liste,
        # prešla na indekse s vrha liste - da ne bismo dobili informacije za
        # manje od 5 letova.
        double_sort_indices = sort_indices * 2
        
        #Dobijanje željenih indeksa u formi liste.
        for i in range(len(double_sort_indices)):
            idx = double_sort_indices[i]
            current_time_string = dt.datetime.now().strftime("%H:%M")
            current_time = dt.datetime.strptime(current_time_string,
                                             "%H:%M").time()
            if current_time < sortirana_tbl.polazak[sortirana_tbl.index ==
                                                    idx][idx]:
                required_indices = double_sort_indices[i:i+5]
                return required_indices
    
    def preostali_letovi(self):
        """Dobijanje podataka za letove do kraja dana."""
        
        tabela_sort = self.time_sort()
        #Indeksi sortirane tabele po vremenu polaska.
        indeksi_sort = tabela_sort.index.to_list()
        
        #Dobijanje trenutnog vremena.
        trenutno_vreme_str = dt.datetime.now().strftime("%H:%M")
        trenutno_vreme = dt.datetime.strptime(trenutno_vreme_str,
                                                    "%H:%M").time()
        
        for i in range(len(indeksi_sort)):
            idx = indeksi_sort[i]
            if trenutno_vreme < tabela_sort.polazak[tabela_sort.index ==
                                                    idx][idx]:
                indeksi_za_letove = indeksi_sort[i:]
                preostali_letovi_df = tabela_sort.loc[indeksi_za_letove]
                return preostali_letovi_df
    
    def lista_destinacija(self):
        """Kreiranje sortirane liste destinacija narednih letova."""
        
        dest_sort_df = self.linije_df.sort_values(by=["destinacija"])
        dest_list = []
        for dest in dest_sort_df.destinacija:
            if dest not in dest_list:
                dest_list.append(dest)
        return dest_list


class Putnici:
    """Klasa za upravljanje podacima iz tabele 'putnici'."""
    
    def __init__(self):
        self.con = pg.connect(
            database="aerodrom",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.putnici_df = None
    
    def putnici_ucitavanje(self):
        """Osvežavanje podataka tabele 'putnici'."""
        
        self.putnici_df = pd.read_sql_query("SELECT * FROM putnici", self.con)
    
    def eksportovanje(self, rb_vrednost, entry_polje):
        """Eksportovanje fajla u jednom od datih formata u zavisnosti od
        izbora."""
        if not entry_polje.get():
            return messagebox.showerror(
                title="Greška",
                message="Niste uneli ime fajla."
            )
        elif rb_vrednost == "1" and entry_polje.get():
            self.putnici_df.to_excel(f"{entry_polje.get()}.xlsx")
        elif rb_vrednost == "2" and entry_polje.get():
            self.putnici_df.to_csv(f"{entry_polje.get()}.csv")
        elif rb_vrednost == "3" and entry_polje.get():
            self.putnici_df.to_json(f"{entry_polje.get()}.json")
        return messagebox.showinfo(
            title="Eksport podataka",
            message="Vaši podaci su uspešno sačuvani."
        )
    
    def graficki_prikaz(self, tip_var, nacin_var, broj_var):
        """Grafičko prikazivanje nekih podataka vezanih za putnike."""

        #Broj podataka za prikazivanje
        if broj_var.get() == "1":
            broj = 5
        elif broj_var.get() == "2":
            broj = 7
        else:
            broj = 10
            
        # Vrednost po kojoj se vrši poređenje podataka.
        if tip_var.get() == "1":
    
            #Najzastupljenije državljanstvo.
            najzastupljeniji_df = \
                self.putnici_df.drzavljanstvo.value_counts().head(broj)
            x_values = list(najzastupljeniji_df.index)
            y_values = list(najzastupljeniji_df)
            y_lbl = "Broj putnika"
            x_lbl = "Država"
            naslov = "Države iz kojih su najzastupljeniji putnici"
            color_bar = "darkorange"
            color_title = "darkred"
        elif tip_var.get() == "2":
            #Sortiranje podataka po kriterijumu broja letova.
            ukupno_letova = self.putnici_df.sort_values(
                by=["broj ranijih letova"],
                ascending=False
            )
            x_values = ukupno_letova["ime i prezime"].head(broj)
            y_values = ukupno_letova["broj ranijih letova"].head(broj)
            x_lbl = "Putnik"
            y_lbl = "Broj letova"
            naslov = "Putnici s najvećim brojem letova"
            color_bar = "olive"
            color_title = "forestgreen"
            
        else:
            najvise_km = self.putnici_df.sort_values(
                by=["kilometraza"],
                ascending=False
            )
            x_values = najvise_km["ime i prezime"].head(broj)
            y_values = najvise_km["kilometraza"].head(broj)
            x_lbl = "Putnik"
            y_lbl = "Pređenih kilometara"
            naslov = "Putnici s najviše pređenih kilometara"
            color_bar = "silver"
            color_title = "mediumblue"
            
        #Vrsta grafičkog prikaza.
        if nacin_var.get() == "1":
            plt.bar(x_values, y_values, color=color_bar)
            plt.title(naslov, fontdict={"family": "serif", "color":
                color_title, "size": 18})
            plt.xlabel(x_lbl)
            plt.ylabel(y_lbl)
            plt.xticks(rotation=80)
            plt.grid()
            plt.subplots_adjust(bottom=0.4)
            
            plt.show()
        else:
            explode_val = []
            for i in range(broj):
                if i == 0:
                    explode_val.append(0.2)
                else:
                    explode_val.append(0)
            plt.pie(y_values, labels=x_values, autopct="%1.1f%%",
                    shadow=True, explode=explode_val)
            plt.title(naslov)
            
            plt.show()
    
    def novi_putnik(self, pasos_id, ime, god, drzava):
        cursor = self.con.cursor()
        
        sql_novi_putnik = f"""
        INSERT INTO putnici("broj pasosa", "ime i prezime", starost,
        drzavljanstvo, "broj ranijih letova", kilometraza, popust,
        "iskoriscen popust")
        VALUES('{pasos_id}', '{ime}', {god}, '{drzava}', 0, 0, 0, True);
        """

        cursor.execute(sql_novi_putnik)
        self.con.commit()
        cursor.close()


class Rezervacije:
    """Klasa za manipulaciju podacima iz tabele 'rezervisanje'."""
    
    def __init__(self):
        self.con = pg.connect(
            database="aerodrom",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.rezervacije_df = None
        
    def rezervacije_ucitavanje(self):
        """Učitavanje podataka tabele 'rezervisanje'."""
        
        self.rezervacije_df = pd.read_sql_query("SELECT * FROM rezervacije",
                                                self.con)
    def unos_u_tabelu(self, dest, date, polaz, sed, pasos, povrat, cena):
        """Unos prikazanih podataka u tabelu 'rezervisanje'."""
        
        cursor = self.con.cursor()
        
        kolone_rez = self.rezervacije_df.columns.to_list()
        sql_rez =f"""
        INSERT INTO rezervacije ("{kolone_rez[1]}",
        "{kolone_rez[2]}", "{kolone_rez[3]}", "{kolone_rez[4]}",
        "{kolone_rez[5]}", "{kolone_rez[6]}", "{kolone_rez[7]}")
        VALUES ('{dest}', '{date}', '{polaz}', '{sed}', '{pasos}',
        {povrat}, {cena});
        """
        
        cursor.execute(sql_rez)
        self.con.commit()
        cursor.close()
        
    def brisanje_rezervacija(self):
        """Zbog datuma koji se stalno menja tabela 'rezevacije' se briše
        nakon svakog pokretanja programa."""
        
        cursor = self.con.cursor()
        sql_brisanje = "TRUNCATE rezervacije"
        cursor.execute(sql_brisanje)
        self.con.commit()
        cursor.close()

avioni = Avioni()
avioni.avioni_ucitavanje()
linije = Linije()
linije.linije_ucitavanje()
putnici = Putnici()
putnici.putnici_ucitavanje()
rezervacije = Rezervacije()
rezervacije.rezervacije_ucitavanje()