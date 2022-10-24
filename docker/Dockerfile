FROM python:3.10.8-slim as builder

RUN apt-get update && \
    apt-get --yes install \
      libffi-dev \
      tmux && \
    rm -rf /var/apt/cache/* && \
    pip install pyOpenSSL

FROM builder

ARG COMMIT_HASH
ARG VERSION

LABEL de.gematik.vendor="gematik GmbH" \
      maintainer="software-development@gematik.de" \
      de.gematik.app="ePA Forschungsfreigabe" \
      de.gematik.git-repo-name="https://gitlab.prod.ccs.gematik.solutions/git/refImpl/epa/poc-epa-forschungsdatenfreigabe.git" \
      de.gematik.commit-sha=$COMMIT_HASH \
      de.gematik.version=$VERSION

EXPOSE 20001 20002 20003

COPY . /app

WORKDIR /app

COPY docker/tmux.conf /root/.tmux.conf

RUN pip install -r requirements.txt && \
    chmod +x /app/start.sh

ENTRYPOINT [ "/app/start.sh" ]
