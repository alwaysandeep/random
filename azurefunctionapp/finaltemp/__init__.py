import logging

import azure.functions as func
import os
import pyodbc


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    server="tcp:sqlserveraddress.database.windows.net,1433"
    database="SampleDB"
    driver="{ODBC Driver 13 for SQL Server}"
    query=f"SELECT Address FROM dbo.Details where Name={name}"
    username = 'azureuser' 
    password = 'Busn@123'
    db_token = ''
    connection_string = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query) 
    country = cursor.fetchone()
    logging.info(f'country response is: {country}')

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. I think you live here: {country}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
