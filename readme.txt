superuser username = ammar
superuser password = ammarpassword

Payment Note:
Since I had an extension due to circcumstances i was not able to test and work with the payment services in time and give them my airline's payment details. Therefore, I will have to manually request you the marker/ assesor to add my payment details using the superuser functionality, alternatively
can access the sql database and manually add it in. (This only applied if you expect dummy data within the db).

1. These are the following fields that need to be added using payments superuser:

name_on_card: keeganAirline
card_number: 2079666858888750
card_number_hash: 8d5a6c72c000deb233690427d006b9e4b394146d7c84cc7cbf1ed1d93e3552d336136da5d31e82dc4868d62069a9537c
account_number: 365555721
sortcode : 232323
expiry_month : 2
expiry_year : 25
cvc : 123
cvc_hash: 9a0a82f0c0cf31470d7affede3406cc9aa8410671520b727044eda15b4c25532a9b5cd8aaf9cec4919d76255b6bfb00f
account_balance : 5574.32

2. Alternatively you can add it using the sql command:

   INSERT INTO payment_api_account (name_on_card, card_number, card_number_hash, account_number, sortcode, expiry_month, expiry_year, cvc, cvc_hash, account_balance)
   VALUES ('keeganAirline', 2079666858888750, '8d5a6c72c000deb233690427d006b9e4b394146d7c84cc7cbf1ed1d93e3552d336136da5d31e82dc4868d62069a9537c', '365555721', '232323', '2', '25', '123', '9a0a82f0c0cf31470d7affede3406cc9aa8410671520b727044eda15b4c25532a9b5cd8aaf9cec4919d76255b6bfb00f', 5574.32);
