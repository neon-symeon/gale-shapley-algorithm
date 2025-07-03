# Mężczyźni i ich preferencje
M = {
    'Aleksander': ['Grażyna', 'Halina', 'Irena', 'Jadwiga', 'Karolina'],
    'Bolek':      ['Halina', 'Irena', 'Grażyna', 'Karolina', 'Jadwiga'],
    'Czesiek':    ['Grażyna', 'Halina', 'Jadwiga', 'Irena', 'Karolina'],
    'Daniel':     ['Karolina', 'Grażyna', 'Halina', 'Irena', 'Jadwiga'],
    'Edward':     ['Irena', 'Halina', 'Karolina', 'Jadwiga', 'Grażyna'],
}

# Kobiety i ich preferencje
F = {
    'Grażyna':  ['Edward', 'Daniel', 'Aleksander', 'Bolek', 'Czesiek'],
    'Halina':   ['Bolek', 'Czesiek', 'Edward', 'Aleksander', 'Daniel'],
    'Irena':    ['Daniel', 'Aleksander', 'Bolek', 'Czesiek', 'Edward'],
    'Jadwiga':  ['Aleksander', 'Bolek', 'Czesiek', 'Daniel', 'Edward'],
    'Karolina': ['Czesiek', 'Daniel', 'Aleksander', 'Bolek', 'Edward'],
}


def validate_input(m_prefs: dict, f_prefs: dict):
    """
    Sprawdza poprawność danych wejściowych przed uruchomieniem algorytmu.
    """
    # 1. Sprawdza typy danych
    if not isinstance(m_prefs, dict) or not isinstance(f_prefs, dict):
        raise TypeError(
            'Dane wejściowe `m_prefs` i `f_prefs` muszą być słownikami.')

    men_set = set(m_prefs.keys())
    women_set = set(f_prefs.keys())

    # 2. Sprawdza równoliczność zbiorów
    if len(men_set) != len(women_set):
        raise ValueError(
            'Popraw dane. Zbiory mężczyzn i kobiet muszą być równoliczne.')

    # 3. Sprawdza rozłączności zbiorów (czy ktoś nie jest jednocześnie w obu
    # grupach)
    if not men_set.isdisjoint(women_set):
        raise ValueError(
            f'Zbiory mężczyzn i kobiet nie są rozłączne. Wspólne elementy:'
            f'{men_set.intersection(women_set)}')

    # 4. Sprawdza spójność list preferencji
    for man, prefs in m_prefs.items():
        if set(prefs) != women_set:
            raise ValueError(
                f'Preferencje "{man}" nie zawierają wszystkich kobiet.')

    for woman, prefs in f_prefs.items():
        if set(prefs) != men_set:
            raise ValueError(
                f'Preferencje {woman} nie zawierają wszystkich mężczyzn.')

    # 5. Sprawdza unikalność list preferencji w obrębie jednej płci

    # 🧠 Jeśli w men_pref_lists są dwie (lub więcej) identyczne listy preferen-
    # cji, tzn. dwóch mężczyzn lub dwie kobiety mają takie same rankingi prefe-
    # rencji, zamiana listy na zbiór usunie te duplikaty, zatem lista i odpo-
    # wiadający jej zbiór będą różnej długości == kod zgłosi błąd.

    men_pref_lists = [tuple(p) for p in m_prefs.values()]
    if len(set(men_pref_lists)) != len(men_pref_lists):
        raise ValueError(
            'Listy preferencji mężczyzn nie są unikalne. Znaleziono duplikaty.')

    # Analogicznie dla kobiet:
    women_pref_lists = [tuple(p) for p in f_prefs.values()]
    if len(set(women_pref_lists)) != len(women_pref_lists):
        raise ValueError(
            'Listy preferencji kobiet nie są unikalne. Znaleziono duplikaty.')


def stable_matching(
        m_prefs: dict,
        f_prefs: dict,
        _max_iterations=None) -> tuple[dict, list]:
    """
    Główna funkcja znajdująca dopasowania metodą Gale'a-Shapley'a.
    """
    # Przed startem waliduje dane wejściowe
    validate_input(m_prefs, f_prefs)

    # Tworzy listę wolnych mężczyzn, którzy jeszcze nie mają dopasowania
    unmatched_men = list(m_prefs)

    # Tworzy słownik przechowujący aktualne dopasowania kobiet do mężczyzn
    matches = {}

    # Przechowuje historię kroków prowadzących do stabilnych dopasowań
    history = []

    # Wentyl bezpieczeństwa - pętla nie powinna wykonać więcej niż n^2 iteracji
    if _max_iterations is None:
        _max_iterations = len(m_prefs) ** 2

    safety_iteration_count = 0

    while unmatched_men:
        # Aktywuje wentyl bezpieczeństwa gdy przekroczy dozw. limit operacji
        if safety_iteration_count > _max_iterations:
            raise RuntimeError(
                f'Przekroczono dopuszczalną liczbę iteracji: '
                f'{_max_iterations}.')

        safety_iteration_count += 1

        # Pobiera mężczyznę bez dopasowanej jeszcze kobiety
        man = unmatched_men.pop(0)

        # Iteruje przez listę preferowanych kobiet dla wybranego mężczyzny
        for woman in m_prefs[man]:
            # Wczytuje aktualnie przypisanego mężczyznę do tej kobiety
            current_match = matches.get(woman)

            if current_match is None:
                # Kobieta bez dopasowania, może utworzyć parę
                matches[woman] = man
                break
            else:
                # Kobieta ma już parę, porównuje mężczyzn między sobą...
                woman_pref = f_prefs[woman]
                if woman_pref.index(man) < woman_pref.index(current_match):
                    # ... i przypisuje kobiecie mężczyznę zgodneo z jej
                    # preferencjami (lepiej do niej dopasowanego)
                    matches[woman] = man

                    # zwraca odrzuconego mężczyznę do listy mężczyzn bez
                    # dopasowania
                    print(f'♂️  {current_match} wraca do klubu samotnych serc')
                    unmatched_men.append(current_match)
                    break

        # Zapisuje postęp w historii dopasowań
        history.append(matches.copy())

    return matches, history


def display_matches(matches, history, show_history=True):  # pragma: no cover
    """
    Funkcja wyświetlająca finalne dopasowania oraz historię ich powstawania.
    """
    text_ = 'Finalne dopasowanie:'
    print(f'\n\n{text_}')
    print('-' * len(text_))
    for woman, man in sorted(matches.items()):
        print(f'{man} + {woman}')

    if show_history:
        # Opcjonalnie pokazuje całą historię
        text_ = 'Historia dochodzenia do rozwiązania:'
        print(f'\n\n{text_}')
        print('-' * len(text_))
        for step, state in enumerate(history, 1):
            print(f'Krok {step}: {state}')


if __name__ == '__main__':  # pragma: no cover

    # 🚩 Uwaga:
    # Kolejność przekazanych słowników ma znaczenie:
    # pierwszy proponuje, dlatego pierwszy (np. mężczyźni) zyskuje przewagę.
    # Możliwa jest odwrotna kolejność.
    # Zmiana strony oferującej (np. na kobiety) sprawia,
    # że w wyniku działania algorytmu możemy otrzymać inny,
    # choć ciągle stabilny, zbiór dopasowań.

    final_matches, matching_history = stable_matching(
        m_prefs=M,
        f_prefs=F,
    )
    display_matches(final_matches, matching_history)
