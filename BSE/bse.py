from bsedata.bse import BSE
b = BSE()
print(b)
# Output:
# Driver Class for Bombay Stock Exchange (BSE)

# to execute "updateScripCodes" on instantiation
b = BSE(update_codes = True)

q = b.getQuote('500182')
print(q)
