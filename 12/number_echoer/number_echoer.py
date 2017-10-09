#!/usr/bin/env python3
import gettext
import locale
import os
import sys


current_locale, encoding = locale.getdefaultlocale()
t = gettext.translation(
    'number_echoer',
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locale'),
    [current_locale, 'en'])
t.install()
ngettext = t.ngettext
_ = t.gettext


def error_and_exit(error):
    """Print given error message to stderr and exit with status code 1. """
    print(error, file=sys.stderr)
    print(_('Usage: {} <number>').format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)


class InputNotInRangeError(ValueError):
    """Raised when too big number is input to NumberEchoer. """
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return (_('Entered number "{}" is not in allowed range. Numbers '
                  'in range <0, 10^12> can be entered. ').format(self.number))


class NumberEchoer(object):
    """Simple class used for converting integers to string.

    Numbers with up to fifteen digits are supported. Returned
    string is affected by system's locale. """
    hundred_to_word = {
        1: _('one hundred'),
        2: _('two hundred'),
        3: _('three hundred'),
        4: _('four hundred'),
        5: _('five hundred'),
        6: _('six hundred'),
        7: _('seven hundred'),
        8: _('eight hundred'),
        9: _('nine hundred'),
    }

    ten_to_word = {
        2: _('twenty'),
        3: _('thirty'),
        4: _('fourty'),
        5: _('fifty'),
        6: _('sixty'),
        7: _('seventy'),
        8: _('eighty'),
        9: _('ninety'),
    }

    one_to_word = {
        1: _('one'),
        2: _('two'),
        3: _('three'),
        4: _('four'),
        5: _('five'),
        6: _('six'),
        7: _('seven'),
        8: _('eight'),
        9: _('nine'),
        10: _('ten'),
        11: _('eleven'),
        12: _('twelve'),
        13: _('thirteen'),
        14: _('fourteen'),
        15: _('fifteen'),
        16: _('sixteen'),
        17: _('seventeen'),
        18: _('eighteen'),
        19: _('nineteen'),
    }

    zero = _('zero')

    def __init__(self):
        self.number_string = ''

    def _reset(self):
        self.number_string = ''

    def _append_string(self, string):
        """Append 'string' to the intermediate result. """
        if self.number_string:
            self.number_string += ' '
        self.number_string += '{}'.format(string)

    def _process_level(self, level, count):
        """Append string representation thousands, millions, billions or
        trillions strings to intermediate result. """
        if not level:
            return

        # Placed here, since deferred translation of plural forms is not
        # possible (yet) and ngettext requires 'count'.
        level_to_word = {
            1: ngettext('thousand', 'thousand', count),
            2: ngettext('million', 'million', count),
            3: ngettext('billion', 'billion', count),
            4: ngettext('trillion', 'trillion', count),
        }

        word = level_to_word[level]
        self._append_string(word)

    def _process_hundreds(self, number):
        """Append string representation of 'number' of hundreds to
        intermediate result. """
        if number == 0:
            return

        self._append_string(self.hundred_to_word[number])

    def _process_tens(self, number):
        """Append string representation of 'number' of tens to
        intermediate result. """
        if number == 0:
            return

        if number < 20:
            self._append_string(self.one_to_word[number])
        else:
            self._append_string(
                # numbers in <20, 99> range
                _('{tens} {ones}').format(
                    tens=self.ten_to_word[number // 10],
                    ones=self.one_to_word[number % 10],
                )
            )

    def _process_section(self, number, level):
        """Append string representation of number to intermediate result
        based on level.

        Number and level are values obtained from _split_to_sections method.
        """
        if number == 0:
            return

        hundreds = number // 100
        if hundreds:
            self._process_hundreds(hundreds)
        self._process_tens(number - 100 * hundreds)

        self._process_level(level, number)

    def _split_to_sections(self, number):
        """Returns list of tuples, each consisting of number and level.

        Number is an integer in range <0, 999>, level represents the power
        of thousand the number is multiplied with in original input (position
        of the number in the original full length number). The list is ordered
        in the same way the sections are ordered in original number.  """
        sections = []
        level = 0
        while True:
            divised = number // 1000
            remainder = number % 1000
            sections.insert(0, (remainder, level))
            level += 1

            if not divised:
                break

            number = divised
        return sections

    def get_string(self, input_number):
        """Process given input_number and return it's fully worded
        string representation. """
        try:
            input_number = int(input_number)
        except ValueError:
            raise ValueError(_('Integer is required as an input. '))

        # check number is in range <0, 1 trillion>
        if input_number not in range(10**12 + 1):
                raise InputNotInRangeError(input_number)

        self._reset()

        # zero
        if input_number == 0:
                self._append_string(self.zero)
        # other number
        else:
            for section, level in self._split_to_sections(input_number):
                self._process_section(section, level)
                level -= 1

        return self.number_string


echoer = NumberEchoer()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        error_and_exit(_('Invalid number of arguments. '))

    try:
        number_string = echoer.get_string(sys.argv[1])
    except (InputNotInRangeError, ValueError) as e:
        error_and_exit(str(e))

    print(number_string)
