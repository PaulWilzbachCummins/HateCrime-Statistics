from flask import Blueprint, render_template, request
import psycopg2
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

conn = psycopg2.connect(dbname='crimes')
cur = conn.cursor()

def generateBiasQuery(bias="All"):

  query = '' 
  print("User Input: ", bias)

  if (bias == 'race'):
    query = 'select state, race, round(100000*race/pop, 3) per_capita FROM states order by per_capita desc;' 
  elif (bias == 'religion'):
    query = 'select state, religion, round(100000*religion/pop, 3) per_capita FROM states order by per_capita desc;'
  elif (bias == 'ethnicity'):
    query = 'select state, eth, round(100000*eth/pop, 3) per_capita FROM states order by per_capita desc;'
  elif (bias == 'disability'):
    query = 'select state, disability, round(100000*disability/pop, 3) per_capita FROM states order by per_capita desc;'
  elif (bias == 'gender'):
    query = 'select state, gender, round(100000*gender/pop, 3) per_capita FROM states order by per_capita desc;'
  elif (bias == 'gender-id'):
    query = 'select state, gender_id, round(100000*gender_id/pop, 3) per_capita FROM states order by per_capita desc;'
  elif (bias == 'sexual-orientation'):
    query = 'select state, sexual_orientation, round(100000*sexual_orientation/pop, 3) per_capita FROM states order by per_capita desc;'
  else:
    query = 'select state, total_crime, round(100000*total_crime/pop, 3) per_capita from states order by per_capita desc;'

  print("---Execute query: ", query)
  cur.execute(query)
  result = cur.fetchall()
  return result

def generatePoliticalQuery():

  query = """select party, sum(total_crime) num_crimes, round(100000*sum(total_crime)/sum(pop),
          3) per_pop_party, round(100000*sum(total_crime)/(select sum(pop) from states), 3)
          per_pop_tot, round(sum(total_crime)/count(party),2) avg_per_state, round(sum(per_agency)
          /count(party), 3) avg_per_agency from states group by party limit 10;"""
  print("---Execute query: ", query)
  cur.execute(query)
  result = cur.fetchall()
  return result;

def generatePlots():
  #Retrieving data from database
  cur.execute("select party, sum(total_crime) num_crimes, round(100000*sum(total_crime)/sum(pop), 3) per_pop_party, round(100000*sum(total_crime)/(select sum(pop) from states), 3) per_pop_tot, round(sum(total_crime)/count(party),2) avg_per_state, round(sum(per_agency)/count(party), 3) avg_per_agency from states group by party limit 10;")
  q = cur.fetchall()

  #Closing connection to database
  #conn.close()

  #Retrieving values from query
  #total crimes
  rc = q[1][1]
  dc = q[0][1]
  #Crimes per cap (total)
  rt = q[1][3]
  dt = q[0][3]
  #Crimes per cap (party)
  rp = q[1][2]
  dp = q[0][2]

  #Creating dataframe
  dict = {'Party':['Republican', 'Democrat'], 'Crimes':[rc,dc], 
          'Crimes Per Capita (Total)':[rt,dt], 'Crimes Per Capita (Party)':[rp,dp]}
  df = pd.DataFrame(dict)

  #Pie chart
  pie = px.pie(
      df, 
      values='Crimes', 
      names='Party',
      color='Party',
      color_discrete_map={'Republican':'red', 'Democrat':'blue'},
      title="Total Number of Reported Hate Crimes")

  #Bar charts
  cx=['Crimes Per Capita (Total)','Crimes Per Capita (Party)'] # X-values 
  bar = go.Figure(data=[
      go.Bar(name='Republican', x=cx, y=[rt,rp], marker_color='red'),
      go.Bar(name='Democrat', x=cx, y=[dt,dp], marker_color = 'blue')
  ])
  # Change the bar mode
  bar.update_layout(barmode='group', 
                    title_text="Hate Crimes Per Capita")
  
  #Writing to png
  pie_name = "pie.png"
  bar_name = "bar.png"
  abs_path = "website/static/images/"
  rel_path = "/static/images/"
  
  pie.write_image(abs_path + pie_name)
  bar.write_image(abs_path + bar_name)
   
  pie_path =rel_path + pie_name
  bar_path = rel_path + bar_name
 
  return pie_path, bar_path

def generateCrimesTable(data, bias="All"):
  headings = ("State", "Number of Hate Crimes (" + bias + ")", "Per Capita")
  data_list=list()
  
  for row in data:
    data_list.append(row)
    
  data=tuple(data_list)
   
  return headings, data

def generatePoliticalTable(data):
  headings = ("Political Party", "Total Hate Crimes reported", 
	      "Hate Crimes per Capita (by Party)", "Hate Crimes per Capita (Total)",
              "Avg Hate Crimes per State", 
              "Avg Hate  Crimes per State Agency")
  data_list=list()

  for row in data:
    data_list.append(row)

  data=tuple(data_list)

  return headings, data

#headings = ("State", "Number of Crimes")
#data = (("California", "454"),("Florida", "67"))

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("home.html")

@views.route('/political-affiliation', methods=['GET', 'POST'])
def political_affiliation():
  result = generatePoliticalQuery()
  headings, data = generatePoliticalTable(result)
  plot1, plot2 = generatePlots()
  return render_template("political_affiliation.html", headings=headings, data=data, plot1=plot1, plot2=plot2)

@views.route('/crimes-ranking', methods=['GET', 'POST'])
def crimes_ranking():
  bias = request.form.get('bias', default="All")
  result = generateBiasQuery(bias)
  headings, data = generateCrimesTable(result, bias)
  return render_template("crimes_ranking.html", headings=headings, data=data)
