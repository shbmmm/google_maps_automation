#!/bin/bash

# Create a temporary file to store coordinates
temp_file=$(mktemp)

# Extract coordinates from filenames and store in temp file
for file in mumbai_*; do
  if [[ $file =~ mumbai_([0-9]+\.[0-9]+)_([0-9]+\.[0-9]+) ]]; then
    echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]} $file" >> $temp_file
  fi
done

# Sort the coordinates (first by latitude descending, then by longitude ascending)
sort -k1,1nr -k2,2n $temp_file > sorted_coords.txt

# Read sorted coordinates and create a grid
mkdir -p sorted_grid
row=0
prev_lat=""
while read lat lon file; do
  if [[ "$lat" != "$prev_lat" ]]; then
    ((row++))
    col=0
  fi
  ((col++))
  new_filename=$(printf "row_%02d_col_%02d_%s" "$row" "$col" "$file")
  cp "$file" "sorted_grid/$new_filename"
  prev_lat="$lat"
done < sorted_coords.txt

# Clean up temporary files
rm $temp_file
rm sorted_coords.txt

echo "Images have been arranged into the 'sorted_grid' directory."

