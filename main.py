import random
from aerodrom import *
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from zavrsni_ispit.pomocni.short_country_dict import *

root = Tk()
root.title("Upravljanje aerodromom")
root.geometry("950x700")
root.resizable(0, 0)


def dimenzije_slike(path, length, height):
    """Menjanje dimenzija slika."""
    
    img = Image.open(path)
    img_resize = img.resize((length, height))
    return ImageTk.PhotoImage(img_resize)


def ciscenje_frejma(frame):
    """Funkcija koja briše sve elemente koje je dati frejm primio."""
    
    for element in frame.winfo_children():
        element.destroy()


def azuriranje_letova():
    """Ažuriranje spiska narednih letova."""
    
    ciscenje_frejma(letovi_frm)
    
    for i in range(len(linije.indeksi_narednih_letova())):
        # Podaci iz DataFrama koji su nam potrebni.
        idx = linije.indeksi_narednih_letova()[i]
        broj_leta = linije.linije_df["broj leta"][idx]
        destinacija = linije.linije_df.destinacija[idx]
        aerodrom = linije.linije_df["naziv aerodroma"][idx]
        tip_aviona = linije.linije_df["tip aviona"][idx]
        polazak = linije.linije_df.polazak[idx]
        polazak_str = polazak.strftime("%H:%M")

        # Smeštanje elemenata na formu.
        jedan_let_frm = ttk.Frame(letovi_frm)
        jedan_let_frm.grid(column=1, row=i, padx=5, pady=5)

        ttk.Label(jedan_let_frm, text="Let broj:").grid(column=1, row=0,
                                                        sticky=E)
        ttk.Label(jedan_let_frm, text="Destinacija:").grid(column=1, row=1,
                                                           sticky=E)
        ttk.Label(jedan_let_frm, text="Aerodrom:").grid(column=1, row=2,
                                                        sticky=E)
        ttk.Label(jedan_let_frm, text="Polazak:").grid(column=1, row=3,
                                                       sticky=E)
        ttk.Label(jedan_let_frm, text=broj_leta).grid(column=2, row=0,
                                                      sticky=W)
        ttk.Label(jedan_let_frm, text=destinacija).grid(column=2, row=1,
                                                        sticky=W)
        ttk.Label(jedan_let_frm, text=aerodrom, width=30).grid(column=2, row=2,
                                                               sticky=W)
        ttk.Label(jedan_let_frm, text=polazak_str).grid(column=2, row=3,
                                                        sticky=W)

        # Slika aviona.
        if tip_aviona == "AIRBUS A 330-200":
            slika = dimenzije_slike("assets/Airbus_A_330-200.png", 150, 52)
        elif tip_aviona == "AIRBUS A 320":
            slika = dimenzije_slike("assets/Airbus_A_320.png", 150, 52)
        elif tip_aviona == "AIRBUS A 319":
            slika = dimenzije_slike("assets/Airbus_A_319.png", 150, 52)
        elif tip_aviona == "ATR 72-600":
            slika = dimenzije_slike("assets/Atr_72_600.png", 150, 52)

        # Smeštanje slike na formu.
        slika_lbl = ttk.Label(letovi_frm, image=slika,
                              text=f"Tip aviona: {tip_aviona}", compound="top")
        slika_lbl.slika = slika
        slika_lbl.grid(column=0, row=i)
    
    letovi_frm.after(10000, azuriranje_letova)


def sortiranje(kriterijum, tv, sb, main):
    """Sortiranje izabranih kolona po izabranom kriterijumu i kreiranje
    treeview elementa na osnovu istog."""
    
    kolone = ["destinacija", "naziv aerodroma", "polazak", "trajanje leta",
              "osnovna cena karte"]
    
    # Dobijanje željenog spiska kolona i sortiranih podataka.
    krit = kolone.pop(kolone.index(kriterijum))
    kolone.insert(0, krit)

    df = linije.linije_df.loc[:, kolone].sort_values(by=[kriterijum])
    
    #Uklanjanje prethodnog treeview i scrollbar elementa i izgradnja novih.
    tv.grid_remove()
    sb.grid_remove()
    
    tv = ttk.Treeview(
        main,
        columns=kolone,
        show="headings",
        height=10
    )
    
    if kriterijum == "destinacija":
        # Imena zaglavlja
        tv.heading(kolone[0], text="Destinacija")
        tv.heading(kolone[1], text="Naziv aerodroam")
        tv.heading(kolone[2], text="Polazak")
        tv.heading(kolone[3], text="Trajanje")
        tv.heading(kolone[4], text="Cena")

        # Širina kolone i pozicija teksta u njoj.
        tv.column(kolone[0], width=100, anchor=W)
        tv.column(kolone[1], width=170, anchor=W)
        tv.column(kolone[2], width=70, anchor="center")
        tv.column(kolone[3], width=70, anchor="center")
        tv.column(kolone[4], width=100, anchor=E)
    
    elif kriterijum == "polazak":
        # Imena zaglavlja
        tv.heading(kolone[0], text="Polazak")
        tv.heading(kolone[1], text="Destinacija")
        tv.heading(kolone[2], text="Naziv aerodroam")
        tv.heading(kolone[3], text="Trajanje")
        tv.heading(kolone[4], text="Cena")

        # Širina kolone i pozicija teksta u njoj.
        tv.column(kolone[0], width=70, anchor="center")
        tv.column(kolone[1], width=100, anchor=W)
        tv.column(kolone[2], width=170, anchor=W)
        tv.column(kolone[3], width=70, anchor="center")
        tv.column(kolone[4], width=100, anchor=E)
        
    else:
        # Imena zaglavlja
        tv.heading(kolone[0], text="Trajanje")
        tv.heading(kolone[1], text="Destinacija")
        tv.heading(kolone[2], text="Naziv aerodroam")
        tv.heading(kolone[3], text="Polazak")
        tv.heading(kolone[4], text="Cena")

        # Širina kolone i pozicija teksta u njoj.
        tv.column(kolone[0], width=70, anchor="center")
        tv.column(kolone[1], width=100, anchor=W)
        tv.column(kolone[2], width=170, anchor=W)
        tv.column(kolone[3], width=70, anchor="center")
        tv.column(kolone[4], width=100, anchor=E)
    
    tv.grid(column=0, row=0, padx=10, pady=10, ipadx=5, ipady=5,
            columnspan=4)
    
    # Ubacivanje podataka u tabelu.
    for i in range(len(df)):
        indeksi = df.index.to_list()
        jedan_red = df.loc[indeksi[i]].to_list()

        # Redosled potrebnih indeksa.
        if kriterijum == "destinacija":
            idxs = [2, 3, 4]
        elif kriterijum == "polazak":
            idxs = [0, 3, 4]
        else:
            idxs = [3, 0, 4]

        jedan_red[idxs[0]] = jedan_red[idxs[0]].strftime("%H:%M")
        jedan_red[idxs[1]] = str(jedan_red[idxs[1]])[7:12]
        jedan_red[idxs[2]] = "%0.2f" % (float(jedan_red[idxs[2]]))
        tv.insert("", END, values=jedan_red)

    # Postavljanje skrolbara za Treeview.
    sb = ttk.Scrollbar(
        main,
        orient="vertical",
        command=tv.yview
    )
    tv.config(yscrollcommand=sb.set)
    sb.grid(column=4, row=0, sticky=NS)


def dest_eksport(df, rb_vrednost):
    """Eksportovanje fajla po destinacijama."""
    
    if rb_vrednost.get() == "1":
        df.to_excel("spisak_destinacija.xlsx")
    elif rb_vrednost.get() == "2":
        df.to_csv("spisak_destinacija.csv")
    elif rb_vrednost.get()== "3":
        df.to_json("spisak_destinacija.json")
    return messagebox.showinfo(
        title="Eksport podataka",
        message="Vaši podaci su uspešno sačuvani."
    )


