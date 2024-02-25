#!/bin/bash

while true; do
  # Generate random number between 0 and 100 for food capacity
  FOOD_CAPACITY_PERCENTAGE=$((RANDOM % 101))
  
  DEVICE_LOCATION=("kitchen" "bedroom")
  RANDOM_LOCATION_INDEX=$((RANDOM % 2))
  SELECTED_LOCATION=${DEVICE_LOCATION[$RANDOM_LOCATION_INDEX]}
  
  JSON_MESSAGE="{\"food_capacity\": $FOOD_CAPACITY_PERCENTAGE, \"device_location\": \"$SELECTED_LOCATION\"}"

  echo "Payload: $JSON_MESSAGE"

  aws iot-data publish --topic cat-feeder/states --cli-binary-format raw-in-base64-out --payload "$JSON_MESSAGE"
  
  sleep 1
done
