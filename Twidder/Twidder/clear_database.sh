#!/bin/bash
cat ./database.db > ./database.db
sqlite3 ./database.db < ./schema.sql