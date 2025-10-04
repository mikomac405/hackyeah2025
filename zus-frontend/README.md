# 🏛️ ZUS Frontend - Symulator Emerytalny

Frontend aplikacji symulatora emerytalnego ZUS napisany w Angular 17.

## 📋 Wymagania systemowe

Przed rozpoczęciem upewnij się, że masz zainstalowane:

### 1. Node.js (wersja 18 lub nowsza)
- **Windows**: Pobierz z [nodejs.org](https://nodejs.org) i zainstaluj
- **macOS**: Pobierz z [nodejs.org](https://nodejs.org) lub użyj `brew install node`
- **Linux**: `sudo apt install nodejs npm` (Ubuntu/Debian)

**Sprawdź czy Node.js jest zainstalowany:**
```bash
node --version
# Powinno pokazać coś jak: v18.17.0 lub nowsze
```

### 2. Angular CLI (globalnie)
```bash
npm install -g @angular/cli
```

**Sprawdź czy Angular CLI jest zainstalowany:**
```bash
ng version
# Powinno pokazać informacje o Angular CLI
```

## 🚀 Jak uruchomić projekt po raz pierwszy

### Krok 1: Sklonuj repozytorium
```bash
git clone <url-repozytorium>
cd hackyeah2025
```

### Krok 2: Przejdź do folderu frontend
```bash
cd zus-frontend
```

### Krok 3: Zainstaluj zależności
```bash
npm install
```
⏱️ *To może potrwać 2-5 minut za pierwszym razem*

### Krok 4: Uruchom serwer deweloperski
```bash
ng serve
```

### Krok 5: Otwórz aplikację w przeglądarce
Wejdź na: [http://localhost:4200](http://localhost:4200)

🎉 **Gotowe!** Aplikacja powinna działać w przeglądarce.

## 📁 Struktura projektu

```
zus-frontend/
├── src/
│   ├── app/
│   │   ├── core/                    # Serwisy i modele biznesowe
│   │   │   ├── models/             # Interfejsy TypeScript
│   │   │   └── services/           # Serwisy (kalkulacje, API)
│   │   ├── features/               # Komponenty głównych funkcji
│   │   │   ├── home/              # Strona główna
│   │   │   ├── simulation/        # Formularz symulacji
│   │   │   ├── results/           # Wyniki obliczeń
│   │   │   └── dashboard/         # Dashboard analityczny
│   │   ├── shared/                # Komponenty współdzielone
│   │   │   ├── components/        # Reużywalne komponenty
│   │   │   └── pipes/             # Pipe'y (formatowanie)
│   │   ├── app.component.*        # Główny komponent aplikacji
│   │   └── app.module.ts          # Główny moduł Angular
│   ├── assets/                    # Pliki statyczne (obrazy, ikony)
│   ├── styles.css                 # Globalne style CSS
│   └── index.html                 # Główny plik HTML
├── package.json                   # Zależności npm
└── angular.json                   # Konfiguracja Angular
```

## 🛠️ Przydatne komendy

### Uruchamianie
```bash
# Uruchom serwer deweloperski
ng serve

# Uruchom serwer z automatycznym otwarciem przeglądarki
ng serve --open

# Uruchom na innym porcie
ng serve --port 4300
```

### Budowanie
```bash
# Zbuduj aplikację do produkcji
ng build

# Zbuduj w trybie deweloperskim
ng build --configuration development
```

### Testowanie
```bash
# Uruchom testy jednostkowe
ng test
```

### Inne przydatne
```bash
# Sprawdź czy kod jest poprawny
ng lint

# Wygeneruj nowy komponent
ng generate component nazwa-komponentu

# Sprawdź wersję Angular
ng version
```

## 🐛 Rozwiązywanie problemów

### Problem: `ng: command not found`
**Rozwiązanie:**
```bash
npm install -g @angular/cli
```

### Problem: `npm: command not found`
**Rozwiązanie:** Zainstaluj Node.js z [nodejs.org](https://nodejs.org)

### Problem: Port 4200 jest zajęty
**Rozwiązanie:**
```bash
ng serve --port 4300
# lub inny wolny port
```

### Problem: Błędy podczas `npm install`
**Rozwiązanie:**
```bash
# Wyczyść cache npm
npm cache clean --force

# Usuń node_modules i zainstaluj ponownie
rm -rf node_modules
npm install
```

### Problem: Aplikacja nie ładuje się w przeglądarce
**Rozwiązanie:**
1. Sprawdź czy serwer działa (powinno być: `✔ Compiled successfully`)
2. Sprawdź konsolę przeglądarki (F12 → Console)
3. Sprawdź czy port 4200 nie jest blokowany przez firewall

## 🔧 Konfiguracja środowiska

### Pliki environment
- `src/environments/environment.ts` - środowisko deweloperskie
- `src/environments/environment.prod.ts` - środowisko produkcyjne

### Główne zależności
- **Angular 17** - framework frontendowy
- **Angular Material** - komponenty UI
- **RxJS** - programowanie reaktywne
- **TypeScript** - język programowania

## 🌐 API Backend

Frontend komunikuje się z backend API (Python) poprzez:
- **Kalkulacje emerytury**: `POST /api/calculate-pension`
- **Grupy emerytalne**: `GET /api/pension-groups`  
- **Statystyki**: `GET /api/regional-stats`

⚠️ **Uwaga**: Obecnie obliczenia są wykonywane lokalnie na frontendzie jako tymczasowe rozwiązanie.

## 👥 Dla zespołu deweloperskiego

### Przed commitem
```bash
# Sprawdź czy kod się buduje
ng build

# Sprawdź czy testy przechodzą
ng test

# Sprawdź formatting
ng lint
```

### Workflow git
```bash
git add .
git commit -m "feat: opis zmian"
git push
```

## 📞 Pomoc

Jeśli masz problemy:

1. **Sprawdź terminal** - czy są jakieś błędy?
2. **Sprawdź konsolę przeglądarki** (F12 → Console)
3. **Restartuj serwer** - Ctrl+C w terminalu, potem `ng serve`
4. **Zapytaj zespół** - opisz dokładnie co robiłeś i jaki błąd widzisz

---

### 🎯 Szybki start (TL;DR)

```bash
# 1. Sklonuj repo i przejdź do frontu
git clone <repo> && cd hackyeah2025/zus-frontend

# 2. Zainstaluj zależności
npm install

# 3. Uruchom
ng serve

# 4. Otwórz http://localhost:4200
```

**Gotowe! 🚀**