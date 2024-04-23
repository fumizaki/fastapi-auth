FROM postgres:12.13-alpine

ENV TZ Asia/Tokyo
ENV LANG js_JP.UTF-8
ENV POSTGRES_DB rdb
ENV POSTGRES_USER rdb
ENV POSTGRES_PASSWORD rdb

# webserviceのmigrationツールで管理するため、コメントアウト
# ADD ./rdb/init_sql/* /docker-entrypoint-initdb.d
ADD ./rdb/script/* /script
RUN chmod +x /script