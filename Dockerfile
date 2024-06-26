FROM python:3.11.9-slim-bookworm

ENV DJANGO_SETTINGS_MODULE francoralite.settings.base
ENV KEYCLOAK_DEFAULT_ACCESS ALLOW
ENV KEYCLOAK_REALM francoralite
ENV KEYCLOAK_SERVER_URL http://keycloak.francoralite.localhost:50000/auth/
ENV KEYCLOAK_METHOD_VALIDATE_TOKEN DECODE
ENV KEYCLOAK_CLIENT_PUBLIC_KEY abcd123
ENV KEYCLOAK_CLIENT_ID francoralite
ENV KEYCLOAK_CLIENT_SECRET_KEY abc123
ENV KEYCLOAK_AUTHORIZATION_CONFIG /tmp/authorization_config.json

WORKDIR /srv/app

# Prepare volumes targets
RUN mkdir -p /srv/app \
  && mkdir -p /srv/media \
  && mkdir -p /srv/static \
  && chown -R www-data:www-data /srv/media /srv/static
VOLUME ["/srv/app", "/srv/media", "/srv/static"]

# Prepare dependencies
RUN apt update \
  && apt install -y curl default-libmysqlclient-dev gcc git pkg-config \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

# Add dependencies requirements
ADD README.md requirements.txt setup.py /srv/app/

# Install Python dependencies
RUN pip install simple-yaml \
  && pip install --no-cache-dir -r /srv/app/requirements.txt

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=10s --retries=20 --timeout=2s \
  CMD curl -f http://localhost:8000/ || exit 1

# Command
CMD ["/srv/app/scripts/start_api.sh"]

# Copy source code
ADD . .
