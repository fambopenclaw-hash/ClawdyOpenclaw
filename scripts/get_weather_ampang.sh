#!/usr/bin/env bash
# Weather fetch wrapper with retry and fallback
# Usage: get_weather_ampang

LOCATION="Ampang,+Selangor"
FALLBACK_LOC="Ampang"
MAX_RETRIES=3
DELAYS=(1 2 3)

fetch_wttr() {
    local loc="$1"
    curl -s "wttr.in/${loc}?m" 2>/dev/null
}

for i in $(seq 0 $((MAX_RETRIES-1))); do
    result=$(fetch_wttr "$LOCATION")
    if [[ -n "$result" && ! "$result" =~ "running out of queries" ]]; then
        echo "$result"
        exit 0
    fi
    sleep "${DELAYS[$i]}"
done

# Fallback to simpler format or alternative location
result=$(fetch_wttr "$LOCATION?format=%C+%t")
if [[ -n "$result" && ! "$result" =~ "running out of queries" ]]; then
    echo "$result"
    exit 0
fi

# Final fallback to just Ampang location
result=$(fetch_wttr "$FALLBACK_LOC?m")
if [[ -n "$result" && ! "$result" =~ "running out of queries" ]]; then
    echo "$result"
    exit 0
fi

# If all fail, output a clear error message
echo "Weather service unavailable after multiple attempts."
exit 1
