#!/bin/bash

INPUT_FILE="credentials.txt"   # file containing credentials (email---password)
BW_BIN="./node_modules/.bin/bw"
delimiter="---"

while read -r line; do
    # Skip empty lines
    [[ -z "$line" ]] && continue

    email="${line%%"$delimiter"*}"  # Get everything before the delimiter
    password="${line##*"$delimiter"}" # Get everything after the delimiter

    echo "Logging in: $email $password"

    # Run login and capture output
    output=$($BW_BIN login "$email" "$password" 2>&1)

    # Check if login succeeded
    if [[ "$output" == *"BW_SESSION"* ]]; then
        echo "Login successful for $email"

        # Extract BW_SESSION from output
        session=$(echo "$output" | grep -oP 'BW_SESSION="\K[^"]+')

        if [[ -n "$session" ]]; then
            export BW_SESSION="$session"

            # Export vault to a uniquely named file
            out_file="${email//[^a-zA-Z0-9]/_}_data.json"
            $BW_BIN export --format json --output "$out_file" --session "$session"

            echo "Exported vault to $out_file"

            # Logging out
            $BW_BIN logout
        else
            echo "Failed to extract session key for $email" >&2
        fi
    else
        echo "Login failed for $email" >&2
        echo "Context: $output" >&2
    fi
    echo
done < "$INPUT_FILE"
