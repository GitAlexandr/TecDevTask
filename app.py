import csv
import json
import redis
import cassandra 
from pars.parser import parse_data
from db.db import DatabaseService
import traceback

def main():
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)

    cassandra_host = '127.0.0.1'
    cassandra_port = 9042
    cassandra_keyspace = 'your_keyspace'
    cassandra_username = 'cassandra'
    cassandra_password = 'cassandra'

    try:
        with DatabaseService(
            host=cassandra_host,
            port=cassandra_port,
            keyspace=cassandra_keyspace,
            username=cassandra_username,
            password=cassandra_password
        ) as database_service:

            csv_file_path = 'habr.csv'
            urls_to_parse = read_urls_from_csv(csv_file_path)

            for url_to_parse in urls_to_parse:
                parsed_data = parse_data(url_to_parse)
                if parsed_data:
                    redis_key = 'parsed_data'
                    redis_conn.set(redis_key, json.dumps(parsed_data))

                    database_service.write_data(parsed_data)
                    print(f"Данные для {url_to_parse} успешно получены и записаны в Redis и ScyllaDB.")
                else:
                    print(f"Ошибка при парсинге для {url_to_parse} или ссылка нерабочая")
    
    except cassandra.UnresolvableContactPoints as e:
        print(f"Error connecting to Cassandra: {e}")

    except Exception as e:
        print("An unexpected error occurred:")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
