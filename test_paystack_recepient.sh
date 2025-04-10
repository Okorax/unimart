# /usr/bin/bash
recipient_url="https://api.paystack.co/transferrecipient"
recipient_data='{
  "type": "nuban",
  "name": "Promise Okoli",
  "account_number": "8169976046",
  "bank_code": "999992",
  "currency": "NGN"
}'

curl -X POST "$recipient_url" \
  -H "Authorization: Bearer sk_test_2ad5ea4a7253aa13a0fe9ac6f7a7ecbd602b3e36" \
  -H "Content-Type: application/json" \
  -d "$recipient_data"
