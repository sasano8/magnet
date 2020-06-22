#! /usr/bin/env sh

echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"

# TODO: echo を直して動くか検証する
echo "
#! /usr/bin/env bash
# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head