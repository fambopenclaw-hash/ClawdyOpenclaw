#!/usr/bin/env bash
# Weather skill wrapper: returns simple text output without emojis.

set -euo pipefail

LOCATION="${1:-Kuala+Lumpur}"
LOCATION_URL="${LOCATION// /+}"

# Use wttr.in plain format (still may contain emojis, we'll strip them)
if WTR_OUT=$(curl -sS --fail "wttr.in/${LOCATION_URL}?format=%l:+%t+%h+%w" 2>/dev/null); then
    LOC_NAME=$(echo "$WTR_OUT" | cut -d: -f1)
    REST=$(echo "$WTR_OUT" | cut -d: -f2- | tr -s ' ')
    TEMP=$(echo "$REST" | awk '{print $1}')
    HUM=$(echo "$REST" | awk '{print $2}')
    WIND=$(echo "$REST" | awk '{print $3}')
    echo "Location: $LOC_NAME"
    echo "Temperature: $TEMP"
    echo "Humidity: $HUM"
    echo "Wind: $WIND"
    exit 0
fi

# Fallback to Open-Meteo
GEO_JSON=$(curl -s "https://geocoding-api.open-meteo.com/v1/search?name=${LOCATION_URL}&count=1&language=en&format=json")
LAT=$(echo "$GEO_JSON" | grep -o '"latitude":[0-9.]*' | head -1 | cut -d: -f2)
LON=$(echo "$GEO_JSON" | grep -o '"longitude":[0-9.]*' | head -1 | cut -d: -f2)

if [[ -z "$LAT" || -z "$LON" ]]; then
    LAT=3.1390
    LON=101.6869
fi

WEATHER_JSON=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current_weather=true&timezone=auto")
TEMP=$(echo "$WEATHER_JSON" | grep -o '"temperature":[0-9][0-9.-]*' | head -1 | cut -d: -f2)
WIND=$(echo "$WEATHER_JSON" | grep -o '"windspeed":[0-9][0-9.-]*' | head -1 | cut -d: -f2)

LOC_DISPLAY="${LOCATION//+/ }"
echo "Location: $LOC_DISPLAY"
echo "Temperature: $TEMP°C"
echo "Wind: $WIND km/h"
