import numpy as np
import pandas as pd
import folium
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from plotly.subplots import make_subplots


def top_countries_two_axis(data,top_k, sort_by_gross_users = True,log_scale = False):
    '''
    Creates a plotly object for the total and relative number of twitter users by country
    Inputs:
        data (dataframe): dataframe grouped by country
        top_k (int): top-k number of countries to plot
        sort_by_gross_users(bool): If True, it sorts the barchart by the gross number of users; if False,
        sorts the barchart by the relative (per 1,000 people) number of users
        log_scale(bool): if True, it plots a log scale for the total number of users; if
        False, it plots a linear scale
    Returns:
        Plotly object
    '''
    data = data.loc[data["country_long"]!="Antarctica"]
    if sort_by_gross_users:
        data = data.sort_values("n_users",ascending=False)[:top_k]
        title = "the Total Number of Users"
    else:
        data = data.sort_values("users_per_K",ascending=False)[:top_k]
        title = "the Number of Users per 1,000 people"

    if log_scale:
        scale = "log"
        log_title = "-log scale-"
    else:
        scale = 'linear'
        log_title = ""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(x = data["country_long"], y = data["n_users"], 
                         name="Gross users",marker_color = 'rgb(55, 83, 109)', 
                        text = data["users_per_K"], offsetgroup = 0,
                       hovertemplate = "Number of users: %{y:,.0f}<br>" +
                         "Users per 1K: %{text:.2f}<br>" + "<extra></extra>"),secondary_y = False)
    fig.add_trace(go.Bar(x = data["country_long"], y = data["users_per_K"], 
                         name="Users/1k people",marker_color = "#E39E22", 
                        text = data["n_users"], offsetgroup = 1,
                       hovertemplate = "Users per 1K: %{y:,.2f}<br>" +
                         "Number of users:  %{text:,.0f}<br>" +
                         "<extra></extra>"),secondary_y = True)   

    
    fig.update_layout(title = "Top {} Most Active Countries Sorted by {}".format(top_k, title),
                      yaxis={'title':'Users (Millions {})'.format(log_title), 'type':'{}'.format(scale)},
                        plot_bgcolor="#f7fafd")
    fig.update_yaxes(title_text='Users (Millions)', secondary_y = False)
    fig.update_yaxes(title_text='Users (per 1,000 people)', secondary_y = True)
    #fig.write_html("./two_axis_plot.html")
    return fig

def top_cities_two_axis(data,top_k, sort_by_gross_users = True,log_scale = False):
    '''
    Creates a plotly object for the total and relative number of twitter users by country
    Inputs:
        data (dataframe): dataframe grouped by country
        top_k (int): top-k number of countries to plot
        sort_by_gross_users(bool): If True, it sorts the barchart by the gross number of users; if False,
        sorts the barchart by the relative (per 1,000 people) number of users
        log_scale(bool): if True, it plots a log scale for the total number of users; if
        False, it plots a linear scale
    Returns:
        Plotly object
    '''
    if sort_by_gross_users:
        data = data.sort_values("n_users",ascending=False)[:top_k]
        title = "the Total Number of Users"
    else:
        data = data.sort_values("users_per_K",ascending=False)[:top_k]
        title = "the Number of Users per 1,000 people"

    if log_scale:
        scale = "log"
        log_title = "-log scale-"
    else:
        scale = 'linear'
        log_title = ""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(x = data["locality_long"], y = data["n_users"], 
                         name="Gross users",marker_color = 'rgb(55, 83, 109)', 
                        text = data["users_per_K"], offsetgroup = 0,
                       hovertemplate = "Number of users: %{y:,.0f}<br>" +
                         "Users per 1K: %{text:.2f}<br>" + "<extra></extra>"),secondary_y = False)
    fig.add_trace(go.Bar(x = data["locality_long"], y = data["users_per_K"], 
                         name="Users/1k people",marker_color = "#E39E22", 
                        text = data["n_users"], offsetgroup = 1,
                       hovertemplate = "Users per 1K: %{y:,.2f}<br>" +
                         "Number of users:  %{text:,.0f}<br>" +
                         "<extra></extra>"),secondary_y = True)   

    fig.update_layout(title = "Top {} Most Active Cities Sorted by {}".format(top_k, title),
                      yaxis={'title':'Users (Millions {})'.format(log_title), 'type':'{}'.format(scale)},
                        plot_bgcolor="#f7fafd")
    fig.update_yaxes(title_text='Users (Millions)', secondary_y = False)
    fig.update_yaxes(title_text='Users (per 1,000 people)', secondary_y = True)
    #fig.write_html("./two_axis_plot.html")
    return fig

