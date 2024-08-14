import locale


def format_cop(_amount):
    locale.setlocale(locale.LC_ALL, 'en_US')
    return locale.currency(_amount, grouping=True)
