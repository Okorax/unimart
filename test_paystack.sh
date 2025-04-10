#!/bin/sh
url="https://api.paystack.co/transfer"
authorization="Authorization: Bearer sk_test_2ad5ea4a7253aa13a0fe9ac6f7a7ecbd602b3e36"
content_type="Content-Type: application/json"
data='{ 
  "source": "balance", 
  "reason": "Calm down", 
  "amount":3794800, 
  "recipient": "RCP_onqbhkfmepex0qq"
}'

curl "$url" -H "$authorization" -H "$content_type" -d "$data" -X POST