def destinacije_graf(tip_var, krit_var, df):
    """Grafički prikaz najvećih i najmanjih vrednosti cena i trajanja leta
    destinacija."""
    
    kolone_lista = df.columns.to_list()
    
    trajanje_sort = df.loc[:,
                    kolone_lista].sort_values(by=["trajanje leta"],
                                              ascending=False)
    cene_sort = df.loc[:,
                kolone_lista].sort_values(by=["osnovna cena karte"],
                                          ascending=False)
    
    #Podaci destinacija i indeksa za najduže i najkraže letove.
    dest_duzina = []
    sortirani_d_indeksi = []
    for i in range(trajanje_sort.shape[0]):
        destin = trajanje_sort.destinacija.iloc[i]
        idx = trajanje_sort.index[i]
        if destin not in dest_duzina:
            dest_duzina.append(destin)
            sortirani_d_indeksi.append(idx)
    
    najduzi_letovi_destinacije = dest_duzina[0:5]
    najduzi_letovi_indeksi = sortirani_d_indeksi[0:5]
    najkraci_letovi_destinacije = list(reversed(dest_duzina))[0:5]
    najkraci_letovi_indeksi = list(reversed(sortirani_d_indeksi))[0:5]

    # Podaci destinacija i indeksa za najveće i najniže cene letova.
    dest_cena = []
    sortirani_c_indeksi = []
    for i in range(cene_sort.shape[0]):
        destin = cene_sort.destinacija.iloc[i]
        idx = cene_sort.index[i]
        if destin not in dest_cena:
            dest_cena.append(destin)
            sortirani_c_indeksi.append(idx)

    najvece_cene_destinacije = dest_cena[0:5]
    najvece_cene_indeksi = sortirani_c_indeksi[0:5]
    najmanje_cene_destinacije = list(reversed(dest_cena))[0:5]
    najmanje_cene_indeksi = list(reversed(sortirani_c_indeksi))[0:5]
    
    #Vrednost x_label je ista za sve.
    x_label = "Destinacija"
    
    # Vrednosti izbora tipa podataka (trajanje leta/cena karte):
    if tip_var.get() == "1":
        if krit_var.get() == "1":
            x_values = najduzi_letovi_destinacije
            x_values.reverse()
            y_values = []
            for indeks in najduzi_letovi_indeksi:
                y = str(trajanje_sort["trajanje leta"][
                            trajanje_sort.index == indeks].squeeze())[7:12]
                y_values.append(y)
            y_values.reverse()
            y_label = "Najduži letovi"
            naslov = "Destinacije kojima letovi traju najduže"
            color_bar = "peru"
            color_title = "saddlebrown"
            
        else:
            x_values = najkraci_letovi_destinacije
            y_values = []
            for indeks in najkraci_letovi_indeksi:
                y = str(trajanje_sort["trajanje leta"][
                            trajanje_sort.index == indeks].squeeze())[7:12]
                y_values.append(y)
            y_label = "Najkraći letovi"
            naslov = "Destinacije kojima letovi traju najkraće"
            color_bar = "peachpuff"
            color_title = "saddlebrown"
            
    else:
        if krit_var.get() == "1":
            x_values = najvece_cene_destinacije
            x_values.reverse()
            y_values = []
            for indeks in najvece_cene_indeksi:
                y = "%0.2f" % (float(cene_sort["osnovna cena karte"][
                                         cene_sort.index == indeks].squeeze()))
                y_values.append(y)
            y_values.reverse()
            y_label = "Najveće cene"
            naslov = "Destinacije kojima su cene karata najveće"
            color_bar = "purple"
            color_title = "indigo"
            
        else:
            x_values = najmanje_cene_destinacije
            y_values = []
            for indeks in najmanje_cene_indeksi:
                y = "%0.2f" % (float(cene_sort["osnovna cena karte"][
                                         cene_sort.index == indeks].squeeze()))
                y_values.append(y)
            y_label = "Najmanje cene"
            naslov = "Destinacije kojima su cene karata najmanje"
            color_bar = "mediumpurple"
            color_title = "indigo"
        
    plt.bar(x_values, y_values, color=color_bar)
    plt.title(naslov,
              fontdict={"family": "serif", "color": color_title, "size": 18})
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=80)
    plt.subplots_adjust(bottom=0.35)
    plt.subplots_adjust(left=0.2)
    plt.grid()

    plt.show()


def rez_dest_izbor():
    """Izbor destinacije koju želimo da rezervišemo."""
    dest_lista = []
    for i in range(linije.linije_df.shape[0]):
        destin = linije.linije_df.destinacija.iloc[i]
        if destin not in dest_lista:
            dest_lista.append(destin)
    return dest_lista


def linije_info():
    """Prikaz podataka o destinacijama, dužini leta i cenama."""
    
    def line_dest_selected(event):
        """Promene nakon unošenja destinacije."""
        dest_select = destinacije_cb.get()
        polazak_cb.set("")
        odrasli_sb.config(state="disabled")
        odrasli_sb.set(0)
        deca_sb.config(state="disabled")
        deca_sb.set(0)
        bebe_sb.config(state="disabled")
        bebe_sb.set(0)
        dolazak_val_lbl.config(text="")
        ukupna_cena_vrednost.config(text=0)
        
        polasci_line = linije.linije_df.polazak[
            linije.linije_df.destinacija == dest_select].to_list()
        lista_polazaka = [x.strftime("%H:%M") for x in polasci_line]
        polazak_cb.config(state="normal", values=lista_polazaka)
        
    def line_polazak_selected(event):
        """Promene koje se dešavaju nakon unošenja polaska za određenu
        destinaciju."""
        
        #Vrednosti za destinaciju i polazak i setovanje ostalih na početne
        # vrednosti.
        dest = destinacije_cb.get()
        polaz = polazak_cb.get()
        polazak = dt.datetime.strptime(polaz, "%H:%M").time()
        odrasli_sb.config(state="normal")
        odrasli_sb.set(0)
        deca_sb.config(state="normal")
        deca_sb.set(0)
        bebe_sb.config(state="normal")
        bebe_sb.set(0)
        ukupna_cena_vrednost.config(text=0)
        
        trajanje_za_dest = linije.linije_df["trajanje leta"][
            (linije.linije_df.destinacija == dest)]
        trajanje_leta = trajanje_za_dest.iloc[0]
        dolazak = (dt.datetime.combine(dt.date(1, 1, 1), polazak) +
                  trajanje_leta).time()
        dolazak_str = dolazak.strftime("%H:%M")

        dolazak_val_lbl.config(text=dolazak_str)
    
    def putnici_cena(event):
        """Cena za određeni broj putnika, uz popuste za mlađe uzraste."""

        dest = destinacije_cb.get()
        cena_za_dest = linije.linije_df["osnovna cena karte"][
            (linije.linije_df.destinacija == dest)]
        osnovna_cena = cena_za_dest.iloc[0]
        umnozak_odrasli = int(odrasli_sb.get())
        umnozak_deca = int(deca_sb.get())
        umnozak_bebe = int(bebe_sb.get())
        ukupna_cena = round(osnovna_cena * (umnozak_odrasli + umnozak_deca *
                                            0.95 + umnozak_bebe * 0.85), 2)
        ukupna_cena_vrednost.config(text="%0.2f" % ukupna_cena)


    #Deo za destinacije, polazak i dolazak.
    linije_tl = Toplevel(root)
    linije_tl.title("Destinacije - dužina letenja - cene")
    linije_tl.attributes("-topmost", "true")
    linije_tl.resizable(0, 0)
    
    destinacije_frm = ttk.Frame(linije_tl)
    destinacije_frm.grid(column=0, row=0, padx=10, pady=10)
    
    destinacije_lbl = ttk.Label(destinacije_frm, text="Izaberite destinaciju")
    destinacije_lbl.grid(column=0, row=0, padx=5, pady=5, sticky=W)
    destinacije_cb = ttk.Combobox(
        destinacije_frm,
        width=30,
        state="readonly",
        values=linije.lista_destinacija(),
    )
    destinacije_cb.grid(column=0, row=1, padx=5, pady=5, sticky=W)
    destinacije_cb.focus()
    destinacije_cb.bind("<<ComboboxSelected>>", line_dest_selected)
    
    polazak_lbl = ttk.Label(destinacije_frm, text="Izaberite polazak")
    polazak_lbl.grid(column=1, row=0, padx=5, pady=5, sticky=W)
    
    polazak_cb = ttk.Combobox(
        destinacije_frm,
        width=15,
        state="disabled",
    )
    polazak_cb.grid(column=1, row=1, padx=5, pady=5, sticky=W)
    polazak_cb.bind("<<ComboboxSelected>>", line_polazak_selected)
    
    dolazak_txt_lbl = ttk.Label(destinacije_frm, text="Dolazak")
    dolazak_txt_lbl.grid(column=2, row=0, padx=5, pady=5, sticky=W)
    
    dolazak_val_lbl = ttk.Label(destinacije_frm, width=15, borderwidth=1,
                                relief="solid", anchor=E)
    dolazak_val_lbl.grid(column=2, row=1, padx=5, pady=5, sticky=W)

    #Deo za cene.
    cene_frm = ttk.LabelFrame(linije_tl, text="Cena leta")
    cene_frm.grid(column=0, row=1, padx=10, pady=10)
    
    odrasli_lbl = ttk.Label(cene_frm, text="Odrasli")
    odrasli_lbl.grid(column=0, row=0, padx=5, pady=5, sticky=W)
    odrasli_sb = ttk.Spinbox(cene_frm, from_=0, to=10, width=15,
                             state="disabled")
    odrasli_sb.grid(column=0, row=1, padx=5, pady=5)
    odrasli_sb.set(0)
    odrasli_sb.bind("<ButtonRelease-1>", putnici_cena)

    deca_lbl = ttk.Label(cene_frm, text="Deca")
    deca_lbl.grid(column=1, row=0, padx=5, pady=5, sticky=W)
    deca_sb = ttk.Spinbox(cene_frm, from_=0, to=10, width=15, state="disabled")
    deca_sb.grid(column=1, row=1, padx=5, pady=5)
    deca_sb.set(0)
    deca_sb.bind("<ButtonRelease-1>", putnici_cena)

    bebe_lbl = ttk.Label(cene_frm, text="Bebe")
    bebe_lbl.grid(column=2, row=0, padx=5, pady=5, sticky=W)
    bebe_sb = ttk.Spinbox(cene_frm, from_=0, to=10, width=15, state="disabled")
    bebe_sb.grid(column=2, row=1, padx=5, pady=5)
    bebe_sb.set(0)
    bebe_sb.bind("<ButtonRelease-1>", putnici_cena)

    ukupna_cena_naslov = ttk.Label(cene_frm, text="Ukupno")
    ukupna_cena_naslov.grid(column=3, row=0, padx=5, pady=5, sticky=W)
    ukupna_cena_vrednost = ttk.Label(
        cene_frm,
        width=15,
        borderwidth=1,
        relief="solid",
        text=0,
        anchor=E)
    ukupna_cena_vrednost.grid(column=3, row=1, padx=5, pady=5)
    
    izadji_linije_btn = ttk.Button(
        linije_tl,
        text="Izađi",
        command=linije_tl.destroy
    )
    izadji_linije_btn.grid(column=0, row=2, padx=10, pady=10, sticky=E)


