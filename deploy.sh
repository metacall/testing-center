#!/bin/bash

# Accept the repo path as an argument
repo_path=$1

# Run the metacall-deploy command and store the output
output=$(metacall-deploy --inspect OpenAPIv3 --dev --workdir "$repo_path")

# Parse the JSON output using jq to extract the server URL and paths
server_url=$(echo "$output" | jq -r '.[0].servers[0].url')
paths=$(echo "$output" | jq -r '.[0].paths | keys[]')

# Output the server URL and paths
echo "Server URL: $server_url"
echo "Available Paths:"
for path in $paths; do
    echo "$server_url$path"
done

# Set the server URL as an environment variable
export SERVER_URL=$server_url


# multi line comment
: ' Exmaple output
[
  {
    "openapi": "3.0.0",
    "info": {
      "title": "MetaCall Cloud FaaS deployment 'time-app-web'",
      "description": "",
      "version": "v1"
    },
    "servers": [
      {
        "url": "http://localhost:9000/aa759149a70a/time-app-web/v1",
        "description": "MetaCall Cloud FaaS"
      }
    ],
    "paths": {
      "/call/time": {
        "get": {
          "summary": "",
          "description": "",
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {}
                }
              }
            }
          }
        }
      },
      "/call/index": {
        "get": {
          "summary": "",
          "description": "",
          "responses": {
            "200": {
              "description": "",
              "content": {
                "application/json": {
                  "schema": {}
                }
              }
            }
          }
        }
      }
    }
  }
]
'