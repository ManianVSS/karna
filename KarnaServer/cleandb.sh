#!/bin/bash
rm -rf api/migrations
rm data/db.sqlite3
bash migrate.sh