def rezervisanje():
    """Rezervacija karata. Izbor destinacije, podaci o putniku i cena
    karata."""

    def cb_dest_selected(event):
        """Promene koje se dešavaju nakon izbora destinacije u Comboboxu."""
        izabrana_dest = rez_dest_cb.get()
        rez_polazak_value.set("")
        rez_sediste_value.set("")
        rez_sediste_value.config(state="disabled")
        var_popunjenost.set("")
        rez_pasos_cb.set("")
        rez_pasos_cb.config(state="disabled")
        rez_putnik_value.config(text="")
        rez_drzava_value.config(text="")
        rez_starost_value.config(text="")
        rez_popust_value.config(text="")
        rezervisi_btn.config(state="disabled")
        ukupna_cena_value.config(text="0")
        
        polasci = linije.linije_df.polazak[
            linije.linije_df.destinacija == izabrana_dest].to_list()
        lista_pol = [x.strftime("%H:%M") for x in polasci]
        rez_polazak_value.config(state="normal", values=lista_pol)
        
    def cb_polazak_selected(event):
        """Promene koje se dešavaju nakon izbora vremena polaska."""
        rez_sediste_value.set("")
        var_popunjenost.set("")
        rez_pasos_cb.set("")
        rez_pasos_cb.config(state="disabled")
        rez_putnik_value.config(text="")
        rez_drzava_value.config(text="")
        rez_starost_value.config(text="")
        rez_popust_value.config(text="")
        rezervisi_btn.config(state="disabled")
        ukupna_cena_value.config(text="0")
        preostala_mesta = popunjenost(var_popunjenost)
        rez_sediste_value.config(state="normal", values=preostala_mesta)
    
    def cb_sediste_selected(event):
        """Promene koje se dešavaju nakon izbora sedišta."""
        id_pasosa = putnici.putnici_df["broj pasosa"].to_list()
        id_pasosa.sort()
        rez_pasos_cb.config(state="normal", values=id_pasosa)
    
    def cb_pasos_selected(event):
        """Nakon izbora ID pasoša, unošenje ostalih podataka o putniku,
        kao i cene karte."""
        
        rezervisi_btn.config(state="normal")
        
        #Podaci za unos.
        podaci_putnika = putnici.putnici_df[
            putnici.putnici_df["broj pasosa"] == rez_pasos_cb.get()]
        ime = podaci_putnika.iloc[0][1]
        drzava = podaci_putnika.iloc[0][3]
        godine = podaci_putnika.iloc[0][2]
        popust = podaci_putnika.iloc[0][6]
        iskoriscen = podaci_putnika.iloc[0][7]
        
        #Cena karte.
        if rez_dest_cb.get():
            osnovna_cena = linije.linije_df["osnovna cena karte"][
                linije.linije_df.destinacija == rez_dest_cb.get()]
            prvi_indeks = osnovna_cena.index[0]
            cena_bez_popusta = osnovna_cena[prvi_indeks]
            cena_bez_popusta_str = "%0.2f" % cena_bez_popusta
            cena_s_popustom = cena_bez_popusta * (1 - popust / 100)
            cena_s_popustom_str = "%0.2f" % cena_s_popustom
        
        rez_putnik_value.config(text=ime)
        rez_drzava_value.config(text=drzava)
        rez_starost_value.config(text=godine)
        
        #Proračuni za cenu s popustom i povratne karte (15% popusta za
        # povratak, tj. povratna = 1.85 * osnovna cena).
        if iskoriscen:
            rez_popust_value.config(text=0)
            if var_chbtn.get() == 0:
                ukupna_cena_value.config(text = cena_bez_popusta_str)
            else:
                cena_bez_popusta *= 1.85
                cena_bez_popusta_str = "%0.2f" % cena_bez_popusta
                ukupna_cena_value.config(text=cena_bez_popusta_str)
        else:
            rez_popust_value.config(text=popust)
            if var_chbtn.get() == 0:
                ukupna_cena_value.config(text= cena_s_popustom_str)
            else:
                cena_s_popustom *= 1.85
                cena_s_popustom_str = "%0.2f" % cena_s_popustom
                ukupna_cena_value.config(text=cena_s_popustom_str)
    
    def calendar_selected(event):
        """Promene nakon promene vrednosti datuma."""
        
        #Provera da li se bira datum pre današnjeg dana.
        if calend.get_date() < dt.date.today():
            messagebox.showerror(title="Greška",
                message="Ne možete da birate datume pre današnjeg dana.")
            calend.set_date(dt.date.today())
            
        if rez_dest_cb.get() and rez_polazak_value.get():
            preostala_mesta = popunjenost(var_popunjenost)
            rez_sediste_value.config(state="normal", values=preostala_mesta)
            
    
    def chbtn_change():
        """Promene koje se dešavaju nakon promene stanja Checkbox elementa,
        koji ukazuje da li se uzima povratna karta ili ne."""
        
        trenutna_cena = float(ukupna_cena_value.cget("text"))
        if var_chbtn.get() == 0:
             cena = "%0.2f" % (trenutna_cena / 1.85)
             ukupna_cena_value.config(text=cena)
        else:
            cena = "%0.2f" % (trenutna_cena * 1.85)
            ukupna_cena_value.config(text=cena)
    
    def prazna_mesta(ukupan_broj, min_v, max_v):
        """Funkcija za izračunavanje liste slobodnih mesta za zadate
        parametre."""
        
        sva_sedista = [x for x in range(1, ukupan_broj + 1)]
        
        #Procentualna popunjenost aviona.
        popuna_pct = random.randint(min_v, max_v)
        broj_preostalih_mesta = round((100 - popuna_pct) /  100 * ukupan_broj)
        preostala_mesta = random.sample(sva_sedista, k=broj_preostalih_mesta)
        preostala_mesta.sort()
        return preostala_mesta
    
    def popunjenost(var):
        """Interaktivno generisanje popunjenosti i praznih mesta (zbog
        obimnosti neophodnih podataka)."""

        dt_sada = dt.date.today()
        dt_izabran = calend.get_date()
        razlika = dt_izabran - dt_sada
        dest = rez_dest_cb.get()
        polaz = rez_polazak_value.get()
        polaz_dt = dt.datetime.strptime(polaz, "%H:%M").time()
        
        #Tip aviona za izabrane podatke.
        avion_tip = linije.linije_df[
            "tip aviona"][(linije.linije_df.destinacija == dest) & (
                linije.linije_df.polazak == polaz_dt)]
        avion_idx = avion_tip.index[0]
        avion = avion_tip[avion_idx]
        
        #Broj sedišta avioan.
        ukupno_sedista = avioni.avioni_df["kapacitet sedista"][
            avioni.avioni_df.tip == avion]
        ukupno_idx = ukupno_sedista.index[0]
        sedista = ukupno_sedista[ukupno_idx]
        
        preostala_sedista = []
        
        if razlika <= dt.timedelta(days=2):
            popunjeno_ver = random.randint(1, 100)
            if popunjeno_ver > 95:
                rez_popunjeno_value.config(foreground="green")
                var.set("DA")
                preostala_sedista = prazna_mesta(sedista, 85, 95)
            else:
                rez_popunjeno_value.config(foreground="red")
                var.set("NE")
        elif razlika <= dt.timedelta(days=4):
            popunjeno_ver = random.randint(1, 100)
            if popunjeno_ver > 80:
                rez_popunjeno_value.config(foreground="green")
                var.set("DA")
                preostala_sedista = prazna_mesta(sedista, 75, 85)
            else:
                rez_popunjeno_value.config(foreground="red")
                var.set("NE")
        elif razlika <= dt.timedelta(days=7):
            popunjeno_ver = random.randint(1, 100)
            if popunjeno_ver > 65:
                rez_popunjeno_value.config(foreground="green")
                var.set("DA")
                preostala_sedista = prazna_mesta(sedista, 50, 60)
            else:
                rez_popunjeno_value.config(foreground="red")
                var.set("NE")
        elif razlika <= dt.timedelta(days=10):
            popunjeno_ver = random.randint(1, 100)
            if popunjeno_ver > 50:
                rez_popunjeno_value.config(foreground="green")
                var.set("DA")
                preostala_sedista = prazna_mesta(sedista, 30, 45)
            else:
                rez_popunjeno_value.config(foreground="red")
                var.set("NE")
        else:
            rez_popunjeno_value.config(foreground="green")
            var.set("DA")
            preostala_sedista = prazna_mesta(sedista, 0, 0)
        return preostala_sedista

    def unos_rezervacije():
        """Unos podataka u tabelu 'rezervisanje'."""
        
        dest_rez = rez_dest_cb.get()
        date_rez = calend.get_date()
        polazak_rez = rez_polazak_value.get()
        sediste_rez = rez_sediste_value.get()
        pasos_rez = rez_pasos_cb.get()
        povratna_rez = var_chbtn.get()
        if povratna_rez == 1:
            povratna_bool = True
        else:
            povratna_bool = False
        cena_rez = float(ukupna_cena_value.cget("text"))
        
        rezervacije.unos_u_tabelu(dest_rez, date_rez, polazak_rez,
                                  sediste_rez, pasos_rez, povratna_bool,
                                  cena_rez)
    
    def novi_putnik():
        """Otvaranje novog prozora za unos informacija o putniku koji nije u
        bazi podataka"""

        def max_len_digit(input):
            """Ograničavanje dužine unosa u polje za broj pasoša i
            mogućnost da se samo koriste brojne vrednosti."""
            
            if input.isdigit() and len(input) <= 10:
                novi_ID_pass.config(text=input)
                return True
            elif input == "":
                return True
            else:
                return False
        
        def cb_drz_select(event):
            """Ubacivanje skraćenice države u ID pasoša."""
            
            for drzava in SHORT_COUNTRY_DICT:
                if drzava == novi_drzava_cb.get():
                    skracenica = SHORT_COUNTRY_DICT[drzava]
            novi_ID_abbr.config(text=skracenica)

        def unesi_novog_putnika():
            """Ubacivanje novog putnika, s relevantnim podacima, u tabelu
            'putnici'."""
            
            if not novi_ime_entry.get():
                return messagebox.showerror(
                    title="Greška",
                    message="Niste uneli ime i prezime putnika."
                )
            elif not novi_drzava_cb.get():
                return messagebox.showerror(
                    title="Greška",
                    message="Niste izabrali državljanstvo putnika."
                )
            elif not novi_pasos_entry.get():
                return messagebox.showerror(
                    title="Greška",
                    message="Niste uneli broj pasoša putnika."
                )
            elif not novi_starost_entry.get():
                return messagebox.showerror(
                    title="Greška",
                    message="Niste uneli starost putnika."
                )
            else:
                ime_i_prezime = novi_ime_entry.get()
                drzavljanstvo = novi_drzava_cb.get()
                broj_pasosa = novi_pasos_entry.get()
                godine = novi_starost_entry.get()
                skracenica_drzave = novi_ID_abbr.cget("text")
                id = f"{skracenica_drzave}-{broj_pasosa}"
                
                putnici.novi_putnik(id, ime_i_prezime, godine, drzavljanstvo)


        novi_tl = Toplevel(rezervacije_tl)
        novi_tl.title("UNOS PODATAKA O NOVOM PUTNIKU")
        novi_tl.attributes("-topmost", "true")
        novi_tl.resizable(0, 0)

        novi_ime_lbl = ttk.Label(novi_tl, text="Ime i prezime")
        novi_ime_lbl.grid(column=0, row=1, padx=10, pady=5, sticky=W)
        novi_ime_entry = ttk.Entry(novi_tl, width=30)
        novi_ime_entry.grid(column=0, row=2, padx=10, pady=5, sticky=W)

        novi_drzava_lbl = ttk.Label(novi_tl, text="Državljanstvo")
        novi_drzava_lbl.grid(column=1, row=1, padx=10, pady=5, sticky=W)
        novi_drzava_cb = ttk.Combobox(
            novi_tl,
            width=30,
            state="readonly",
            values=SHORT_COUNTRY_LIST
        )
        novi_drzava_cb.grid(column=1, row=2, padx=10, pady=5, sticky=W)
        novi_drzava_cb.bind("<<ComboboxSelected>>", cb_drz_select)

        novi_pasos_lbl = ttk.Label(novi_tl, text="Broj pasoša")
        novi_pasos_lbl.grid(column=2, row=1, padx=10, pady=5, sticky=W)
        reg = novi_tl.register(max_len_digit)
        novi_pasos_entry = ttk.Entry(novi_tl, width=15)
        novi_pasos_entry.grid(column=2, row=2, padx=10, pady=5, sticky=W)
        novi_pasos_entry.config(validate="key", validatecommand=(reg, '%P'))

        novi_starost_lbl = ttk.Label(novi_tl, text="Starost", anchor=E)
        novi_starost_lbl.grid(column=3, row=1, padx=10, pady=5, sticky=W)
        novi_starost_entry = ttk.Entry(novi_tl, width=10)
        novi_starost_entry.grid(column=3, row=2, padx=10, pady=5, sticky=W)
        
        id_frm = ttk.Frame(novi_tl)
        id_frm.grid(column=0, row=3, padx=10, pady=15, sticky=W)
        
        novi_ID_naslov = ttk.Label(id_frm, text="ID pasoša")
        novi_ID_naslov.grid(column=0, row=0, columnspan= 3, pady=5, sticky=W)
        novi_ID_abbr = ttk.Label(
            id_frm,
            width=4,
            font=("TkDefaultFont", 10, "bold")
        )
        novi_ID_abbr.grid(column=0, row=1, pady=5, sticky=E)
        novi_ID_dash = ttk.Label(
            id_frm,
            width=1,
            font=("TkDefaultFont", 10, "bold"),
            text="-"
        )
        novi_ID_dash.grid(column=1, row=1, pady=5)
        novi_ID_pass = ttk.Label(
            id_frm,
            width=12,
            font=("TkDefaultFont", 10, "bold")
        )
        novi_ID_pass.grid(column=2, row=1, pady=5, sticky=W)
        
        novi_unesi_btn = ttk.Button(
            novi_tl,
            text="Unesi",
            command=lambda : [
                unesi_novog_putnika(),
                novi_ime_entry.delete(0, "end"),
                novi_drzava_cb.set(""),
                novi_pasos_entry.delete(0, "end"),
                novi_starost_entry.delete(0, "end"),
                novi_ID_abbr.config(text=""),
                novi_ID_pass.config(text=""),
                messagebox.showinfo(
                    title="Uspešan unos",
                    message="Novi putnik uspešno unesen u bazu podataka.")]
        )
        novi_unesi_btn.grid(column=2, row=4, padx=10, pady=10, sticky=E)
        
        novi_izadjii_btn = ttk.Button(
            novi_tl,
            text="Izađi",
            command=novi_tl.destroy
        )
        novi_izadjii_btn.grid(column=3, row=4, padx=10, pady=10, sticky=E)


    rezervacije_tl = Toplevel(root)
    rezervacije_tl.title("REZERVACIJE KARATA")
    rezervacije_tl.resizable(0, 0)
    
    #Deo za destinaciju i datum putovanja.
    rez_dest_frm = ttk.LabelFrame(rezervacije_tl, text="Destinacija")
    rez_dest_frm.grid(column=0, row=0, columnspan=2, padx=10, pady=10,
                      sticky=EW)
    
    rez_dest_lbl = ttk.Label(rez_dest_frm, text="Izbor destinacije")
    rez_dest_lbl.grid(column=0, row=0, padx=5, pady=5, sticky=W)
    
    rez_dest_cb = ttk.Combobox(
        rez_dest_frm,
        state="readonly",
        values=rez_dest_izbor()
    )
    rez_dest_cb.grid(column=0, row=1, padx=5, pady=5, sticky=W)
    rez_dest_cb.focus()
    rez_dest_cb.bind("<<ComboboxSelected>>", cb_dest_selected)

    rez_datum_lbl = ttk.Label(rez_dest_frm, text="Datum")
    rez_datum_lbl.grid(column=1, row=0, padx=5, pady=5, sticky=W)
    calend = DateEntry(rez_dest_frm, selectmode="day",
                       date_pattern="dd/mm/yyyy")
    calend.grid(column=1, row=1, padx=5, pady=5, sticky=W)
    calend.bind("<<DateEntrySelected>>", calendar_selected)

    rez_polazak_title = ttk.Label(rez_dest_frm, text="Vreme polaska")
    rez_polazak_title.grid(column=2, row=0, padx=5, pady=5, sticky=W)
    rez_polazak_value = ttk.Combobox(rez_dest_frm, width=15, state="disabled")
    rez_polazak_value.grid(column=2, row=1, padx=5, pady=5, sticky=W)
    rez_polazak_value.bind("<<ComboboxSelected>>", cb_polazak_selected)

    rez_sediste_title = ttk.Label(rez_dest_frm, text="Broj sedišta")
    rez_sediste_title.grid(column=3, row=0, padx=5, pady=5, sticky=W)
    rez_sediste_value = ttk.Combobox(rez_dest_frm, width=10, state="disabled")
    rez_sediste_value.grid(column=3, row=1, padx=5, pady=5, sticky=W)
    rez_sediste_value.bind("<<ComboboxSelected>>", cb_sediste_selected)
    
    rez_popunjeno_title = ttk.Label(
        rez_dest_frm,
        text="Ima li slobodnih mesta?"
    )
    var_popunjenost = StringVar()
    rez_popunjeno_title.grid(column=4, row=0, padx=5, pady=5, sticky=W)
    rez_popunjeno_value = ttk.Label(
        rez_dest_frm,
        width=20,
        borderwidth=1,
        relief="solid",
        textvariable=var_popunjenost,
        anchor="center"
    )
    rez_popunjeno_value.grid(column=4, row=1, padx=5, pady=5, sticky=W)

    
    #Deo za informacije o putniku.
    rez_putnik_frm = ttk.LabelFrame(rezervacije_tl, text="Putnik")
    rez_putnik_frm.grid(column=0, row=1, columnspan=2, padx=10, pady=10,
                        sticky=EW)
    
    #Deo za putnika i informacije o njemu.
    rez_pasos_title = ttk.Label(rez_putnik_frm, text="ID pasoša")
    rez_pasos_title.grid(column=0, row=0, padx=5, pady=5, sticky=W)
    rez_pasos_cb = ttk.Combobox(rez_putnik_frm, width=15, state="disabled")
    rez_pasos_cb.grid(column=0, row=1, padx=5, pady=5, sticky=W)
    rez_pasos_cb.bind("<<ComboboxSelected>>", cb_pasos_selected)
    
    rez_putnik_lbl = ttk.Label(rez_putnik_frm, text="Ime i prezime")
    rez_putnik_lbl.grid(column=1, row=0, padx=5, pady=5, sticky=W)
    rez_putnik_value = ttk.Label(rez_putnik_frm, width=20, borderwidth=1,
                                 relief="solid")
    rez_putnik_value.grid(column=1, row=1, padx=5, pady=5, sticky=W)
    
    rez_drzava_title = ttk.Label(rez_putnik_frm, text="Državljanstvo")
    rez_drzava_title.grid(column=2, row=0, padx=5, pady=5, sticky=W)
    rez_drzava_value = ttk.Label(rez_putnik_frm, width=25, borderwidth=1,
                                relief="solid")
    rez_drzava_value.grid(column=2, row=1, padx=5, pady=5, sticky=W)
    
    rez_starost_title = ttk.Label(rez_putnik_frm, text="Starost")
    rez_starost_title.grid(column=3, row=0, padx=5, pady=5, sticky=W)
    rez_starost_value = ttk.Label(rez_putnik_frm, width=10, borderwidth=1,
                                relief="solid", anchor=E)
    rez_starost_value.grid(column=3, row=1, padx=5, pady=5, sticky=W)
    
    rez_popust_title = ttk.Label(rez_putnik_frm, text="Popust")
    rez_popust_title.grid(column=4, row=0, padx=5, pady=5, sticky=W)
    rez_popust_value = ttk.Label(rez_putnik_frm, width=10, borderwidth=1,
                                relief="solid", anchor=E)
    rez_popust_value.grid(column=4, row=1, padx=5, pady=5, sticky=W)
    
    rez_povratna_lbl = ttk.Label(rez_putnik_frm, text="Povratna karta")
    rez_povratna_lbl.grid(column=5, row=0, padx=5, pady=5, sticky=W)
    var_chbtn = IntVar()
    rez_povratna_chbtn = ttk.Checkbutton(
        rez_putnik_frm,
        text="povratna",
        variable=var_chbtn,
        onvalue=1,
        offvalue=0,
        command=chbtn_change
    )
    rez_povratna_chbtn.grid(column=5, row=1, padx=5, pady=5, sticky=W)
    rez_povratna_chbtn.state(["!alternate"])
    
    rezervisi_btn = ttk.Button(
        rez_putnik_frm,
        text="Rezerviši",
        state="disabled",
        command=lambda : [
            unos_rezervacije(),
            messagebox.showinfo(title="Rezervacija",
                                message="Rezervacija je uspešno izvršena.")
        ]
    )
    rezervisi_btn.grid(column=5, row=2, padx=5, pady=15, sticky=E)
    
    #Deo za novog putnika i ukupnu cenu karata.
    novi_putnik_frm = ttk.LabelFrame(rezervacije_tl, text="Novi putnik")
    novi_putnik_frm.grid(column=0, row=2, padx=10, pady=10, sticky=EW)
    novi_putnik_lbl = ttk.Label(novi_putnik_frm, text="Unos novog putnika")
    novi_putnik_lbl.grid(column=0, row=0, padx=5, pady=5, sticky=W)
    novi_putnik_btn = ttk.Button(
        novi_putnik_frm,
        text="Unos",
        command=novi_putnik
    )
    novi_putnik_btn.grid(column=1, row=0, padx=5, pady=5, sticky=E)

    ukupna_cena_frm = ttk.LabelFrame(rezervacije_tl, text="Ukupna cena")
    ukupna_cena_frm.grid(column=1, row=2, padx=10, pady=10, sticky=EW)
    ukupna_cena_title = ttk.Label(ukupna_cena_frm,
                                  text="Ukupna cena karate",
                                  width=25
                                  )
    ukupna_cena_title.grid(column=0, row=0, padx=5, pady=5, sticky=E)
    ukupna_cena_value = ttk.Label(ukupna_cena_frm,
                                  text="0",
                                  width=10,
                                  font=("Arial", 16, "bold"),
                                  borderwidth=1,
                                  relief="solid",
                                  anchor=E
                                  )
    ukupna_cena_value.grid(column=1, row=0, padx=5, pady=5, sticky=E)
    
    izadji_rez_btn = ttk.Button(rezervacije_tl,
                                 text="Izađi",
                                 command=rezervacije_tl.destroy
                                 )
    izadji_rez_btn.grid(column=1, row=3, padx=10, pady=10, sticky=E)


