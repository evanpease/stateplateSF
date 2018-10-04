from flask import render_template
from flaskexample.a_Model import ModelIt
from flaskexample import app
from flask import request
from flask import jsonify
import json
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

# Python code to connect to Postgres
user = 'postgres' #add your Postgres username here
password = '1234'
host = 'localhost'
port = '5432'
dbname = 'sf_resto_recs_db'
# db = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db_name))
con = None
con = psycopg2.connect(database = dbname, user = user, host = host, password = password)

@app.route('/')
@app.route('/index')
@app.route('/input_state')
def view_method():
    sql_query = """
		SELECT "State" FROM recommendations;
		"""
    query_results=pd.read_sql_query(sql_query,con)
    dropdown_list = list(query_results['State'])
    return render_template('input_state.html', title='StatePlateSF', dropdown_list=dropdown_list)

@app.route('/output_restaurant', methods=['GET','POST'])
def resto_output():
    state_req = request.form.get("statechoice")
    # state_req_pd = state_req.replace(" ","-")
    # state_req_pd = state_req_pd.lower()
    sql_query = """
            SELECT "State","RestaurantNames","RestaurantCosSim","RestaurantMenuURL",\
            "RestaurantAddress", "StateSimilarityName", "StateSimilarityCosSim"\
            FROM recommendations WHERE "State" = '%s' ;
            """ % state_req
    data_from_sql=pd.read_sql_query(sql_query,con)
    ex_list = data_from_sql['RestaurantNames'].tolist()[0].replace('{','').replace('}','').replace('"','').split(',')
    if len(ex_list)>5:
        rec_RestName = list()
        for el in range(len(ex_list)):
            if ex_list[el][0]==' ':
                rec_RestName[-1]=rec_RestName[-1]+','+ex_list[el]
            else:
                rec_RestName.append(ex_list[el])
    else:
        rec_RestName = ex_list
    rec_RestSim = [float(x) for x in data_from_sql['RestaurantCosSim'].tolist()[0][1:-1].split(',')]
    rec_RestURL = data_from_sql['RestaurantMenuURL'].tolist()[0][1:-1].split(',')
    rec_RestAddress = data_from_sql['RestaurantAddress'].tolist()[0][2:-2].split('","')

    sql_query2 = """
        SELECT "State" FROM recommendations;
        """
    state_list=pd.read_sql_query(sql_query2,con)
    dropdown_list = list(state_list['State'])
    return render_template('output_restaurant.html', state_req=state_req, dropdown_list=dropdown_list, restName1=rec_RestName[0],\
        restName2=rec_RestName[1], restName3=rec_RestName[2], restName4=rec_RestName[3], restName5=rec_RestName[4],\
        restURL1=rec_RestURL[0], restURL2=rec_RestURL[1], restURL3=rec_RestURL[2], restURL4=rec_RestURL[3], restURL5=rec_RestURL[4],\
        restAdd1=rec_RestAddress[0], restAdd2=rec_RestAddress[1], restAdd3=rec_RestAddress[2], restAdd4=rec_RestAddress[3],\
        restAdd5=rec_RestAddress[4], restSim1=rec_RestSim[0], restSim2=rec_RestSim[1], restSim3=rec_RestSim[2], restSim4=rec_RestSim[3],\
        restSim5=rec_RestSim[4])

@app.route('/prez')
def view_presentation():
    return render_template('prez.html', title='Demo Presentation')
