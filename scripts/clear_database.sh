#!/bin/bash
cat ../server/database.db > ../server/database.db
sqlite3 ../server/database.db < ../server/schema.sql