def letovi_do_kraja_dana():
    """Spisak svih letova do kraja dana iz tabele 'linije', sortiran po
    vremenu polaska."""
    
    preostali_letovi_df = linije.preostali_letovi()
    
    do_kraja_dana_tl = Toplevel(root)
    do_kraja_dana_tl.title("LETOVI DO KRAJA DANA")
    do_kraja_dana_tl.attributes("-topmost", "true")
    do_kraja_dana_tl.resizable(0, 0)
    
    #Naslov.
    do_kraja_dana_lbl = ttk.Label(
        do_kraja_dana_tl,
        text="Spisak letova do kraja dana".upper(),
        font=("Calibri", 22, "bold"),
        background="grey80",
        foreground="darkblue",
        relief="raised",
        anchor="center"
    )
    do_kraja_dana_lbl.grid(column=0, row=0, padx=20, pady=20, ipadx=10,
                           ipady=10, sticky=EW)
    
    #Kolone Treeview forme su nazivi kolona tabele 'linije'.
    kolone = preostali_letovi_df.columns.to_list()
    
    preostali_tv = ttk.Treeview(
        do_kraja_dana_tl,
        columns=kolone,
        show="headings",
        height=20
    )
    
    # Imena zaglavlja.
    preostali_tv.heading("broj leta", text="Broj leta")
    preostali_tv.heading("tip aviona", text="Tip aviona")
    preostali_tv.heading("destinacija", text="Destinacija")
    preostali_tv.heading("naziv aerodroma", text="Naziv aerodroma")
    preostali_tv.heading("polazak", text="Polazak")
    preostali_tv.heading("trajanje leta", text="Trajanje")
    preostali_tv.heading("osnovna cena karte", text="Osnovna cena")
    
    #Širina kolone i pozicija teksta u njoj.
    preostali_tv.column("broj leta", width=50, anchor="center")
    preostali_tv.column("tip aviona", width=130, anchor=W)
    preostali_tv.column("destinacija", width=100, anchor=W)
    preostali_tv.column("naziv aerodroma", width=170, anchor=W)
    preostali_tv.column("polazak", width=70, anchor="center")
    preostali_tv.column("trajanje leta", width=70, anchor="center")
    preostali_tv.column("osnovna cena karte", width=100, anchor=E)
    
    preostali_tv.grid(column=0, row=1, padx=10, pady=10, ipadx=5, ipady=5)
    
    #Ubacivanje podataka u tabelu.
    for i in range(len(preostali_letovi_df)):
        indeksi = preostali_letovi_df.index.to_list()
        jedan_red = preostali_letovi_df.loc[indeksi[i]].to_list()
        jedan_red[4] = jedan_red[4].strftime("%H:%M")
        jedan_red[5] = str(jedan_red[5])[7:12]
        jedan_red[6] = "%0.2f" % (float(jedan_red[6]))
        preostali_tv.insert("", END, values=jedan_red)
    
    #Postavljanje skrolbara za Treeview.
    scroll = ttk.Scrollbar(do_kraja_dana_tl, orient="vertical",
                           command=preostali_tv.yview)
    preostali_tv.config(yscrollcommand=scroll.set)
    scroll.grid(column=1, row=1, sticky=NS)
    
    #Dugme za zatvaranje prozora.
    izadji_preostali_btn = ttk.Button(do_kraja_dana_tl, text="Izađi",
                                      command=do_kraja_dana_tl.destroy)
    izadji_preostali_btn.grid(column=0, row=2, padx=10, pady=10, sticky=E)


