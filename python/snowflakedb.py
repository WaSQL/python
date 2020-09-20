#! python
"""
Installation
    python -m pip install --upgrade snowflake-connector-python
       If it fails then go to https://visualstudio.microsoft.com/visual-cpp-build-tools/
           download build tools
           install c++ build tools
           reboot and try again

"""


#imports
try:
    import snowflake.connector
    import config
    import common
except ImportError as err:
    sys.exit(err)
###########################################
#Python’s default arguments are evaluated once when the function is defined, not each time the function is called.
def connect(params):
    try:
        dbconfig = {}
        #check config.CONFIG
        if 'dbuser' in config.CONFIG:
            dbconfig['user'] = config.CONFIG['dbuser']

        if 'dbpass' in config.CONFIG:
            dbconfig['password'] = config.CONFIG['dbpass']

        if 'dbaccount' in config.CONFIG:
            dbconfig['account'] = config.CONFIG['dbaccount']

        if 'dbwarehouse' in config.CONFIG:
            dbconfig['warehouse'] = config.CONFIG['dbwarehouse']

        if 'dbname' in config.CONFIG:
            dbconfig['database'] = config.CONFIG['dbname']

        if 'dbschema' in config.CONFIG:
            dbconfig['schema'] = config.CONFIG['dbschema']

        #check params and override any that are passed in
        if 'dbuser' in params:
            dbconfig['user'] = params['dbuser']

        if 'dbpass' in params:
            dbconfig['password'] = params['dbpass']

        if 'dbaccount' in params:
            dbconfig['account'] = params['dbaccount']

        if 'dbwarehouse' in params:
            dbconfig['warehouse'] = params['dbwarehouse']

        if 'dbname' in params:
            dbconfig['database'] = params['dbname']

        if 'dbschema' in params:
            dbconfig['schema'] = params['dbschema']

        # connect
        conn_snowflake = snowflake.connector.connect(**dbconfig)
        cur_snowflake = conn_snowflake.cursor(dictionary=True)
            
        #need to return both cur and conn so conn stays around
        return cur_snowflake, conn_snowflake
        
    except snowflake.connector.Error as err:
        print("snowflakedb.connect error: {}".format(err))
        return false

###########################################
def queryResults(query,params):
    try:
        #connect
        cur_snowflake, conn_snowflake =  connect(params)
        #now execute the query
        cur_snowflake.execute(query)
        #NOTE: columns names can be accessed by cur_snowflake.column_names
        recs = cur_snowflake.fetchall()
        #NOTE: get row count with cur_snowflake.rowcount
        if type(recs) in (tuple, list):
            return recs
        else:
            return []
        
    except snowflake.connector.Error as err:
        return ("snowflakedb.queryResults error: {}".format(err))
###########################################
