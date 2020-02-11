
def currencyFormat(val):
    val = "{0:.2f}".format(round(val, 2))
    return "$" + val.rjust(16, ' ')

def percentFormat(val):
    val = "{0:.2f}".format(round(val, 2))
    return "%" + val.rjust(16, ' ')