def putnici_info():
    """Prikaz tabele 'putnici', s mogućnošću eksportovanja podataka o njima
    i grafičkim prikazima pojedinih podataka"""
    
    putnici_tl = Toplevel(root)
    putnici_tl.title("INFORMACIJE O PUTNICIMA")
    putnici_tl.resizable(0, 0)
    
    #Deo za eksportovanje tabele u excel, csv ili json format.
    eksport_frm = ttk.LabelFrame(
        putnici_tl,
        text="Eksportovanje podataka o putnicima"
    )
    eksport_frm.grid(column=0, row=0, padx=10, pady=10)

    ime_fajla_lbl = ttk.Label(eksport_frm, text="Unesite ime fajla")
    ime_fajla_lbl.grid(column=0, row=0, pady=5, padx=5, sticky=W)
    ime_fajla_entry = ttk.Entry(eksport_frm)
    ime_fajla_entry.grid(column=0, row=1, pady=5, padx=5, sticky=W)

    rd_buttons = {"excel": "1", "csv": "2", "json": "3"}
    var_eksport = StringVar(eksport_frm)
    for (tekst, vrednost) in rd_buttons.items():
        ttk.Radiobutton(eksport_frm,
                        text=tekst,
                        variable=var_eksport,
                        value=vrednost
                        ).grid(row=(int(vrednost) + 1), padx=5, pady=2,
                               sticky=W)
    var_eksport.set("1")

    prihvati_btn = ttk.Button(eksport_frm, text="Prihvati",
        command=lambda : [putnici.eksportovanje(var_eksport.get(),
                                               ime_fajla_entry),
                         ime_fajla_entry.delete(0, END),
                         ime_fajla_entry.focus()])
    prihvati_btn.grid(column=0, row=5, padx=5, pady=10, sticky=E)
    
    ime_fajla_entry.focus()

    #Deo za grafički prikaz.
    prikaz_frm = ttk.LabelFrame(putnici_tl, text="Grafički prikaz podataka")
    prikaz_frm.grid(column=1, row=0, padx=10, pady=10)
    
    #Izbor tipa podataka za prikazivanje.
    tip_frm = ttk.LabelFrame(prikaz_frm, text="Tip podataka")
    tip_frm.grid(column=0, row=0, padx=10, pady=10)
    
    tip_dict = {
        "Najzastupljenija država": "1",
        "Najviše letova": "2",
        "Najveća kilometraža": "3"
    }
    var_tip = StringVar(tip_frm)
    for (tekst, vrednost) in tip_dict.items():
        ttk.Radiobutton(tip_frm,
                        text=tekst,
                        variable=var_tip,
                        value=vrednost).grid(row=(int(vrednost) - 1),
                                             padx=5, pady=5, sticky=W)
    var_tip.set("1")
    
    #Izbor načina prikazivanja podataka.
    nacin_frm = ttk.LabelFrame(prikaz_frm, text="Vrsta grafika")
    nacin_frm.grid(column=1, row=0, padx=10, pady=10)

    nacin_dict = {"Bar": "1", "Pie": "2"}
    var_nacin = StringVar(nacin_frm)
    for (tekst, vrednost) in nacin_dict.items():
        ttk.Radiobutton(nacin_frm,
                        text=tekst,
                        variable=var_nacin,
                        value=vrednost).grid(row=(int(vrednost) - 1),
                                             padx=5, pady=5, sticky=W)
    var_nacin.set("1")
    
    #Broj podataka za prikazivanje.
    broj_frm =ttk.LabelFrame(prikaz_frm, text="Broj podataka")
    broj_frm.grid(column=2, row=0, padx=10, pady=10)

    broj_dict = {"5": "1", "7": "2", "10": "3"}
    var_broj = StringVar(broj_frm)
    for (tekst, vrednost) in broj_dict.items():
        ttk.Radiobutton(broj_frm, text=tekst, variable=var_broj,
                        value=vrednost).grid(row=(int(vrednost) - 1), padx=5,
                                             pady=5, sticky=W)
    var_broj.set("1")

    primeni_btn = ttk.Button(prikaz_frm, text="Primeni",
        command=lambda: putnici.graficki_prikaz(var_tip, var_nacin, var_broj))
    primeni_btn.grid(column=2, row=1, padx=10, pady=10, sticky=E)

    izadji_btn = ttk.Button(putnici_tl, text="Izađi",
                            command=putnici_tl.destroy)
    izadji_btn.grid(column=1, row=1, padx=10, pady=10, sticky=E)


