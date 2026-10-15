# Records the README GIFs. See "Changing the themes" in README.md.
FROM ghcr.io/charmbracelet/vhs@sha256:ea49a6a1c529be83153e88321892b5585964418f0b9055e8c1e0d732194234a3

RUN apt-get update \
 && apt-get install -y --no-install-recommends nodejs npm \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code@2.1.300

COPY demo.tape record.sh /opt/
ENTRYPOINT ["/opt/record.sh"]
