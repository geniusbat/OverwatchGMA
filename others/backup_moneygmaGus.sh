#!/bin/bash
#You have to set up bash variable (use export <var>=<value>) with the token created for admin for the api of the website
curl --header "Authorization: Token $MONEYGMA_GUS_API_TOKEN" https://moneygma.duckdns.org/api/expense -o moneygmaGus_backup