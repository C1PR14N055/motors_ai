# MOTORS.AI 🧠🚙

## About this project

`Artificial Intelligence` powered cars `crawler`, tracks the cars market prices, make assumptions about cars, show statistics.

### TODO list

-   [x] Crawl cars on autovit
-   [x] Categorize cars into custom format for scalability
-   [ ] Normalize, scale, splint data into bins
-   [ ] Machine Leaning price prediction / stats / charts
-   [ ] Flask API
-   [ ] Frontend
-   [ ] Raspberry Pi case + HDD for storage

### Setup

#### Linux

```zsh
$ sudo apt install python3
$: pip3 install virtualenv
$: source venv/bin/activate
$: pip3 install -r requirements.txt
$: python3 run.py
```

#### OSX

```zsh
$: brew install python3
$: pip3 install virtualenv
$: source venv/bin/activate
$: pip3 install -r requirements.txt
$: python3 run.py
```

### Future milestones

0. MVP (Version 1.0):

    - cars crawler, cars with price indicator (bad, average, cheap, "castana" 🌰)

1. Version 2.0:

    - crawl and keep data, in 5 years verify cars app by internet history (+ VIN?)

2. Version 3.0:

    - pwa cars at good prices app free (with ads)
    - with device / browser ident, and custom install instructions
    - subscription for instant car news

3. Version 4.0:
    - verified by apo authorized mechanic (like uber drivers, with stars rating)