def flota_info():
    """Prikaz informacija o svakom avionu iz flote."""
    
    flota_tl = Toplevel(root)
    flota_tl.title("INFORMACIJE O RASPOLOŽIVIM AVIONIMA")
    flota_tl.attributes("-topmost", "true")
    flota_tl.resizable(0, 0)
    
    flota_frm = ttk.Frame(flota_tl)
    flota_frm.grid(column=0, row=1, padx=30, pady=30)
    
    flota_naslov_lbl = ttk.Label(
        flota_tl,
        text="INFORMACIJE O AVIONIMA",
        font=("Calibri", 22, "bold"),
        background="grey80",
        foreground="royalblue",
        relief="raised",
        anchor="center"
    )
    flota_naslov_lbl.grid(column=0, row=0, padx=20, pady=20, ipadx=10,
                          ipady=10, sticky=EW)
    
    #Kreiranje slike.
    for i in range(4):
        tip = avioni.avioni_df.tip.iloc[i]
        if tip == "AIRBUS A 330-200":
            slika = dimenzije_slike("assets/Airbus_A_330-200.png", 300, 105)
        elif tip == "AIRBUS A 320":
            slika = dimenzije_slike("assets/Airbus_A_320.png", 300, 105)
        elif tip == "AIRBUS A 319":
            slika = dimenzije_slike("assets/Airbus_A_319.png", 300, 105)
        elif tip == "ATR 72-600":
            slika = dimenzije_slike("assets/Atr_72_600.png", 300, 105)
        
        #Smeštanje slike na formu.
        slika_lbl = ttk.Label(flota_frm, image=slika)
        slika_lbl.slika = slika
        slika_lbl.grid(column=i, row=0, padx=5, pady=5)
        
        #Ispisivanje tipa aviona.
        tip_aviona_lbl = ttk.Label(
            flota_frm,
            text=tip,
            font=("Arial", 18, "bold"),
            background="royalblue",
            foreground="white",
            padding=15,
            width=25,
            anchor="center"
        )
        tip_aviona_lbl.grid(column=i, row=1)
        
        ukupno_aviona = avioni.avioni_df.ukupno.iloc[i]
        ukupno_suma_stringa = len(str(ukupno_aviona) + "Ukupno aviona")
        ukupno_spaces = 30 - ukupno_suma_stringa
        ukupno_str = "Ukupno aviona" + " " * ukupno_spaces + str(ukupno_aviona)
        ukupno_aviona_lbl = ttk.Label(
            flota_frm,
            text=ukupno_str,
            font=("Courier", 14),
            padding=10,
            width=30
        )
        ukupno_aviona_lbl.grid(column=i, row=2, padx=10, sticky=W)
        
        duzina_aviona = avioni.avioni_df.duzina.iloc[i]
        duzina_suma_stringa = len(str(duzina_aviona) + "Dužina aviona") + 2
        duzina_spaces = 30 - duzina_suma_stringa
        duzina_str = "Dužina aviona" + " " * duzina_spaces + str(
            duzina_aviona) + " m"
        duzina_aviona_lbl = ttk.Label(
            flota_frm,
            text=duzina_str,
            font=("Courier", 14),
            padding=10,
            width=30
        )
        duzina_aviona_lbl.grid(column=i, row=3, padx=10, sticky=W)
        
        raspon_krila = avioni.avioni_df["raspon krila"].iloc[i]
        raspon_suma_stringa = len(str(raspon_krila) + "Raspon krila") + 2
        raspon_spaces = 30 - raspon_suma_stringa
        raspon_str = "Raspon krila" + " " * raspon_spaces + str(
            raspon_krila) + " m"
        
        raspon_krila_lbl = ttk.Label(
            flota_frm,
            text=raspon_str,
            font=("Courier", 14),
            padding=10,
            width=30
        )
        raspon_krila_lbl.grid(column=i, row=4, padx=10, sticky=W)
        
        kapacitet_sedista = avioni.avioni_df["kapacitet sedista"].iloc[i]
        sedista_suma_string = len(str(kapacitet_sedista) + "Kapacitet sedišta")
        sedista_spaces = 30 - sedista_suma_string
        sedista_str = "Kapacitet sedišta" + " " * sedista_spaces + str(
            kapacitet_sedista)
        
        kapacitet_sedista_lbl = ttk.Label(
            flota_frm,
            text=sedista_str,
            font=("Courier", 14),
            padding=10,
            width=30
        )
        kapacitet_sedista_lbl.grid(column=i, row=5, padx=10, sticky=W)
        
        brzina_krstarenja = round(avioni.avioni_df[
                                      "brzina krstarenja"].iloc[i])
        brzina_suma_string = len(str(brzina_krstarenja) +
                                 "Brzina krstarenja") + 5
        brzina_spaces = 30 - brzina_suma_string
        brzina_str = "Brzina krstarenja" + " " * brzina_spaces + str(
            brzina_krstarenja) + " km/h"
        
        brzina_krstarenja_lbl = ttk.Label(
            flota_frm,
            text=brzina_str,
            font=("Courier", 14),
            padding=10,
            width=30
        )
        brzina_krstarenja_lbl.grid(column=i, row=6, padx=10, sticky=W)
        
        visina_krstarenja = avioni.avioni_df["visina krstarenja"].iloc[i]
        visina_suma_string = len(str(visina_krstarenja) +
                                 "Visina krstarenja") + 2
        visina_spaces = 30 - visina_suma_string
        visina_str = "Visina krstarenja" + " " * visina_spaces + str(
            visina_krstarenja) + " m"
        
        visina_krstarenja_lbl = ttk.Label(
            flota_frm,
            text=visina_str,
            font=("Courier", 14),
            padding=10,
            width=30
        )
        visina_krstarenja_lbl.grid(column=i, row=7, padx=10, sticky=W)
    
    flota_izadji_btn = ttk.Button(
        flota_frm,
        text="Izađi",
        command=flota_tl.destroy
    )
    flota_izadji_btn.grid(column=3, row=8, padx=10, pady=20, sticky=E)