def plot_gdp_and_users(dataframe):
    '''
    Plots a scatterplot of twitter users per 1k people and GDP per capita (2019)
    Inputs:
        dataframe
    Returns:
        Plotly object
    '''
    fig = go.Figure(data = go.Scatter(x = dataframe['gdp_2019'],
                                y = dataframe['users_per_K'],
                                mode = 'markers',
                                text = dataframe['country_long'],
                               marker = dict(size=[9]*len(dataframe),
                                color = ["#38762B"]*len(dataframe)))) 

    fig.update_layout(title ='Twitter Users and GDP per capita 2019',
                          xaxis = {'title':'GDP per capita 2019 (log scale)', 'type':'log'},
                          yaxis = {'title':'Twitter Users per 1,000 people'},
                             plot_bgcolor="#FFFFFF")
    fig.update_xaxes(showgrid = True, gridwidth = 1, gridcolor="#f7fafd")
    fig.update_yaxes(showgrid = True, gridwidth = 1, gridcolor="#f7fafd")
    fig.update_xaxes(showline = True, linewidth = 1, linecolor='black')
    fig.update_yaxes(showline = True, linewidth = 1, linecolor='black')
    fig.update_xaxes(ticks = "outside", tickwidth = .25, tickcolor='black', ticklen = 10)
    fig.update_yaxes(ticks = "outside", tickwidth = .25, tickcolor='black', ticklen = 10)
    fig.update_traces(
        hovertemplate = "<br>".join([
            "GDP per capita: %{x:,.0f}" + "<extra></extra>",
            "Users per 1,000 people: %{y:,.2f}"]))
    return fig

def dot_maps(dataframe,total_users = True):
    '''
    Plots a dot map with total users OR users per 1k people
    Inputs:
        dataframe (pandas dataframe): dataframe of cities
        total_users(bool): If True, uses total number of users. If False, uses users per 1k people
    Returns:
        Folium object
        
    '''
    if total_users:
        var = 'n_users'
    else:
        var = 'users_per_K'
    map_city = folium.Map( location = [0,0], 
                          zoom_start=2, 
                          tiles='cartodbpositron')
    for country in dataframe.country_long.unique():
        for i, (city, lat, lon, users) in enumerate(zip(
        dataframe.loc[dataframe.country_long==country,'locality_long'],
        dataframe.loc[dataframe.country_long==country,'latitude'],
        dataframe.loc[dataframe.country_long==country,'longitude'],
        dataframe.loc[dataframe.country_long==country,'{}'.format(var)])):
            folium.CircleMarker(
            [lat, lon],
            radius= 0.01*math.sqrt(users) if total_users else  0.05*(users) ,
            fill=True,
            fill_opacity=0.5,
            color='k',
            tooltip = city.title() + ' (' + '{}'.format(users) + ' Users)' if total_users else city.title() + ' (' + '{0:.2f}'.format(users) + ' Users per 1K people)' 
            ).add_to(map_city)
    return map_city

