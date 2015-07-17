import facebook

access_token = '1424256687904844|BgP_1Cua2V2xawRDdXLbNontxq4'      # Obtained from https://developers.facebook.com/tools/accesstoken/
app_id = "1424256687904844"                       # Obtained from https://developers.facebook.com/
app_secret = "20dd231b3a4c7300da5649cedaa5d716"         # Obtained from https://developers.facebook.com/


graph = facebook.GraphAPI('CAAUPWpnzmEwBABZANv4cIAGsrawmY6ItKTwVRKjESmGzfG555o2ZBvqyxfDLf90e2zGf7QzHQX7UZCw6vCMCOkpNfuE475ZBauiIxo56uXJdzH7tA0GpDBJdbSaed1lI8ZCZBIpf7ZCxTJhsXQQNJlZA1doRa36BKBZAOoIAKbHTnmzOmjoHO6nDUZCfwKP8WsjyMMW8jF0KC53HUJaTix1pmr')

# Extend the expiration time of a valid OAuth access token.
extended_token = graph.extend_access_token(app_id, app_secret)
print extended_token #verify that it expires in 60 days