def spisak_destinacija():
    """Spisak svih destinacija s nazivom aerodroma, vremenom polaska,
    trajanjem leta i cenom. Izbor sortiranja spiska po destinaciji, vremenu
    polaska i trajanju leta. Eksport u excel fajl."""
    
    dest_df = linije.linije_df.loc[:, ("destinacija", "naziv aerodroma",
                                       "polazak", "trajanje leta",
                                       "osnovna cena karte")].sort_values(by=["destinacija"])
    
    spisak_tl = Toplevel(root)
    spisak_tl.title("SPISAK SVIH DESTINACIJA")
    spisak_tl.resizable(0, 0)
    
    # Naslov.
    spisak_naslov_lbl = ttk.Label(
        spisak_tl,
        text="SPISAK SVIH DESTINACIJA",
        font=("Calibri", 22, "bold"),
        background="grey80",
        foreground="darkblue",
        relief="raised",
        anchor="center"
    )
    spisak_naslov_lbl.grid(column=0, row=0, padx=20, pady=20, ipadx=10,
                           ipady=10, sticky=EW)
    
    spisak_frm = ttk.Frame(spisak_tl)
    spisak_frm.grid(column=0, row=1, padx=30, pady=30, sticky=EW)
    
    #Kolone koje se koriste u Treeview formi.
    lista_kolona = dest_df.columns.to_list()
    
    spisak_tv = ttk.Treeview(
        spisak_frm,
        columns=lista_kolona,
        show="headings",
        height=10
    )
    
    #Imena zaglavlja
    spisak_tv.heading("destinacija", text="Destinacija")
    spisak_tv.heading("naziv aerodroma", text="Naziv aerodroam")
    spisak_tv.heading("polazak", text="Polazak")
    spisak_tv.heading("trajanje leta", text="Trajanje")
    spisak_tv.heading("osnovna cena karte", text="Cena")
    
    #Širina kolone i pozicija teksta u njoj.
    spisak_tv.column("destinacija", width=100, anchor=W)
    spisak_tv.column("naziv aerodroma", width=170, anchor=W)
    spisak_tv.column("polazak", width=70, anchor="center")
    spisak_tv.column("trajanje leta", width=70, anchor="center")
    spisak_tv.column("osnovna cena karte", width=100, anchor=E)
    
    spisak_tv.grid(column=0, row=0, padx=10, pady=10, ipadx=5, ipady=5,
                   columnspan=4)
    
    # Ubacivanje podataka u tabelu.
    for i in range(len(dest_df)):
        indeksi = dest_df.index.to_list()
        jedan_red = dest_df.loc[indeksi[i]].to_list()
        jedan_red[2] = jedan_red[2].strftime("%H:%M")
        jedan_red[3] = str(jedan_red[3])[7:12]
        jedan_red[4] = "%0.2f" % (float(jedan_red[4]))
        spisak_tv.insert("", END, values=jedan_red)
        
    #Postavljanje skrolbara za Treeview.
    scroll = ttk.Scrollbar(
        spisak_frm,
        orient="vertical",
        command=spisak_tv.yview
    )
    spisak_tv.config(yscrollcommand=scroll.set)
    scroll.grid(column=4, row=0, sticky=NS)
    
    #Elementi za različiti načini sortiranja.
    sortiranje_lbl = ttk.Label(
        spisak_frm,
        text="Izaberite sortiranje leta po:"
    )
    sortiranje_lbl.grid(column=0, row=1, padx=5, pady=5, sticky=E)
    
    sort_dest_btn = ttk.Button(
        spisak_frm,
        text="Destinaciji",
        command=lambda : sortiranje("destinacija", spisak_tv, scroll,
                                    spisak_frm)
    )
    sort_dest_btn.grid(column=1, row=1, padx=5, pady=5)

    sort_polaz_btn = ttk.Button(
        spisak_frm,
        text="Polasku",
        command=lambda : sortiranje("polazak", spisak_tv, scroll, spisak_frm)
    )
    sort_polaz_btn.grid(column=2, row=1, padx=5, pady=5)

    sort_traj_btn = ttk.Button(
        spisak_frm,
        text="Trajanju",
        command=lambda : sortiranje("trajanje leta", spisak_tv, scroll,
                                    spisak_frm)
    )
    sort_traj_btn.grid(column=3, row=1, padx=5, pady=5)
    
    #Grafički prikaz za trajanje leta i cene.
    graf_frm = ttk.LabelFrame(
        spisak_frm,
        text="Eksportovanje i grafički prikaz"
    )
    graf_frm.grid(column=0, row=2, columnspan=4, padx=30, pady=20, sticky=EW)

    #Deo za eksportovanje tabele u excel, csv ili json format.
    eksport_spisak_frm = ttk.LabelFrame(
        graf_frm,
        text="Eksportovanje tabele sa destinacijama"
    )
    eksport_spisak_frm.grid(column=0, row=0, padx=10, pady=10)
    
    eksport_dict = {"excel": "1", "csv": "2", "json": "3"}
    var_eksp = StringVar(eksport_spisak_frm)
    
    for (tekst, vrednost) in eksport_dict.items():
        ttk.Radiobutton(
            eksport_spisak_frm,
            text=tekst,
            variable=var_eksp,
            value=vrednost).grid(row=(int(vrednost) + 1), padx=5, pady=2,
                                 sticky=W)
    var_eksp.set("1")
    
    eksportuj_btn = ttk.Button(
        graf_frm,
        text="Eksportuj",
        command=lambda : dest_eksport(dest_df, var_eksp)
    )
    eksportuj_btn.grid(column=0, row=1, padx=5, pady=10, sticky=E)
    
    trajanje_cena_frm = ttk.LabelFrame(graf_frm, text="Tip podataka")
    trajanje_cena_frm.grid(column=1, row=0, padx=10, pady=10)
    
    trajanje_cena_dict = {"Trajanje leta": "1", "Cena karte": "2"}
    var_trajanje_cena = StringVar(trajanje_cena_frm)
    
    for (tekst, vrednost) in trajanje_cena_dict.items():
        ttk.Radiobutton(
            trajanje_cena_frm,
            text=tekst,
            variable=var_trajanje_cena,
            value=vrednost
        ).grid(row=(int(vrednost) - 1), padx=5, pady=5, sticky=W)
    
    var_trajanje_cena.set("1")
    
    #Izbor kriterijuma za određeni tip podataka.
    krit_frm = ttk.LabelFrame(graf_frm, text="Kriterijum")
    krit_frm.grid(column=2, row=0, padx=10, pady=10)
    
    krit_dict = {"Najveće": "1", "Najmanje": "2"}
    var_krit = StringVar(krit_frm)
    
    for (tekst, vrednost) in krit_dict.items():
        ttk.Radiobutton(
            krit_frm,
            text=tekst,
            variable=var_krit,
            value=vrednost
        ).grid(row=(int(vrednost) - 1), padx=5, pady=5, sticky=W)
    
    var_krit.set("1")

    primeni_btn = ttk.Button(
        graf_frm,
        text="Primeni",
        command=lambda : destinacije_graf(var_trajanje_cena, var_krit, dest_df)
    )
    primeni_btn.grid(column=2, row=1, padx=5, pady=10, sticky=E)

    #Dugme za zatvaranje.
    spisak_izadji_btn = ttk.Button(
        spisak_tl,
        text="Izađi",
        command=spisak_tl.destroy
    )
    spisak_izadji_btn.grid(column=0, row=3, padx=30, pady=30, sticky=E)


