#Liking a user
https://api.happn.fr/api/users/1847725971/accepted/2484939267

    "data": {
        "message": "user accepted"
    }, 
    "error": null, 
    "error_code": 0, 
    "status": 200, 
    "success": true
}


#Charming a user #uses credits
POST https://api.happn.fr/api/users/1847725971/pokes/2484939267
http.useragent:   Happn/1.0 AndroidSDK/0
Authorization:    OAuth="c9f52cd265dd7378449b1c09d4e069a302"
Content-Type:     application/json
Content-Length:   2
User-Agent:       Dalvik/1.6.0 (Linux; U; Android 4.4.2; SCH-I535 Build/KOT49H)
Host:             api.happn.fr
Connection:       Keep-Alive
Accept-Encoding:  gzip

empty json


# Send message
 POST https://api.happn.fr/api/conversations/1847725985/messages/

Request                                                                                                   Response
http.useragent:   Happn/1.0 AndroidSDK/0
Authorization:    OAuth="c9f52cd265dd7378449b1c09d4e069a302"
Content-Type:     application/json
Content-Length:   68
User-Agent:       Dalvik/1.6.0 (Linux; U; Android 4.4.2; SCH-I535 Build/KOT49H)
Host:             api.happn.fr
Connection:       Keep-Alive
Accept-Encoding:  gzip

JSON
{
    "fields": "message,creation_date,sender.fields(id)", 
    "message": "aww"
}



# Get Conversations
GET https://api.happn.fr/api/users/1847725971/conversations/?query=%7B%22limit%22%3A16%2C%22offset%22%3A0%2C%22fields%22%3A%22id%2Cparticipants.fields%28user.fields%28id%2Cfirst_name%2Cage%2Cp
                        rofiles.mode%280%29.width%28144%29.height%28144%29.fields%28width%2Cheight%2Cmode%2Curl%29%29%29%2Cis_read%2Ccreation_date%2Cmodification_date%2Cis_read%2Clast_message.fields%28creation_da
                        te%2Cmessage%29%22%7D

# GET messages
https://api.happn.fr/api/conversations/1847725985/messages/?query=%7B%22limit%22%3A16%2C%22offset%22%3A0%2C%22fields%22%3A%22id%2Cmessage%2Ccreation_date%2Csender.fields%28id%2Cfirst_name%
                        2Cage%2Cprofiles.mode%280%29.width%2872%29.height%2872%29.fields%28mode%2Cwidth%2Cheight%2Curl%29%29%22%7D

Get Messages
http.useragent:   Happn/1.0 AndroidSDK/0
Authorization:    OAuth="c9f52cd265dd7378449b1c09d4e069a302"
Content-Type:     application/json
User-Agent:       Dalvik/1.6.0 (Linux; U; Android 4.4.2; SCH-I535 Build/KOT49H)
Host:             api.happn.fr
Connection:       Keep-Alive
Accept-Encoding:  gzip

