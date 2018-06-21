import re

_whole_word = lambda x: re.compile(r'(?<=\W)' + x + '(?=\W)')
_mixed_ordinal_pat = _whole_word(r'-?\d+(st|th|nd|rd)')
_integer_pat = _whole_word(r'\d+')
_floating_point_after_pat = re.compile(r'\.\d+[^a-zA-Z.]')
_floating_point_before_pat = re.compile(r'(?<=\d\.)')
#_date_iso8601_pat = _whole_word(r'\d{4}-\d{2}-\d{2}')
_date_fmt2_pat = _whole_word(r'\d{2} (Jan|Feb|Mar]|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}')
_date_iso8601_pat = _whole_word(r'\d{4}-(0\d|1[0-2])-(0[1-9]|[12][0-9]|3[01])')
_number_fmt1_pat = _whole_word(r'\d+')

def mixed_ordinals(text):
    '''Find tokens that begin with a number, and then have an ending like 1st or 2nd.'''
    for match in _mixed_ordinal_pat.finditer(text):
        yield('ordinal', match)

def integers(text):
    '''Find integers in text. Don't count floating point numbers.'''
    for match in _integer_pat.finditer(text):
        # If the integer we're looking at is part of a floating-point number, skip it.
        if _floating_point_before_pat.match(text, match.start()) or \
                _floating_point_after_pat.match(text, match.end()):
            continue
        yield ('integer', match)

def scan(text, *extractors):
    '''
    Scan text using the specified extractors. Return all hits, where each hit is a
    tuple where the first item is a string describing the extracted number, and the
    second item is the regex match where the extracted text was found.
    '''
    for extractor in extractors:
        for item in extractor(text):
            yield item


def dates_iso8601(text):
    ''' Find and extract date and time based on iso8601 format'''
    for match in _date_iso8601_pat.finditer(text):
        yield('date', match)


def dates_fmt2(text):
    for match in _date_fmt2_pat.finditer(text):
        yield('date', match)

def numbers_fmt1(text):
    for match in _number_fmt1_pat.finditer(text):
        yield('integer', match)