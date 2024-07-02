# 1. Naslov projekta
    UPRAVLJANJE AERODROMOM

# 2. Kratak opis projekta
Projekat je urađen kao sastavni deo kursa "Python Developer - Advanced" u 
kompaniji **ITOiP** (IT Obuka i Praksa - https://itoip.rs).

Ovaj projakat je zamišljen kao pojednostavljena verzija poslova koje bi 
jedan aerodrom mogao da radi. Neki podaci su realni i uzeti su sa sajta 
https://www.airserbia.com/, dok je ostalo kreirano po slobodnoj volji.

Aplikacija je urađena u Pythonu, uz pomoć PostgreSQL sistema za upravljanje 
bazama podataka.

Tabele koje su urađene kao primer nalaze se u arhivi 'tables.zip', a 
primeri eksportovanih fajlova nalaze se u arhivi 'exported.zip'.

# 3. Sadržaj README.md fajla
#### 1. Naslov projekta
#### 2. Kratak opis projekta
#### 3. Sadržaj README.md fajla
#### 4. Baza podataka i struktura tabela
#### 5. Kako koristiti aplikaciju

# 4. Baza podataka i struktura tabela
Naziv baze podataka: "aerodrom"

Tabele:

    AVIONI (modifikovani podaci uzeti su sa gore navedenog sajta)
        tip                 (varchar (20), primary key, not null)
            #tip aviona
        ukupno              (integer, not null)     #ukupno aviona tog tipa
        duzina              (float, not null)       #u metrima
        raspon krila        (float, not null)       #u metrima
        kapacitet sedista   (integer, not null)     #ukupan broj sedišta
        brzina krstarenja   (float, not null)       #u km/h
        visina krstarenja   (integer, not null)     #u metrima

    LINIJE (pojednostavljeni podaci uzeti su sa gore navedenog sajta)
        broj leta           (integer, primary key, not null)
        tip aviona          (varchar (20), not null)
        destinacija         (varchar (20), not null)
        naziv aerodroma     (varchar (30), not null)
        polazak             (time, not null)
        trajanje leta       (interval, not null)
        osnovna cena karte  (integer, not null)     #u dinarima

    PUTNICI
        broj pasosa         (varchar(20), primary key, not null)
            #sa skraćenicom države iz koje je putnik
        ime i prezime       (varchar(30), not null)
        starost             (integer, not null)
        drzavljanstvo       (varchar(30), not null)
        broj ranijih letova (integer, not null)
        kilometraza         (integer, not null)
        popust              (integer, not null)     #u procentima
        iskoriscen popust   (boolean, not null)

    REZERVACIJE
        "broj rezervisanje"  (serial, primary key, not null)
        destinacija         (varchar (20), not null)
        datum               (date, not null)
        polazak             (time, not null)
        numeracija sedista  (varchar(3), not null)
        broj pasosa         (varchar(20), not null)
        povratna karta      (boolean, not null)
        cena rezervisanje    (float, not null)        #u dinarima
            #cena karte zavisi od popusta, starosti i da li je povratna
# 5. Kako koristiti aplikaciju

## 5.1. Glavni ekran

Glavni ekran, ispod naslova aerodroma, podeljen je u dva dela. Prvi je 
'Izbor informacija', koji sadrži dugmad za izbor informacija, dok je drugi, 
'Narednih pet letova', prikaz sledećih letova, s osnovnim podacima o njima.

Na dnu imamo dugme koje zatvara aplikaciju i briše podatke iz tabele 
'rezervacije'.

#### 5.1.1 Izbor informacija

U ovom delu imamo 6 dugmeta koja otvaraju nove prozore, u skladu s 
nazivom svakog dugmeta.

#### 5.1.2 Narednih pet letova

Drugi deo ekrana prikazuje informacije o narednih 5 letova. Prvo su 
prikazani tip aviona za taj let, sa svojom slikom, a nakon toga su podaci o 
broju leta, destinaciji na koju se leti, nazivu aerodroma na koji se ide i 
vremenom polaska.

Podaci se interaktivno smenjuje, tj. kada prođe vreme za poletanje leta, 
podaci se ažuriraju i stvara se nova lista.

NAPOMENA: Prilikom svakog novog iscrtavanja elemenata na formi za
prikazivanje narednih 5 letova, slika trepne. Budući da je prvobitno 
postavljeno da se ažuriranje forme vrši na 1 sekundu (1000 ms), to je bilo 
primetno. Zbog toga je vreme ažuriranja povećano na 10 sekundi. Slika još 
uvek trepće, ali je to mnogo manje izraženo. Nuspojava ovakvog setovanja je 
da se forma nekada ne ažurira odmah, nego nakon nekoliko sekundi po isteku 
vremena polaska.

## 5.2. Informacije o linijama

Novi ekran nam daje mogućnost da izabremo destinaciju. Pre izbora 
destinacije nije moguće unositi druge podatke. Kada se izabere destinacija 
polje za izbor polazaka postaje dostupno, s relevantnim vremenima polazaka.

Pošto se izabere i vreme polaska, automatski se upisuje vreme dolaska i 
otključavaju ostala (spinbox) polja.

Drugi, donji deo ekrana, pod nazivom 'Cene leta' ostavljaju mogućnost da se 
izabere broj putnika, koji su podeljeni u kategorije: 'Odrasli', 'Deca' i 
'Bebe'.

Dok biramo putnike, interaktivno se dobija cena za ukupan broj svih 
izabranih kategorija, tako da neko može da vidi kolika bi cena bila za više 
putnika. Putnici su podeljeni u ove kategorije zato što deca, od 3 do 11 
godina, imaju popust od 5%, a bebe, starosti do 2 godine, popust od 15%.

Ako izaberemo novi polazak za istu destinaciju (ukoliko ima više polazaka), 
svi elementi u delu 'Cena leta' se resetuju, uključujući i cenu. Izborom 
nove destinacije, pak, resetuju se svi ostali podaci.

Na dnu imamo dugme 'Izađi' koje zatvara ovaj prozor.

## 5.3. Rezervacije

Rezervacija je posebna kategorija u ovom programu, jer se ne oslanja na 
podatke iz tabele, iako tabela 'rezervacije' postoji, ona je prazna 
prilikom svakog pokretanja aplikacije, budući da se briše prilikom svakog 
zatvaranja (ako se izvrši pritiskom dugmeta 'Zatvori'). Podaci se kreiraju 
_interaktivno_, jer ne samo što bi obim podataka morao da bude mnogo veći, 
nego bi podaci o rezervacijama bili zastareli kada se aplikacija pokrene 
nakon određenog vremena.

Ekran koji se otvori, podeljen je u tri osnovne kategorije. Prvo imamo 
podatke povezane s destinacijom, onda podakte povezane s putnicima iz baze 
podataka, a na kraju tu je deo za unos novih putnika koji nisu u bazi.

#### 5.3.1 Destinacija

Ovde su u početku dostupni samo izbori za destinaciju i datum. Nije moguće 
izabrati datum pre današnjeg dana, jer se ništa ne rezerviše za prošlo 
vreme. Informacija o grešci nas o tome obaveštava, ukoliko ipak pokušamo to da 
izvedemo.

Nakon izbora destinacije iz padajućeg menija, postaje dostupan i padajući 
meni s vremenima polazaka za tu destinaciju. Kada izaberemo vreme polaska, 
dobijamo informaciju da li ima slobodnih mesta. Ukoliko ih nema, lista 
broja sedišta je prazna, a ukoliko ih ima, program generiše određeni broj 
mesta. Generisani podaci su podešeni tako da je manja verovatnoća za 
nalaženje slobodnih mesta za ranije datume, a veća za kasnije.

Ukoliko slobodnih mesta nema, potrebno je izabrati novi datum ili novo 
vreme, dok ne dobijemo odgovor da slobodnih mesta ima.

After the seat numbering is selected, a drop-down menu becomes available to 
select passengers already in the database.

Prilikom izbora nove destinacije, svi podaci se, osim datuma i izbora za 
povratnu kartu, resetuju.

Takođe, prilikom izbora novog polaska, resetuju se svi podaci, osim 
destinacije, datuma i izbora za povratnu kartu.

#### 5.3.2 Putnici i cene karata

Kada padajući meni 'ID pasoša' postane dostupan, moguće je izabrati bilo 
kog putnika iz tabele 'putnici'. Izborom putnika upisuju se svi ostali 
podaci iz baze podataka potrebni za kreiranje cene karte, kao i osnovni 
podaci o putniku. Cena se, takođe, automatski upisuje, a njena vrednost 
može da varira u odnosu na osnovnu cenu u zavisnosti od toga da li postoji 
popust i da li se uzima povratna karta.

Svi potrebni podaci ubacuju se u tabelu 'rezervacije' pritiskom na dugme 
'Rezerviši'. Inače, ovo dugme _nije dostupno_ dok nema svih potrebnih podataka.

_Popusti_:

Kao što je već ranije pomenuto, deca starosti 3-11 godina imaju popust od 
5%, a bebe, starosti od 1 ili 2 godine imaju popust od 15%.

Moguće je da putnici dobiju popust na kilometražu koju su prešli s ovom 
kompanijom. Oni koji su prešli više od 10.000 km dobijaju popust od 5%, a 
oni koji su prešli više od 20.000 km dobijaju popust od 10%. Međutim, ovaj 
popust ne traje stalno. Popust može da se koristi ukoliko već nije 
iskorišćen, a da li se to desilo pokazuje nam vrednost iz kolone 'iskoriscen 
popust' u tabeli 'putnici'. Iskorišćeni popust se na ekranu prikazuje 
_kao da ga nema_ (vrednost popusta je 0).

Popust se dobija i na povratnu kartu. On iznosi 15% na udvostručenu osnovnu 
cenu karte.

Popusti se kombinuju, tj. jedan popust ne isključuje drugi.

#### 5.3.3 Novih putnici u bazi podataka

Prilikom pritska na dugme 'Unos' u delu za novog putnika otvara se nova 
forma. Na ovoj form upisuje se ime i prezime novog putnika, broj pasoša (ne 
ceo ID pasoša) i starost, a državljanstvo se bira iz padajućeg menija.

Izborom državljanstva ažurira se ID pasoša upisivanjem skraženice države na 
početak.

Upisivanje broja pasoša ograničava nas samo na unos brojnih vrednosti i ne 
dozvoljava da broj pasoša bude duži od 10 karaktera. Takođe, tokom unošenja 
broja pasoša, interaktivno se ažurira drugi deo ID pasoša.

Kada su svi podaci popunjeni, pritiskom na dugme 'Unesi', u tabelu 'putnici' 
upisuje se novi putnik sa svim potrebnim podacima.

Nakon obaveštenja o uspešnom unosu podataka, svi podaci se brišu i polja su 
spremna za novi unos.

## 5.4 Letovi do kraja dana

Na ovoj formi se, u obliku tabele, daje spisak svih preostalih letova do 
kraja dana. Tu su i druge informacije o tim letovima: broj leta, tip aviona,
naziv aerodroma na koji se dolazi, vreme polaska, vreme trajanja leta i 
osnovna cena karte leta.

## 5.5 Putnici

Ovde se otvara prozor s dva odvojena dela. Prvi deo odnosi se na mogućnost 
eksportovanja fajla, sa svim podacima o putnicima iz tabele 'putnici'. 
Eksportovanje se izborom opcije vrši u formate Excel, CSV i JSON.

U polje za unos imena fajla unosi se naziv kojim želimo da imenujemo taj 
fajl, bez potrebe da se unosi ekstenzija. Nakon uspešnog eksportovanja, 
dobijamo obaveštenje o izvršenoj operaciji, a vrednost u polju za unos se 
briše.

Drugi deo odnosi se na grafički prikaz podataka o putnicima. Postoje izbori 
za tip podataka, vrstu grafika i broj prikazanih podataka. Tip podataka 
daje nam izbor između najvećeg broja putnika iz pojedine države, putnika 
koji imaju najviše letova ili putnika koji su prošli najveću kilometražu. 
Vrsta grafika daje nam izbor da li ćemo podatke prikazati u formi 'bar' 
ili 'pie'. Broj prikazanih podataka određuje koliko vrednosti će biti 
prikazano na grafiku. Svi izbori deluju _združeno_, a rezultat dobijamo 
pritiskom na dugme 'Primeni'.

## 5.6 Podaci o floti

Na pritisak ovog dugmeta na glavnom ekranu, otvara se novi s prikazom 
raspoloživih aviona, njihovim slikama i osnovnim podacima o njima. Od 
podataka tu su: tip aviona, koliko ukupno aviona takvog tipa ima, kolika im 
je dužina, raspon krila, kapacitet sedišta, kolika je brzina krstarenja i 
visina na kojoj lete.

## 5.7 Spisak destinacija

Na dnu je dugme za spisak destinacija. Otvaranjem novog prozora dobijaju 
se tabelarni podaci o destinacijama na koje se leti s nazivom aerodroma na 
koji se sleće, polaskom, trajanjem leta i osnovnom cenom karte.

Dobijeni podaci mogu da se sortiraju na tri načina: po destinacijama na 
koje se leti, po vremenu polaska i po vremenu trajanja leta.

Osim toga, podaci mogu da se eksportuju u formatima Excel, CSV i JSON, a 
naziv eksportovanog fajla je 'spisak_destinacija'.

Takođe, moguće je grafički prikazati podatke o trajanju leta i ceni, na 
takav način da se dobije stubični grafik 5 destinacija s najdužom ili 
najkraćom dužinom leta, kao i 5 destinacija s najvećom ili najmanjom cenom 
karte.
