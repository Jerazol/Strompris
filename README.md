# Strompris

# For å komme i gang
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

#Sett env-variabler
export PG_CONNECTION_STRING='pq://databasebruker:passord@databasehost/databasenavn'
export ELVIA_METER=<Meter ID fra min side på elvia.no>
export ELVIA_TOKEN=<API-token fra min side på elvia.no>