naslov_lbl = ttk.Label(root,
                       text="Aerodrom \"Nikola Tesla\"",
                       background="grey80",
                       foreground="maroon",
                       font=("Cambria", 32, "bold"),
                       anchor="center",
                       borderwidth=1,
                       relief="raised"
                       )
naslov_lbl.grid(column=0,
                row=0,
                columnspan=2,
                padx=20,
                pady=20,
                ipadx=20,
                ipady=20
                )

info_frm = ttk.LabelFrame(root, text="Izbor informacija")
info_frm.grid(column=0, row=1, padx=20, pady=20, ipady=5, sticky=NS)

#Menjanje stila za velika slova na glavnom ekranu.
style = ttk.Style()
style.configure("big.TButton", font=("Arial", 18, "bold"))

linije_btn = ttk.Button(
    info_frm,
    text="INFORMACIJE O LINIJAMA",
    style="big.TButton",
    width=30,
    command=lambda : linije_info()
)
linije_btn.grid(column=0, row=0, padx=15, pady=5, ipady=10)

rezervacije_btn = ttk.Button(
    info_frm,
    text="REZERVACIJE",
    style="big.TButton",
    width=30,
    command=lambda : rezervisanje()
)
rezervacije_btn.grid(column=0, row=1, padx=15, pady=5, ipady=10)

letovi_btn = ttk.Button(
    info_frm,
    text="LETOVI DO KRAJA DANA",
    style="big.TButton",
    width=30,
    command=letovi_do_kraja_dana
)
letovi_btn.grid(column=0, row=2, padx=15, pady=5, ipady=10)

putnici_btn = ttk.Button(
    info_frm,
    text="PUTNICI",
    style="big.TButton",
    width=30,
    command=putnici_info
)
putnici_btn.grid(column=0, row=3, padx=15, pady=5, ipady=10)

flota_btn = ttk.Button(
    info_frm,
    text="PODACI O FLOTI",
    style="big.TButton",
    width=30,
    command=flota_info
)
flota_btn.grid(column=0, row=4, padx=15, pady=5, ipady=10)

destinacije_btn = ttk.Button(
    info_frm,
    text="SPISAK DESTINACIJA",
    style="big.TButton",
    width=30,
    command=spisak_destinacija
)
destinacije_btn.grid(column=0, row=5, padx=15, pady=5, ipady=10)

letovi_frm = ttk.LabelFrame(root, text="Narednih pet letova")
letovi_frm.grid(column=1, row=1, padx=20, pady=20, ipady=5, sticky=EW)

for i in range(len(linije.indeksi_narednih_letova())):
    # Podaci iz DataFrama koji su nam potrebni.
    idx = linije.indeksi_narednih_letova()[i]
    broj_leta = linije.linije_df["broj leta"][idx]
    destinacija = linije.linije_df.destinacija[idx]
    aerodrom = linije.linije_df["naziv aerodroma"][idx]
    tip_aviona = linije.linije_df["tip aviona"][idx]
    polazak = linije.linije_df.polazak[idx]
    polazak_str = polazak.strftime("%H:%M")
    
    # Smeštanje elemenata na formu.
    jedan_let_frm = ttk.Frame(letovi_frm)
    jedan_let_frm.grid(column=1, row=i, padx=5, pady=5)
    
    ttk.Label(jedan_let_frm, text="Let broj:").grid(column=1, row=0, sticky=E)
    ttk.Label(jedan_let_frm, text="Destinacija:").grid(column=1, row=1,
                                                       sticky=E)
    ttk.Label(jedan_let_frm, text="Aerodrom:").grid(column=1, row=2, sticky=E)
    ttk.Label(jedan_let_frm, text="Polazak:").grid(column=1, row=3, sticky=E)
    ttk.Label(jedan_let_frm, text=broj_leta).grid(column=2, row=0, sticky=W)
    ttk.Label(jedan_let_frm, text=destinacija).grid(column=2, row=1, sticky=W)
    ttk.Label(jedan_let_frm, text=aerodrom, width=30).grid(column=2, row=2,
                                                           sticky=W)
    ttk.Label(jedan_let_frm, text=polazak_str).grid(column=2, row=3, sticky=W)
    
    # Slika aviona.
    if tip_aviona == "AIRBUS A 330-200":
        slika = dimenzije_slike("assets/Airbus_A_330-200.png", 150, 52)
    elif tip_aviona == "AIRBUS A 320":
        slika = dimenzije_slike("assets/Airbus_A_320.png", 150, 52)
    elif tip_aviona == "AIRBUS A 319":
        slika = dimenzije_slike("assets/Airbus_A_319.png", 150, 52)
    elif tip_aviona == "ATR 72-600":
        slika = dimenzije_slike("assets/Atr_72_600.png", 150, 52)
    
    # Smeštanje slike na formu.
    slika_lbl = ttk.Label(letovi_frm, image=slika,
                          text=f"Tip aviona: {tip_aviona}", compound="top")
    slika_lbl.slika = slika
    slika_lbl.grid(column=0, row=i)

zatvori_btn = ttk.Button(
    root,
    text="Zatvori",
    command=lambda : [root.destroy(), rezervacije.brisanje_rezervacija()]
)
zatvori_btn.grid(column=1, row=2, padx=15, pady=5, sticky=E)

azuriranje_letova()

root.mainloop()
