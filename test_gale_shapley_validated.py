import unittest
from gale_shapley_validated import (
    validate_input,
    stable_matching,
)


class TestStableMatching(unittest.TestCase):

    def setUp(self):
        self.m_prefs = {
            'Adam': ['Ewa', 'Zofia'],
            'Bartek': ['Zofia', 'Ewa'],
        }

        self.f_prefs = {
            'Ewa': ['Adam', 'Bartek'],
            'Zofia': ['Bartek', 'Adam'],
        }

    # VALIDATE INPUT

    def test_validate_input_correct(self):
        """
        sprawdza, czy funkcja poprawnie przyjmuje poprawne dane wejściowe
        (tj. zestawy preferencji mężczyzn i kobiet).
        """
        try:
            validate_input(self.m_prefs, self.f_prefs)
        except Exception as e:
            self.fail(f'Unexpected exception raised: {e}')

    def test_validate_input_wrong_type(self):
        """
        Sprawdza typy danych, czy funkcja validate_input zgłasza wyjątek
        TypeError, jeśli dane wejściowe nie są słownikami.
        """
        with self.assertRaises(TypeError):
            validate_input([], self.f_prefs)

    def test_validate_input_unequal_sizes(self):
        """
        Sprawdza równoliczność zbiorów, czy funkcja validate_input wykrywa
        różną liczbę mężczyzn i kobiet w danych wejściowych,
        zgłaszając ValueError.
        """
        self.f_prefs.pop('Ewa')
        with self.assertRaises(ValueError):
            validate_input(self.m_prefs, self.f_prefs)

    def test_validate_input_non_disjoint(self):
        """
        Sprawdza rozłączności zbiorów, czy funkcja poprawnie wykrywa sytuację,
        gdy zbiory mężczyzn i kobiet nie są rozłączne (tj. gdy jedna osoba
        pojawia się zarówno w zbiorze mężczyzn, jak i kobiet).
        """
        self.m_prefs['Ewa'] = ['Zofia', 'Ewa']
        with self.assertRaises(ValueError):
            validate_input(self.m_prefs, self.f_prefs)

    def test_validate_input_missing_prefs(self):
        """
        Sprawdza spójność list preferencji, czy funkcja validate_input wykrywa
        sytuację, w której preferencje są niekompletne, tj. mężczyzna lub ko-
        ta nie ma w swojej liście preferencji wszystkich osób płci przeciwnej.
        """
        self.m_prefs['Adam'].remove('Zofia')
        with self.assertRaises(ValueError):
            validate_input(self.m_prefs, self.f_prefs)

    def test_validate_input_duplicate_preferences_men(self):
        """
        Sprawdza unikalność list preferencji, czy funkcja validate_input
        wykrywa duplikaty list preferencji mężczyzn, zgłaszając ValueError,
        jeśli dwóch mężczyzn ma identyczne listy preferencji.
        """
        self.m_prefs['Adam'] = ['Zofia', 'Ewa']
        self.m_prefs['Bartek'] = ['Zofia', 'Ewa']
        with self.assertRaises(ValueError):
            validate_input(self.m_prefs, self.f_prefs)

    def test_validate_input_duplicate_preferences_women(self):
        """
        Analogicznie do poprzedniego. Sprawdza, czy funkcja validate_input
        zgłasza ValueError, jeśli dwie kobiety mają identyczne
        listy preferencji.
        """
        f_prefs = {
            'Ewa': ['Adam', 'Bartek'],
            'Zofia': ['Adam', 'Bartek'],
        }
        with self.assertRaises(ValueError):
            validate_input(self.m_prefs, f_prefs)

    def test_validate_input_man_and_woman_same_name(self):
        """
        Testuje walidację, gdy ta sama osoba występuje w mężczyznach
        i kobietach.
        """
        m_prefs = {'Adam': ['Zofia'], 'Bartek': ['Zofia']}
        f_prefs = {'Ewa': ['Adam', 'Bartek'], 'Adam': ['Czesiek', 'Adam']}
        with self.assertRaises(ValueError):
            validate_input(m_prefs, f_prefs)

    def test_validate_input_woman_missing_preferences(self):
        """
        Testuje walidację, gdy kobieta nie ma pełnych preferencji mężczyzn.
        """
        m_prefs = {
            'Adam': ['Ewa', 'Zofia'],
            'Bartek': ['Zofia', 'Ewa']
        }
        f_prefs = {
            'Ewa': ['Adam', 'Bartek'],
            'Zofia': ['Bartek']
        }  # brak Adama w preferencjach Zosi

        with self.assertRaises(ValueError):
            validate_input(m_prefs, f_prefs)

    # STABLE MATCHING

    def test_runtime_error_on_exceeding_iterations(self):
        """
        Wymusza RuntimeError przy przekroczeniu limitu iteracji.
        """
        with self.assertRaises(RuntimeError):
            stable_matching(self.m_prefs, self.f_prefs, _max_iterations=0)

    def test_stable_matching(self):
        """
        Weryfikuje poprawność działania funkcji stable_matching, sprawdzając,
        czy zwraca oczekiwane, stabilne dopasowania oraz czy historia kroków
        jest poprawnie zapisywana i kończy się stanem odpowiadającym wynikowym
        dopasowaniom.
        """
        matches, history = stable_matching(self.m_prefs, self.f_prefs)
        expected_matches = {'Ewa': 'Adam', 'Zofia': 'Bartek'}
        self.assertEqual(matches, expected_matches)
        self.assertTrue(len(history) > 0)
        self.assertEqual(history[-1], expected_matches)

    def test_force_swap(self):
        """
        Testuje zamianę partnera.
        """
        m_prefs = {
            'Adam': ['Ewa', 'Zofia', 'Anna'],
            'Bartek': ['Ewa', 'Anna', 'Zofia'],
            'Czesiek': ['Anna', 'Ewa', 'Zofia']
        }
        f_prefs = {
            'Ewa': ['Bartek', 'Adam', 'Czesiek'],  # Ewa woli Bartka od Adama
            'Zofia': ['Adam', 'Bartek', 'Czesiek'],
            'Anna': ['Czesiek', 'Adam', 'Bartek']
        }

        matches, history = stable_matching(m_prefs, f_prefs)

        # Sprawdza ostateczny, prawidłowy wynik po zamianie
        expected_matches = {'Ewa': 'Bartek', 'Zofia': 'Adam', 'Anna': 'Czesiek'}
        self.assertEqual(matches, expected_matches)

        # Sprawdza, czy w historii faktycznie doszło do zamiany
        # Szuka kroku, w którym Ewa była tymczasowo z Adamem
        ewa_was_with_adam = any(
            state.get('Ewa') == 'Adam' for state in history
        )
        # Wczytuje dopasowania dla Ewy: z historii i ostateczne.
        ewa_first_match = history[0].get('Ewa')
        ewa_final_match = matches.get('Ewa')
        self.assertTrue(
            ewa_was_with_adam,
            "Test nie wykazał, że Ewa była tymczasowo z Adamem przed zamianą."
        )
        self.assertEqual('Adam', ewa_first_match)
        self.assertEqual('Bartek', ewa_final_match)


if __name__ == '__main__':
    # Uruchamia wszystkie testy z maksymalną szczegółowością (verbosity=2)
    # i wyłączonym buforowaniem (buffer=False), by pokazać printy.
    unittest.main(
        argv=['first-arg-is-ignored'],
        exit=False,
        verbosity=2,
        buffer=False
    )
