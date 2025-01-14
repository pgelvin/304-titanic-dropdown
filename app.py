######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic - Pat Gelvin'
color1='#92A5E8'
color2='#333EFF'
color3='#FF33FF'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/pgelvin/304-titanic-dropdown.git'


###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Female']=df['Sex'].map({'male':0, 'female':1})
df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
variables_list_1=['Survived', 'Embarked', 'Sex', 'Fare', 'Age']
variables_list_2=['Survived', 'Embarked', 'Sex']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
# dropdown one
app.layout = html.Div([
    html.H3('Choose a dropdown variable for a statistical summary:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list_1],
        value=variables_list_1[0]
    ),
# dropdown two
    dcc.Dropdown(
        id='slicer',
        options=[{'label': i, 'value': i} for i in variables_list_2],
        value=variables_list_2[1]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value'),Input('slicer','value')]) # dropdown one and two inputs
def display_value(continuous_var, second_dimension):
    grouped_mean=df.groupby(['Cabin Class', second_dimension])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['first'].index,
        y=results.loc['first'][continuous_var],
        name='First Class',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['second'].index,
        y=results.loc['second'][continuous_var],
        name='Second Class',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['third'].index,
        y=results.loc['third'][continuous_var],
        name='Third Class',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped Bar chart',
        xaxis = dict(title = str(second_dimension)), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
