class TakeLast:
    """
    Returns the last non-null/non-empty value from the values received,
    so it's typically used as an output processor to single-valued fields.
    It doesn't receive any ``__init__`` method arguments, nor does it accept Loader contexts.

    Example:

    >>> proc = TakeLast()
    >>> proc(['one', 'two', 'three', ''])
    'three'
    """

    def __call__(self, values):
        for value in values[::-1]:
            if value is not None and value != "":
                return value
