FROM python:3.12-alpine

LABEL maintainer="DYNKV Studio <contact@dynkv.com>"
LABEL project="WCSSTP™ Protocol Test Suite"

WORKDIR /app

COPY wcsstp_core.py test_wcsstp.py server.py ./

# Run unit test suite during build to guarantee 100% integrity
RUN python test_wcsstp.py

RUN mkdir -p /data

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8081/health')" || exit 1

ENTRYPOINT ["python", "server.py"]
