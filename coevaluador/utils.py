from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
import re


@deconstructible
class RutValidator(validators.RegexValidator):
    regex = r'[0-9]+\.?[0-9]{3}\.?[0-9]{3}\-?[0-9|K|k]$'  # For RUT - Chile
    message = _(
        'Enter a valid rut. This value may contain only numbers and ./- characters.'
    )
    flags = 0


def validate(raw_rut):
    r = re.compile(r'[0-9]+\.?[0-9]{3}\.?[0-9]{3}\-?[0-9|K|k]$')
    m = r.match(raw_rut)
    if m:
        return True
    else:
        return False


def escape_rut(rut):
    return rut.replace('.', '').replace('-', '').replace('k', 'K').replace(' ', '').replace('\t', '')
