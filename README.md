# 1. Project title
    AIRPORT MANAGEMENT

# 2. Brief description of the project
The project was done as an integral part of the course "Python Developer - 
Advanced" in the company **ITOiP** (IT Training and Practice - 
https://itoip.rs).

This project is intended as a simplified version of the jobs that would
one airport could work. Some data are real and taken from the site 
https://www.airserbia.com/, while the rest was created by free will.

The application was made in Python, with the help of the PostgreSQL 
database management system.

Tables made as an example are in the archive 'tables.zip', and examples of 
exported files are in the archive 'exported.zip'.

# 3. The README.md file contents
#### 1. Project title
#### 2. Brief description of the project
#### 3. The README.md file contents
#### 4. Database and table structure
#### 5. Application description and usage

# 4. Database and table structure
Database name: "aerodrom"

Tables:

    avioni (modified data taken from the above site)
        tip                 (varchar (20), primary key, not null)
                                                    # aircraft type
        ukupno              (integer, not null)     # total aircrafts
        duzina              (float, not null)       # in meters
        raspon krila        (float, not null)       # in meters
        kapacitet sedista   (integer, not null)     # total number of seats
        brzina krstarenja   (float, not null)       # in km/h
        visina krstarenja   (integer, not null)     # in meters

    linije (simplified data is taken from the above site)
        broj leta           (integer, primary key, not null)  # flight number
        tip aviona          (varchar (20), not null)          # aircraft type
        destinacija         (varchar (20), not null)          # destination
        naziv aerodroma     (varchar (30), not null)          # airport
        polazak             (time, not null)                  # departure
        trajanje leta       (interval, not null)              # flight duration
        osnovna cena karte  (integer, not null)               # ticket price

    putnici
        broj pasosa         (varchar(20), primary key, not null)
                        # passport number with the abbreviation of the country
        ime i prezime       (varchar(30), not null) # passenger's full name
        starost             (integer, not null)     # passenger's age
        drzavljanstvo       (varchar(30), not null) # citizenship
        broj ranijih letova (integer, not null)     # previous flights number
        kilometraza         (integer, not null)     # mileage
        popust              (integer, not null)     # percentage discount
        iskoriscen popust   (boolean, not null)     # used discount

    rezervacije
        broj rezeracije     (serial, primary key, not null) # reservation no.
        destinacija         (varchar (20), not null)        # destination
        datum               (date, not null)                # date
        polazak             (time, not null)                # departure
        numeracija sedista  (varchar(3), not null)          # seat numbering
        broj pasosa         (varchar(20), not null)         # passport number
        povratna karta      (boolean, not null)             # round-trip ticket
        cena rezervisanje    (float, not null)              # reservation price

# 5. Application description and usage

## 5.1. Main Screen

The main screen, below the airport heading, is divided into two parts. The 
first one is 'Information Selection', which contains buttons for selecting 
information, while the second one, 'Next Five Flights', is a display of the 
next flights, with basic information about them.

