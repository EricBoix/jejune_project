FROM neo4j:5.22.0

ENV NEO4J_PLUGINS '[ "apoc" ]'
ENV NEO4J_dbms_security_procedures_unrestricted apoc.*

COPY ./apoc-5.22.0-core.jar /var/lib/neo4j/plugins

EXPOSE 7474 7687
