#!/bin/bash
   docker-compose --env-file .venv/.env -f  '.docker/docker_compose_configuration.yml' up -d --build