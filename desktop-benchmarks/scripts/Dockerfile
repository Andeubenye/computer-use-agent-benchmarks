FROM claude-benchmark-desktop:v1
USER root
RUN apt-get update && apt-get install -y --no-install-recommends libreoffice-calc fonts-liberation \
    && rm -rf /var/lib/apt/lists/*
COPY start-desktop.sh /opt/desktop/start-csv.sh
RUN chmod 755 /opt/desktop/start-csv.sh
USER agent
ENV DISPLAY=:1
WORKDIR /home/agent
ENTRYPOINT ["/opt/desktop/start-csv.sh"]
