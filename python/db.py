#! python
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