def top_countries(data,top_k_countries,gross_users = True,log_scale = False):
    '''
    Creates a plotly object for the total or relative number of twitter users by country
    Inputs:
        data (dataframe): dataframe grouped by country
        top_k_countries (int): top-k number of countries to plot
        gross_users(bool): If True, it plots the gross number of users; if False,
        it plots the relative (per 1,000 people) number of users
        log_scale(bool): if True, it plots a log scale for the total number of users; if
        False, it plots a linear scale
    Returns:
        Plotly object
    '''
    if log_scale:
        scale = "log"
        log_title = "-log scale-"
    else:
        scale = 'linear'
        log_title = ""
    if gross_users:
        data = data.sort_values("n_users",ascending=False)[:top_k_countries]
        x = data["country_long"]
        y = data["n_users"]
        fig = go.Figure([go.Bar(x = x, y = y, marker_color='rgb(55, 83, 109)', 
                        text = data["users_per_K"],
                       hovertemplate=
        "Number of users: %{y:,.0f}<br>" +
        "Users per 1K: %{text:.2f}<br>" +
        "<extra></extra>")])
        fig.update_layout(title = "Top {} Most Active Countries According to the Total Number of Users".format(top_k_countries),
                      #xaxis={'title':'Country'},
                      yaxis={'title':'Users (Millions {})'.format(log_title), 'type':'{}'.format(scale)},
                        plot_bgcolor="#f7fafd")
    else:
        data = data[data["country_long"]!="Antarctica"].sort_values("users_per_K", ascending=False)[:top_k_countries]
        x = data["country_long"]
        y = data["users_per_K"] 
        fig = go.Figure([go.Bar(x = x, y = y, marker_color='rgb(55, 83, 109)',
                        text = data["n_users"],
                       hovertemplate=
        "Users per 1K: %{y:.2f}<br>" +
        "Number of users: %{text:,.0f}<br>" +
        "<extra></extra>")])
        fig.update_layout(title = "Top {} Most Active Countries According to the Number of Users per 1,000 people".format(top_k_countries),
                      #xaxis={'title':'Country'},
                      yaxis={'title':'Users (per 1,000 people)', 'type':'{}'.format(scale)},
                         plot_bgcolor="#f7fafd")

    return fig

def top_cities(data,top_k_cities,gross_users = True,log_scale = False):
    '''
    Creates a plotly object for the total or relative number of twitter users by country
    Inputs:
        data (dataframe): dataframe grouped by country
        top_k_cities (int): top-k number of cities to plot
        gross_users(bool): If True, it plots the gross number of users; if False,
        it plots the relative (per 1,000 people) number of users
        log_scale(bool): if True, it plots a log scale for the total number of users; if
        False, it plots a linear scale
    Returns:
        Plotly object
    '''
    if log_scale:
        scale = "log"
        log_title = "-log scale-"
    else:
        scale = 'linear'
        log_title = ""
    
    if gross_users:
        data = data.sort_values("n_users",ascending=False)[:top_k_cities]
        x = data["locality_long"]
        y = data["n_users"]
        fig = go.Figure([go.Bar(x = x, y = y, marker_color='#E68848', 
                        text = data["population"],
                       hovertemplate=
        "Number of users: %{y:,.0f}<br>" +
        "Population: %{text:.2f}<br>" +
        "<extra></extra>")])
        fig.update_layout(title = "Top {} Most Active Cities According to the Total Number of Users".format(top_k_cities),
                      #xaxis={'title':'Country'},
                      yaxis={'title':'Users (Millions {})'.format(log_title), 'type':'{}'.format(scale)},
                        plot_bgcolor="#f7fafd")
    else:
        data = data[data["country_long"]!="Antarctica"].sort_values("users_per_K", ascending=False)[:top_k_cities]
        x = data["locality_long"]
        y = data["users_per_K"] 
        fig = go.Figure([go.Bar(x = x, y = y, marker_color='#E68848',
                        text = data["population"],
                       hovertemplate=
        "Users per 1K: %{y:.2f}<br>" +
        "Population: %{text:,.0f}<br>" +
        "<extra></extra>")])
        fig.update_layout(title = "Top {} Most Active Cities According to the Number of Users per 1,000 people".format(top_k_cities),
                      #xaxis={'title':'Country'},
                      yaxis={'title':'Users (per 1,000 people)', 'type':'{}'.format(scale)},
                         plot_bgcolor="#f7fafd")

    return fig