![1 - Main Screen](https://github.com/kdkrle/airport_management/assets/59825527/3d2e1faa-1b57-4087-a79e-2193a07c9a85)

_Picture 1: Main Screen_

At the bottom we have a button that closes the application and deletes the 
data from the 'rezervacije' (reservations) table.

#### 5.1.1 Information Selection

In this section we have 6 buttons that open new windows, according to the 
name of each button.

#### 5.1.2 Next Five Flights

The second part of the screen shows information about the next 5 flights. 
First, it is shown the aircraft type for that specific flight, with its 
picture, followed by information about the flight number, the destination, 
the name of the airport, and the time of departure.

Data is changed interactively, i.e. when it's time for the plane to take off,
the data is updated and a new list is created.

NOTE: At each new drawing of elements on the form on which the next 5 
flights are displayed, the image blinks. Since the form was originally set 
to update every 1 second (1000 ms), this was noticeable. Therefore, the 
update time has been increased to 10 seconds. The image still blinks, but it's 
much less noticeable. The side effect of this setting is that sometimes the 
form is not updated immediately, but after a few seconds after the 
departure time has expired.

## 5.2. Line information

The new screen gives us the option to choose a destination. It is not 
possible to enter other data before selecting the destination. Once the 
destination is selected, the departure selection field becomes available, 
with the relevant departure times.

![2 - Line Information](https://github.com/kdkrle/airport_management/assets/59825527/be9ed1fb-1762-4f4b-912d-b3fadcf0c32b)

_Picture 2: Line Information_

Since the departure time is also selected, the arrival time is 
automatically entered and the other (Spinbox) fields are unlocked.

The second, lower part of the screen, called 'Flight prices' allows you to 
choose the number of passengers, which are divided into categories: 
'Adults', 'Children' and 'Babies'.

As we select passengers, the price for the total number of all selected 
categories is interactively obtained, so that one can see what the price 
would be for more passengers. Passengers are divided into these categories 
because children, from 3 to 11 years, have a discount of 5%, and babies, 
aged up to 2 years, a discount of 15%.

If we choose a new departure for the same destination (if there are 
multiple departures), all elements in the 'Flight price' section are reset, 
including the price. Selecting a new destination resets all other data.

At the bottom we have an 'Izađi' (Exit) button which closes this window.

## 5.3. Reservations

Reservation is a special category in this program, because it does not rely 
on table data, although the 'reservation' table exists, it is empty every 
time the application is started, since it is deleted every time it is 
closed (if it is done by pressing the 'Zatvori' (Close) button). The data 
is created _interactively_, because not only the amount of data would have 
to be much larger, but the booking data would be out of date when the 
application is launched after a certain amount of time.

![3 - Reservations](https://github.com/kdkrle/airport_management/assets/59825527/d25575c5-69f3-45ad-8b8a-5c0ac3ad0ee6)

_Picture 3: Reservations_

The screen that has been opened is divided into three basic categories. 
First we have data related to the destination, then data related to 
passengers from the database, and finally there is a part for entering new 
passengers who are not in the database.

#### 5.3.1 Destination

Only destination and date choices are initially available here. It is not 
possible to choose a date before today, because reservations are not made 
for the time that has passed. The error information informs us about it, if 
we still try to perform it.

After selecting a destination from the drop-down menu, a drop-down menu 
with departure times for that destination becomes available. When we choose 
the time of departure, we receive information on whether there are any 
available seats. If there are none, the list of seats is empty, and if 
there are, the program generates a certain number of seats. The generated 
data is adjusted so that the probability of finding free places is lower 
for earlier dates and higher for later ones.

If there are no vacant seats, it is necessary to choose a new date or a new 
time, until we receive an answer that there are vacant seats.

After the seat numbering is selected, a drop-down menu becomes available to 
select passengers who are already in the database.

When choosing a new destination, all data is reset, except for the date and 
selection for the return ticket.

Also, when selecting a new departure, all data is reset, except for the 
destination, date and selection for the return ticket.

#### 5.3.2 Passengers and ticket prices

When the 'ID pasoša' (Passport ID) drop-down menu becomes available, it is 
possible to select any passenger from the 'putnici' (passengers) table. By 
selecting a passenger, all other data from the database needed to create 
the ticket price, as well as basic data about the passenger, are displayed. 
The price is also entered automatically, and its value may vary from the 
base price depending on whether there is a discount and whether a return 
ticket is taken.

All the necessary data are inserted into the 'rezervacije' (reservations) 
table by pressing the 'Rezerviši' (Reserve) button. Otherwise, this button 
is _not available_ until all required data has been entered.

_Discounts_:

As mentioned before, children aged 3-11 years have a 5% discount, and 
babies aged 1 or 2 years have a 15% discount.

It is possible for passengers to get a discount on the mileage they have 
traveled with this company. Those who have traveled more than 10,000 km get 
a 5% discount, and those who have traveled more than 20,000 km get a 10% 
discount. However, this discount does not last permanently. The discount 
can be used if it has not already been used, and whether this has happened 
we can see by the value from the 'iskoriscen popust' (discount used) column 
in the 'putnici' (passengers) table. The used discount is displayed on the 
screen _as if it doesn't exist_ (discount value is 0).

A discount is also available on the return ticket. It amounts to 15% on 
double the basic price of the ticket.

Discounts are combined, i.e. one discount does not exclude the other.

#### 5.3.3 New passengers in the database

When pressing the 'Unos' (Enter) button in the new passenger section, a new 
form opens. On this form, the new passenger's first and last name, passport 
number (not the full passport ID) and age are entered, and the nationality 
is selected from the drop-down menu.

![4 - New Passenger](https://github.com/kdkrle/airport_management/assets/59825527/9ef2c306-c07b-457a-90e5-892cfbd058e0)

_Picture 4: New Passengers_

By selecting the citizenship, the Passport ID is updated by writing the 
abbreviation of the country at the beginning.

Entering the passport number limits us only to entering numerical values 
and does not allow the passport number to be longer than 10 characters. 
Also, while entering the passport number, the second part of the passport 
ID is updated interactively.

When all the data is filled in, by pressing the 'Unesi' (Enter) button, a new 
passenger with all the necessary data is entered in the 'putnici' (passengers) 
table.

After notification of successful data entry, all data is deleted and the 
fields are ready for new entry.

## 5.4 Flights until the end of the day

This screen provides a list of all remaining flights to the end of the day 
in the form of a table. There is also other information about those 
flights: flight number, type of aircraft, name of the airport of arrival, 
time of departure, duration of the flight and the basic price of the flight 
ticket.

![5 - Flight List](https://github.com/kdkrle/airport_management/assets/59825527/eb724bac-b63b-4c3e-a63f-274f2cbf2b2a)

_Picture 5: List of Flights Until the End of the Day_

## 5.5 Passengers

This opens a window with two separate sections. The first section refers to 
the possibility of exporting a file, with all data about passengers from 
the table 'putnici' (passengers). By selecting the option, export is done 
in Excel, CSV and JSON formats.

![6 - Passenger Information](https://github.com/kdkrle/airport_management/assets/59825527/2b8054c0-78e6-4b01-9696-fd383cd26785)

_Picture 6: Passenger Information_

In the field for entering the name of the file, we enter the name we want 
to name that file with, without the need to enter the extension. After a 
successful export, we receive a notification about the performed operation, 
and the value in the input field is deleted.

The second part refers to the graphic display of passenger data. There are 
choices for data type, chart type, and number of data displayed. The data 
type gives us a choice between the largest number of passengers from a 
particular country, passengers with the most flights, or passengers with 
the most mileage. The graph type gives us a choice whether to display the 
data in 'bar' or 'pie' form. The number of displayed data determines how 
many values will be displayed on the chart. All choices work _together_, 
and we get the result by pressing the 'Primeni' (Apply) button.

![6 1 - Most Passengers Country](https://github.com/kdkrle/airport_management/assets/59825527/de69e101-e92c-4c0a-9f8a-555be8a373df)

_Picture 7: Countries With the Most Passengers (bar)_

![6 2 - Most Flights Passsengers](https://github.com/kdkrle/airport_management/assets/59825527/9c66aa6e-790d-41d9-880e-02197c02530e)

_Picture 8: Passengers With the Most Flights_

![6 3 - Highest Mileage Passengers](https://github.com/kdkrle/airport_management/assets/59825527/83cb96c3-e3a4-4cf4-95c7-2f5b7bc21f7d)

_Picture 9: Passengers With the Highest Mileage_

![6 4 - Most Passengers Country (pie)](https://github.com/kdkrle/airport_management/assets/59825527/93e1c6c0-1bdd-4bd2-a26b-47d771f48315)

_Pictures 10: Countries With the Most Passengers (pie)_

## 5.6 Fleet data

Pressing this button on the main screen opens a new one with a display of 
available aircraft, their images and basic information about them. The data 
includes: the type of aircraft, how many aircraft of that type there are in 
total, their length, wingspan, seat capacity, cruise speed and altitude at 
which they fly.

![7 - Fleet Data](https://github.com/kdkrle/airport_management/assets/59825527/8aa32478-dbf6-44a2-bd6e-5b1cfa127201)

_Picture 11: Fleet data_

## 5.7 Destination List

At the bottom is a button for a list of destinations. By opening a new 
window, tabular data on the destinations to which you fly are obtained with 
the name of the airport where you land, the departure, the duration of the 
flight and the basic price of the ticket.

![8 - Destination List](https://github.com/kdkrle/airport_management/assets/59825527/a722e0d3-a41e-474c-8e88-23805b4e93f9)

_Picture 12: Destination List_

The obtained data can be sorted in three ways: by destinations, by 
departure time and by flight duration.

In addition, data can be exported in Excel, CSV and JSON formats, and the 
name of the exported file is 'spisak_destinacila' (destination list).

Also, it is possible to graphically display data on flight duration and 
price, in such a way as to obtain a bar chart of 5 destinations with the 
longest or shortest flight length, as well as 5 destinations with the 
highest or lowest ticket price.

![8 1 - Longest Flights](https://github.com/kdkrle/airport_management/assets/59825527/7e2f635a-d1af-46d6-a080-9b1b6a0e5720)

_Picture 13: Longest Flights_

![8 2 - Shortest Flights](https://github.com/kdkrle/airport_management/assets/59825527/3730ed3c-3677-4873-b0cb-8ed124af5469)

_Picture 14: Shortest Flights_

![8 3 - Highest Prices](https://github.com/kdkrle/airport_management/assets/59825527/9552c0e9-7f93-4261-8333-aebfd3c72959)

_Picture 15: Highest Prices_

![8 4 - Lowest Prices](https://github.com/kdkrle/airport_management/assets/59825527/6c5ed38f-b981-4c9d-887c-fe2c569eb33a)

_Picture 16: Lowest Prices_
