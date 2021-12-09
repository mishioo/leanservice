[![Build status](https://ci.appveyor.com/api/projects/status/ujxrfksccqa8e4rl?svg=true)](https://ci.appveyor.com/project/mishioo/leanservice)
[![Coverage Status](https://coveralls.io/repos/github/mishioo/leanservice/badge.svg?branch=main)](https://coveralls.io/github/mishioo/leanservice?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# leanservice
Niniejsze repozytorium powstało jako rozwiązania zadania rekrutacyjnego od Kuby z
LeanCode. Jest to implementacja niewielkiej aplikacji typu JSON API, która losuje post z
obrazkiem z wybranego subreddita oraz przechowuje historię losowania.

Aplikacja udostępnia dwa endpointy:

`/random` - `GET` zwraca link do losowego obrazka z portalu reddit.com, z wybranego
subreddita. Subreddit, jak i metodę losowania można wybrać poprzez query string, za
pomocą parametrów odpowiednio "sub" i "listing". Jeśli parametr nie został podany,
używana jest wartość domyślna, którą można wybrać, umieszczając pozycję odpowiednio
DEFAULT_SUBREDDIT i DEFAULT_LISTING w pliku konfiguracyjnym ".env". Wszystkie poprawnie
zwrócone linki zapisywane są w bazie danych do późniejszego odczytania.

`/history` - `GET` zwraca listę wszystkich wylosowanych dotąd obrazków.

Dodatkowo dostępny jest też endpoint `/docs` zawierający automatycznie wygenerowaną
dokumentację API.

## Tech stack
Do stworzenia tej aplikacji wykorzystałem dobrze mi znany język Python oraz
asynchroniczny framework [FastAPI](https://fastapi.tiangolo.com/), świetnie
wykorzystujący zalety współczesnego Pythona. Do komunikacji z bazą danych wybrałem
popularną bibliotekę ORM [SQLAlchemy](https://www.sqlalchemy.org/).

## Uruchomienie
0. TL;DR co mam wkleić w terminal?:

    ```bash
    sudo add-apt-repository universe
    sudo apt update
    sudo apt install git
    sudo apt install python3-pip
    sudo apt install python3-venv
    git clone https://github.com/mishioo/leanservice.git
    cd leanservice
    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements.txt
    echo "DATABASE_URL=sqlite+aiosqlite:////./history.db" > .env
    uvicorn leanservice.main:app
    ```

1. Zainstaluj `git` i manager paczek Pythona (`pip`):

    ```
    sudo add-apt-repository universe
    sudo apt update
    sudo apt install git
    sudo apt install python3-pip
    ```
    W podstawowej dystrybucji Ubuntu nie znajduje się `git` potrzebny do sklonowania
    repozytorium, ani `pip` niezbędny do instalacji dodatkowych paczek z PyPI.

2. Sklonuj repozytorium z aplikacją:

    ```bash
    git clone https://github.com/mishioo/leanservice.git
    cd leanservice
    ```

3. Opcjonalnie (zalecane) - przygotuj wirtualne środowisko:

    ```bash
    sudo apt install python3-venv
    python3 -m venv venv
    source venv/bin/activate
    ```
    Zakładając, że ten krok został wykonany, odpowiednią instalację Pythona można
    wywołać poleceniem `python`, bez wskazywania wersji -- tak robię w kolejnych
    punktach. W przypadku rezygnacji z wirtualnego środowiska należy użyć polecenia
    z wyszczególnioną wersją, jak powyżej.

4. Zainstaluj zależności:

    ```bash
    python -m pip install -r requirements.txt
    ```

5. Przygotuj plik konfiguracyjny:

    ```bash
    echo "DATABASE_URL=${adres}" > .env
    ```
    Gdzie zmienna `adres` zawiera adres dostępu do bazy danych, razem z dialektem i
    sterownikiem oraz z poświadczeniami, jeśli są potrzebne, w następującej formie:
    `dialect+driver://username:password@host:port/database`. Domyślnym dialektem i
    silnikiem są `sqlite+aiosqlite`, w przypadku użycia innych może wystąpić potrzeba
    zainstalowania dodatkowego oprogramowania. Przykładowy adres dla uruchomienia
    lokalnego to: `sqlite+aiosqlite:////./history.db` (`sqlite+aiosqlite:///` dla
    Windows).

    Podanie adresu bazy danych jest obowiązkowe, dodatkowo plik konfiguracyjny może
    zawierać następujące wartości:
    
    - `DEFAULT_SUBREDDIT` - domyślny subreddit
    - `DEFAULT_LISTING` - domyślna lista, z której ma nastąpić losowanie (new, hot,
        best, rising, top, controversial)
    - `ENV` - typ środowiska uruchomienia aplikacji (dev, prod, test)

6. Uruchom aplikację:

    ```bash
    uvicorn leanservice.main:app
    ```
    Host oraz port mogą zostać skonfigurowane poprzez dodanie `--host` (domyślnie:
    127.0.0.1) oraz `--port` (domyślnie: 8000).

7. Profit ???

## Automatyczne testy
Realizowane przy użyciu frameworku pytest, wymagają instalacji dodatkowych bibliotek i
wtyczek. Zakładając, że punkt 3. został wykonany:

```bash
python -m pip install -r requirements-test.dev
python -m pytest --cov=leanservice tests
coverage html  # jeśli chcemy wygenerować raport html
```
