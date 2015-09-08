$ORIGIN	warsaw.practicum.os3.nl.
$TTL 600
; 
;       Addresses and other host information. 
; 
@      		IN      SOA     warsaw.practicum.os3.nl. martin.warsaw.practicum.os3.nl. ( 
                                2014092312   ;   Serial 
                                900	     ;   Refresh 
                                300          ;   Retry 
                                3600         ;   Expire 
                                300 )        ;   Negative cache TTL 
;       Define the name servers and the mail servers 
                IN      NS      ns1.warsaw.practicum.os3.nl.
                IN      MX      10 mx1.warsaw.practicum.os3.nl. 
                IN      MX      20 mx2.warsaw.practicum.os3.nl. 
; 
;       Define localhost 
; 
localhost       IN      A       127.0.0.1 
; 
;       Define the hosts in this zone 
; 
warsaw.practicum.os3.nl.          	IN      A       145.100.104.62 
ns1					IN	A	145.100.104.62
mx1            				IN      A       145.100.104.61
mail1   				IN      CNAME   mx1.warsaw.practicum.os3.nl. 
mx2            				IN      A       145.100.104.60
mail2          				IN      CNAME   mx2.warsaw.practicum.os3.nl. 
twain    				IN      A       145.100.104.59
osiris     				IN      A       145.100.104.58
*					IN	TXT	"sitefinder"
*                                       IN      A	145.100.104.62

