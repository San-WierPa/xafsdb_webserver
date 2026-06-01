#!/usr/bin/env bash
set -e

sudo mkdir -p /srv/mongodb
sudo chown -R 1001:1001 /srv/mongodb
docker compose -f xafsdb_deployment/docker-compose.yaml --env-file xafsdb_deployment/.env pull
docker compose -f xafsdb_deployment/docker-compose.yaml --env-file xafsdb_deployment/.env up -d
docker compose -f xafsdb_deployment/docker-compose.yaml --env-file xafsdb_deployment/.env ps
