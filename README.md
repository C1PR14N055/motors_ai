# MOTORS.AI 🏎️ 🏍️ 🧠

`Artificial Intelligence` powered car ads `crawler`:

-   Tracks cars market prices
-   Makes assumptions about cars & shows statistics
-   ???
-   Profit

### Setup and run

#### Linux

```zsh
$ sudo apt install python3
$ pip3 install virtualenv
$ mkdir venv && python3 -m venv ./venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 run.py
```

#### OSX

```zsh
$ brew install python3
$ pip3 install virtualenv
$ mkdir venv && virtualenv -p python3 ./venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 run.py
```

### Todo list

-   [x] Crawl cars on autovit
-   [x] Categorize cars into custom format for scalability
-   [x] Split data into bins, normalize, scale
-   [x] Visualize data, create plots
-   [ ] Machine-Leaning price prediction / stats / charts
-   [ ] Multi-Threading, scrape continuously (within req. limits) while training continuously
-   [ ] Flask Backend API
-   [ ] Frontend static with jQuery or vanilla.js
-   [ ] Dockerize
-   [ ] Mini-server w/ Raspberry Pi + 3D Case + ext. HDD

### Future milestones

#### - Version 1.0 (MVP):

    - cars crawler
    - stats, price indicator (bad, average, cheap, "castana" 🌰)

#### - Version 2.0:

    - crawl and keep data, in 5 years verify cars app by internet history (+ VIN?)

#### - Version 3.0:

    - pwa cars at good prices app free (with ads)
    - with device / browser ident, and custom install instructions
    - subscription for instant car news

#### - Version 4.0:

    - verified by app authorized mechanic (like uber drivers, with star ratings)
