"""
Install needed modules
	Oracle - https://cx-oracle.readthedocs.io/en/latest/user_guide/introduction.html
		python -m pip install cx_Oracle
	Postgres - https://stackoverflow.com/questions/413228/pygresql-vs-psycopg2
		python -m pip install psycopg2
	HANA - https://github.com/SAP/PyHDB
		python -m pip install pyhdb
	ODBC - https://github.com/mkleehammer/pyodbc/wiki
		python -m pip install pyodbc
	Mysql - https://www.w3schools.com/python/python_mysql_select.asp
		python -m pip install mysql.connector
	MsSQL - https://docs.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server
		python -m pip install pymssql
	SQLite - https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

	Snowflake
		python -m pip install --upgrade snowflake-connector-python


"""
import logging
import sys
import configparser as cp
import cx_Oracle as ora
import psycopg2 as postgres_c
import pyhdb as hana_c
import pyodbc as odbc_c
import mysql.connector as mysql_c
import sqlite3 as sqlite_c
import pymssql as mssql_c
#import snowflake.connector as snowflake_c

"""
https://stackoverflow.com/questions/14509192/how-to-import-functions-from-other-projects-in-python
"""
CONFIG_LOCATION = './db_config'

def get_db_type(dbname):
    """
    :param dbname: name that corresponds to db_config
    :return: 
    """
    db_config = cp.ConfigParser()
    try:
        db_config.read(CONFIG_LOCATION)
        dbtype = db_config.get(dbname, 'dbtype')
    except:
        logging.error(sys.exc_info())
        exit(1)

    return db_config.get(dbname, 'dbtype')


def get_db_config(dbname):
    """
    :param dbname: name that corresponds to db_config
    :return:
    """
    db_config = cp.ConfigParser()
    try:
        db_config.read(CONFIG_LOCATION)
    except:
        logging.error(sys.exc_info())
        exit(1)

    return db_config


def get_connection(dbname):
    """
    Get connection for database type using db_config parameters
    :param dbname:
    :return: connection object
    """
    conn = None
    db_config = cp.ConfigParser()
    try:
        db_config.read(CONFIG_LOCATION)
        dbtype = db_config.get(dbname, 'dbtype')

        if dbtype == 'POSTGRESQL':
            conn_str = __get_pg_conn_string(dbname=dbname, db_config=db_config)
            conn = psy.connect(conn_str)

        elif dbtype == 'HANA':
            conn_dict = __get_hana_conn_string(dbname=dbname, db_config=db_config)
            conn = pyhdb.connect(host=conn_dict['host'], port=conn_dict['port'], user=conn_dict['user'],
                                 password=conn_dict['password'])

        elif dbtype == 'SNOWFLAKE':
            conn_dict = __get_snowflake_conn_string(dbname=dbname, db_config=db_config)
            conn = sfc.connect(account=conn_dict['account'], user=conn_dict['user'],
                               password=conn_dict['password'], database=conn_dict['database'],
                               schema=conn_dict['schema'], warehouse=conn_dict['warehouse'], role=conn_dict['role'])

        elif dbtype == 'ORACLE':
            conn_str = __get_ora_conn_string(dbname=dbname, db_config=db_config)
            conn = ora.Connection(conn_str, encoding="UTF-8")

        else:
            raise Exception("No connection formatting configuration exists for {}".format(dbtype))
        return conn
    except:
        logging.error(sys.exc_info())
        exit(1)


def __get_pg_conn_string(dbname, db_config):
    """
    Build postgresql connection string
    :param dbname:
    :return: formatted connection string
    """
    return """dbname={} user={} password={} host={} port={}""". \
        format(db_config.get(dbname, 'database'),
               db_config.get(dbname, 'user'),
               db_config.get(dbname, 'password'),
               db_config.get(dbname, 'host'),
               db_config.get(dbname, 'port'))


def __get_ora_conn_string(dbname, db_config):
    """
    Build etl connection string
    :param dbname:
    :return: formatted connection string
    """
    return """{}/{}@{}:{}/{}""".\
        format(db_config.get(dbname, 'user'),
               db_config.get(dbname, 'password'),
               db_config.get(dbname, 'host'),
               db_config.get(dbname, 'port'),
               db_config.get(dbname, 'tsname'))


def __get_hana_conn_string(dbname, db_config):
    """
    Build hana connection dictionary
    :param dbname:
    :return: connection dictionary
    """
    hana_conn_dict = {}
    hana_conn_dict.update({'host': db_config.get(dbname, 'host')})
    hana_conn_dict.update({'port': db_config.get(dbname, 'port')})
    hana_conn_dict.update({'user': db_config.get(dbname, 'user')})
    hana_conn_dict.update({'password': db_config.get(dbname, 'password')})

    return hana_conn_dict


def __get_snowflake_conn_string(dbname, db_config):

    snowflake_conn_dict = {}
    snowflake_conn_dict.update({'account': db_config.get(dbname, 'account')})
    snowflake_conn_dict.update({'user': db_config.get(dbname, 'user')})
    snowflake_conn_dict.update({'password': db_config.get(dbname, 'password')})
    snowflake_conn_dict.update({'database': db_config.get(dbname, 'database')})
    snowflake_conn_dict.update({'schema': db_config.get(dbname, 'schema')})
    snowflake_conn_dict.update({'warehouse': db_config.get(dbname, 'warehouse')})
    snowflake_conn_dict.update({'role': db_config.get(dbname, 'role')})

    return snowflake_conn_dict


def db_get_query_results(dbname, query):
    """
    :param db: the database name that corresponds to a db_config
    :param query: the actual sql statement
    :return a list of dictionaries is returned:
    """
    conn = get_connection(dbname=dbname)
    cur = conn.cursor()
    results = None

    try:
        cur.execute(query)
        columns = cur.description
        results = [{columns[index][0]: column for index, column in enumerate(value)} for value in cur.fetchall()]
    except:
        logging.error(sys.exc_info())
        exit(1)

    try:
        cur.close()
        conn.close()
    except:
        pass

    return results


def db_get_query_result(dbname, query):
    """
    :param dbname:
    :param query:
    :return:
    """
    results = db_get_query_results(dbname=dbname, query=query)
    return results[0]


def db_execute_query(dbname, query):
    results = db_get_query_results(dbname=dbname, query=query)
    return


def db_get_table_metadata_hana(dbname, table):
    query = 'select * from table_columns where table_name = {} order by position'.format(table.upper())
    results=db_get_query_results(dbname=dbname, query=query)
    return results


def db_get_table_metadata(dbname, table):
    dbtype = get_db_type(dbname=dbname).upper()
    if dbtype == "HANA":
        db_get_table_metadata_hana( dbname=dbname, table=table)
