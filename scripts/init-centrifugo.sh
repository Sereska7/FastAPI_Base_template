#!/bin/bash

cat <<EOF> "$CONFIG"
{
  "token_hmac_secret_key": "$CLIENTS__CENTRIFUGO__TOKEN_HMAC_SECRET_KEY",
  "api_key": "$CLIENTS__CENTRIFUGO__X_API_KEY",
  "admin_password": "$CLIENTS__CENTRIFUGO__ADMIN_PASSWORD",
  "admin_secret": "$CLIENTS__CENTRIFUGO__ADMIN_SECRET",
  "admin": true,
  "client_queue_max_size": 31457280,

  "allowed_origins": ["*"],
  "presence": true,

  "history_size": 2,
  "history_ttl": "60s",

  "join_leave": false,

  "proxy_http_headers": [
    "Origin",
    "User-Agent",
    "Cookie",
    "Authorization",
    "X-Real-Ip",
    "X-Forwarded-For",
    "X-Request-Id"
  ],

  "namespaces": [
    {
      "name": "country",
      "allow_subscribe_for_client": true,
      "history_size": 1,
      "history_ttl": "720h",
      "force_positioning": true,
      "force_recovery": true,
      "allow_publish_for_client": true
    },
    {
      "name": "city",
      "allow_subscribe_for_client": true,
      "history_size": 1,
      "history_ttl": "720h",
      "force_positioning": true,
      "force_recovery": true,
      "allow_publish_for_client": true
    }
  ],
  "prometheus": true,
  "engine": "redis",
  "redis_address": "$REDIS__HOST:$REDIS__PORT",
  "redis_password": "$REDIS__PASSWORD"
}
EOF

exec centrifugo -c config.json
