# 📝 Hackathon ZUS – Lista zadań

## 📊 Analityka i dane
- [ ] Import danych ZUS (Prognoza Funduszu Emerytalnego do 2080 r.)
- [ ] Dodanie danych GUS, NBP, MF (wzrost wynagrodzeń, inflacja, chorobowe)
- [ ] Opracowanie algorytmu prognozy emerytury (indeksacja, odwrócona indeksacja, stopa zastąpienia)
- [ ] Model wpływu chorobowego (osobno dla kobiet i mężczyzn)
- [ ] Scenariusze +1, +2, +5 lat przejścia na emeryturę
- [ ] Struktura danych i API (JSON wejściowy/wyjściowy)

---

## 💻 Backend
- [ ] Endpoint przyjmujący dane użytkownika (wiek, płeć, wynagrodzenie, itp.)
- [ ] Logika obliczeń prognozy na serwerze (testy jednostkowe)
- [ ] Baza danych: sessions, forecasts, usage_logs
- [ ] Generowanie raportów PDF (dla użytkownika)
- [ ] Generowanie XLS (dla administratora)
- [ ] Logging + eksport użyć (data, parametry, wyniki, kod pocztowy)
- [ ] Bezpieczeństwo i RODO (anonimizacja, HTTPS, minimalizacja danych)

---

## 🖼 Frontend
- [ ] Ekran startowy (oczekiwana emerytura, wykres grup, ciekawostki)
- [ ] Formularz symulacji (wiek, płeć, brutto, rok rozpoczęcia/zakończenia, środki opcjonalne, chorobowe)
- [ ] Wyniki (kwota rzeczywista i urealniona, stopa zastąpienia, wpływ chorobowego, scenariusze)
- [ ] Dashboard (edycja parametrów, okresy choroby, wzrost środków w czasie)
- [ ] Pobieranie raportu (PDF/XLS)
- [ ] Styling zgodny z Księgą Znaku ZUS (paleta, WCAG 2.0, responsywność)
- [ ] Testy dostępności (aria-labels, kontrast, obsługa klawiatury)

---

## 📝 Raportowanie i zgodność
- [ ] Raport użyć XLS (data, godzina, oczekiwana emerytura, płeć, wynagrodzenie, chorobowe, środki, wyniki, kod pocztowy)
- [ ] Generowanie PDF użytkownika z wykresami i parametrami wejściowymi
- [ ] Testy WCAG 2.0 (manualne i automatyczne)
- [ ] Testy jednostkowe, integracyjne i e2e
- [ ] Polityka prywatności i zgodność z RODO
- [ ] Dokumentacja dla admina i użytkownika (instrukcja obsługi, FAQ)

---

## 🚀 Bonusy (jeśli starczy czasu)
- [ ] Porównanie scenariuszy obok siebie
- [ ] Animowany timeline kariery → emerytura
- [ ] Infografiki do social media (PNG/SVG)
- [ ] Dark mode
- [ ] Wersja EN UI
