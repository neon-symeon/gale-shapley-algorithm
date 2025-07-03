# Algorytm Gale’a-Shapleya (Stable Matching)

**Autorzy:** Igor Owczarek, Jan Potoczek, Michał Szczurek, Szymon Marek

## 📌 Wprowadzenie

Algorytm Gale’a-Shapleya (1962) rozwiązuje **problem stabilnego skojarzenia** dwóch zbiorów uczestników o równolicznej liczebności, z których każdy posiada listę preferencji. Znajduje stabilne dopasowanie, w którym nie istnieją pary chcące zerwać swoje obecne dopasowania na rzecz siebie nawzajem.

W praktyce algorytm znajduje zastosowanie m.in. w:

* procesach rekrutacji na uczelnie,
* przydziałach lekarzy do szpitali (NRMP),
* programach wymiany nerek,
* przydziałach uczniów do szkół.

## 🧩 Jak działa algorytm?

1️⃣ Dopóki istnieje niedopasowany uczestnik:

* Proponuje on najbardziej preferowanej osobie, która jeszcze go nie odrzuciła.
* Jeśli osoba jest wolna, akceptuje propozycję.
* Jeśli jest zaręczona, porównuje obecnego partnera z nowym:

  * Jeśli woli nowego, zrywa obecne zaręczyny i przyjmuje nową propozycję.
  * W przeciwnym razie odrzuca nowego kandydata.

2️⃣ Po zakończeniu iteracji powstaje stabilne dopasowanie, w którym:

* Osoba proponująca otrzymuje **najkorzystniejsze dostępne stabilne dopasowanie**.
* Osoba przyjmująca musi zaakceptować **najmniej korzystne spośród stabilnych dopasowań**.

Złożoność czasowa: **O(n²)**.

---

## 💡 Przykład

Dla zbiorów:

* Mężczyźni: Aleksander, Bolek, Czesiek, Daniel, Edward
* Kobiety: Grażyna, Halina, Irena, Jadwiga, Karolina

oraz ich preferencji, algorytm znajdzie stabilne dopasowania gwarantujące brak konfliktów oraz możliwość stabilnego skojarzenia wszystkich uczestników.

---

## 🚀 Uruchomienie projektu

1️⃣ Sklonuj repo:

```bash
git clone https://github.com/<twoj_nick>/gale-shapley-algorithm.git
cd gale-shapley-algorithm
```

2️⃣ Zainstaluj zależności:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

3️⃣ Uruchom algorytm:

```bash
python gale_shapley_validated.py
```

---

## 🧪 Uruchamianie testów

Uruchom testy jednostkowe:

```bash
python -m unittest discover -v
```

lub z pokryciem kodu:

```bash
coverage run -m unittest discover
coverage report -m
```

---

## 🩺 Zastosowania w rzeczywistości

* **NRMP (przydział rezydentur medycznych w USA)**: wdrożenie algorytmu zmniejszyło chaos w rekrutacjach, zapewniając stabilność dopasowań.
* **System przydziału do szkół w Nowym Jorku i Bostonie**: pozwala na zgłaszanie prawdziwych preferencji bez strategicznego zgadywania.
* **Programy wymiany nerek**: algorytmy oparte o Gale’a-Shapleya umożliwiają identyfikowanie kompatybilnych par dawców i biorców, ratując życie.

---

## 📚 Dalsze materiały

* Roughgarden T. *Kidney Exchange and Stable Matching*, *Twenty Lectures on Algorithmic Game Theory*, Cambridge University Press (2016).
* Pass (2018) - *A Course in Networks and Markets*.
* [Film wyjaśniający algorytm (YouTube)](https://youtu.be/0m_YW1zVs-Q?si=fKaSp8ktp1Ekxi-o)

---

## 🛡️ Licencja

Projekt udostępniony na licencji **MIT** – możesz korzystać, modyfikować i uczyć się swobodnie.

---

## ✨ Podziękowania

Dziękujemy za zainteresowanie projektem!
Zachęcamy do przeczytania pełnego **artykułu o algorytmie Gale’a-Shapleya na naszym [LinkedIn](tutaj-wstaw-link-do-artykulu)** (gdy opublikujesz).

> Jeśli uznasz projekt za wartościowy, zostaw ⭐ na GitHub – pomoże nam dotrzeć do innych zainteresowanych stabilnymi dopasowaniami!
