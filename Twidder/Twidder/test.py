import database_helper

body = {"API Key" : "1@1.1", "hmac" : "a5464a9ccb49ce9de80ab58087e54796c341775bf6f3ee67ecad34cc1cb78a5a", "data" : "hej"}
print(database_helper.getHmac_from_body(body))

print(database_helper.hash256({'data':'hej'}, '9d644fbf-25d3-4c02-b98c-e8664a946c81'))