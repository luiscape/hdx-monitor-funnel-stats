##################################################
# Funnel Stats micro-service. Supports the
# HDX Monitor.
##################################################

FROM python:2.7.10

MAINTAINER Luis Capelo <capelo@un.org>


# Clone app and install dependencies.
RUN \
  git clone https://github.com/luiscape/hdx-monitor-funnel-stats \
  && cd hdx-monitor-funnel-stats \
  && make setup
  
WORKDIR "/hdx-monitor-funnel-stats"

EXPOSE 7000

CMD ["make", "run"]
