$ORIGIN	paris.derby.practicum.os3.nl.
$TTL 600
; 
;       Addresses and other host information. 
; 
@      		IN      SOA     paris.derby.practicum.os3.nl. martin.paris.derby.practicum.os3.nl. ( 
                                2015011300   ;   Serial 
                                900	     ;   Refresh 
                                300          ;   Retry 
                                3600         ;   Expire 
                                300 )        ;   Negative cache TTL 
;       Define the name servers and the mail servers 
                IN      NS      ns1.warsaw.practicum.os3.nl.
                IN      MX      10 mx1.paris.derby.practicum.os3.nl. 
                IN      MX      20 mx2.paris.derby.practicum.os3.nl. 
; 
;       Define localhost 
; 
localhost       IN      A       127.0.0.1 
; 
;       Define the hosts in this zone 
; 
paris.derby.practicum.os3.nl.          	IN      A       145.100.104.62 
ns1					IN	A	145.100.104.62
mx2					IN	A	145.100.104.62
mx2            				IN      A       145.100.104.60
www	    				IN      A       145.100.104.59
www2     				IN      A       145.100.104.58

