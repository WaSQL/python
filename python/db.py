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

https://stackoverflow.com/questions/2349991/how-to-import-other-python-files
"""

#imports
try:
    import sys
    import config
    import common
except ImportError as err:
    sys.exit(err)


def queryResults(dbname,query,params):
    if dbname in config.DATABASE:
        #add DATABASE settings to params
        for k in config.DATABASE[dbname]:
            params[k] = config.DATABASE[dbname][k]
        #HANA
        if config.DATABASE[dbname]['dbtype'].startswith('hana'):
            import hanadb
            return hanadb.queryResults(query,params)
        #MSSQL
        if config.DATABASE[dbname]['dbtype'].startswith('mssql'):
            import mssqldb
            return mssqldb.queryResults(query,params)
        #Mysql
        if config.DATABASE[dbname]['dbtype'].startswith('mysql'):
            import mysqldb
            return mysqldb.queryResults(query,params)
        #ORACLE
        if config.DATABASE[dbname]['dbtype'].startswith('oracle'):
            import oracledb
            return oracledb.queryResults(query,params)
        #SNOWFLAKE
        if config.DATABASE[dbname]['dbtype'].startswith('snowflake'):
            import snowflakedb
            return snowflakedb.queryResults(query,params)
        #SQLITE
        if config.DATABASE[dbname]['dbtype'].startswith('sqlite'):
            import sqlitedb
            return sqlitedb.queryResults(query,params)