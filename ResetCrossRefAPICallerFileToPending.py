import pyodbc
import configparser
import sys
import time
import pdb

try:
    config = configparser.ConfigParser()

    #deployed application setup for reading configuration file.
    complete_executable_path = sys.executable.replace("ResetCrossRefAPICallerFileToPending.exe","configurationFile.ini")

    #code level setup for reading configuration file.
    #complete_executable_path = sys.path[0] + '\configurationFile.ini'

    config.read(complete_executable_path)

    #print(f"Executable path: {complete_executable_path}")
    #c.set_trace()

    default_settings = config['DEFAULT']

    server_name = default_settings['server_name']
    database_name = default_settings['database_name']
    user_id = default_settings['user_id']
    database_password = default_settings['database_password']

    batch_id = input("Please enter batchid to be reset:")
    sql_statement = "select RefId,JobId from [wms_JobsProcessTracker] where RefId='"+ batch_id +"'"

except Exception as e:
    print(f"Error {e}.")
    #print(f"Error {e}. Application Path is at {complete_executable_path} and sys executable is at {sys.executable}.")

try:
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=' + server_name + ';'
                          'Database=' + database_name + ';'
                          'UID=' + user_id + ';'
                          'PWD='+ database_password +';'
                          "Trusted_Connection=No")

    cursor = conn.cursor()
    cursor.execute(sql_statement)

    is_found = False

    for row in cursor:
        print(row)
        is_found = True
        break

    if is_found:
        #sql_pending_statement = "exec usp_crossRefCaller_pending @batchId=" + batch_id + ""
        sql_exec_pending_statement = "SET NOCOUNT ON; exec [dbo].[usp_crossRefCaller_pending] ?"
        values = (batch_id)
        cursor.execute(sql_exec_pending_statement,batch_id)
        cursor.commit()

        print(f"Successfully put to pending batchid {batch_id}, please check!")
    else:
        print(f"Batch id {batch_id} is not found!")

except Exception as e:
    print(f'Error: {e}')

time.sleep(5)