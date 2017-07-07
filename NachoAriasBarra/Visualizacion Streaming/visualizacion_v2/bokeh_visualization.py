# -*- encoding: utf-8 -*-
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, Range1d, Button, Paragraph, TextInput
from bokeh.models import Select, Label, SingleIntervalTicker, LinearAxis
from bokeh.models.layouts import Column
from bokeh.io import curdoc
from bokeh.models.glyphs import VBar, Line
from bokeh.layouts import layout
import json
from random import uniform as uni
from ast import literal_eval
import ast
import time
from datetime import datetime as dt
import os
import sys
from time import sleep
import threading
path_to_append = os.path.dirname(os.path.abspath(__file__)).replace("/visualization", "")
sys.path.append(path_to_append)
from KafkaConnection.kafka_connection import KafkaConnection as KFK


sources = []
all_column_names = []
counter = 0.0
topic_name = "visualization200"

all_names = ["time", "EEUU_Unem", "Spain_Unem", "Japan_Unem", "UK_Unem",
             "EEUU_DJI", "UK_LSE", "Spain_IBEX35", "Japan_N225"]

unem_options = ["EEUU_Unem", "Spain_Unem", "UK_Unem", "Japan_Unem"]
unem_values = ["EEUU_Unem", "Spain_Unem"]

filename = "final_data.csv"

vel_options = ["Slow", "Normal", "Fast"]

source_unem = None

last_date = dt(1999,12,1)
date_stop = dt(2016,11,1)

update_time = 200
sleep_time = 0.0

velocity_options = {"Slow":5.0, "Normal":2.5, "Fast":0.25}

try:

    # Kafka config
    kafka_ip = 'localhost'
    kafka_port = 9092

    # kafkastockExchange = KFK(host=kafka_ip, port=kafka_port, topic='stockExchange')
    # message_stock = kafkastockExchange.init_Kafka_consumer()

    # kafka_unemployment = KFK(host=kafka_ip, port=kafka_port, topic='unemployment')
    # consumer_unem = kafka_unemployment.init_Kafka_consumer()

    kafka_connection = KFK(host=kafka_ip, port=kafka_port, topic=topic_name)
    consumer = kafka_connection.init_Kafka_consumer()

except:
    pass


def source_bokeh_kafka(column_names):
    data_dict = {name: [] for name in column_names}
    source = ColumnDataSource(data_dict)
    return source

def multi_plot(figure_info, source):

    fig = Figure(plot_width=figure_info["plot_width"],
                 plot_height=figure_info["plot_height"],
                 title=figure_info["title"], x_axis_type = "datetime")

    fig.yaxis.axis_label = figure_info["yaxis_label"]

    my_y_label = figure_info["secondary_y_label"]

    fig.extra_y_ranges = {my_y_label: Range1d(start=0, end=figure_info["max_unemployment"])}
    fig.add_layout(LinearAxis(y_range_name=my_y_label,  axis_label=my_y_label), 'right')


    for idx in range(1, len(figure_info["names"])):
        legend_name = str(figure_info["legends"][idx-1]) + " "

        if "Unem" not in figure_info["names"][idx]:

            fig.vbar(source=source, x=figure_info["names"][0], top=figure_info["names"][idx],
                     bottom = 0, width = 1000000000, color = figure_info["colors"][idx-1], fill_alpha = 0.2,
                     line_alpha = 0.1, legend = legend_name)

        else:

           fig.line(source=source, x = figure_info["names"][0], y = figure_info["names"][idx],
                     line_width = figure_info["line_widths"][idx-1], alpha = figure_info["alphas"][idx-1],
                     color = figure_info["colors"][idx-1], legend = legend_name, y_range_name=my_y_label)

    fig.legend.location = figure_info["legend_location"]
    fig.xaxis.axis_label = figure_info["xaxis_label"]
    # fig.yaxis.axis_label = figure_info["yaxis_label"]
    fig.title.align = figure_info["title_align"]

    fig.logo = None
    fig.toolbar_location = None

    return fig


def multiline_plot(figure_info, source):

    fig = Figure(plot_width=figure_info["plot_width"],
                 plot_height=figure_info["plot_height"],
                 title=figure_info["title"], x_axis_type = "datetime")

    for idx in range(1, len(figure_info["names"])):
        legend_name = str(figure_info["legends"][idx-1]) + " "

        fig.line(source=source, x=figure_info["names"][0], y=figure_info["names"][idx],
                 line_width=figure_info["line_widths"][idx - 1], alpha=figure_info["alphas"][idx - 1],
                 color=figure_info["colors"][idx - 1], legend=legend_name)

    fig.legend.location = figure_info["legend_location"]
    fig.xaxis.axis_label = figure_info["xaxis_label"]
    fig.yaxis.axis_label = figure_info["yaxis_label"]
    fig.title.align = figure_info["title_align"]

    fig.logo = None
    fig.toolbar_location = None

    return fig


def update_data():

    global sources
    global all_column_names
    global counter
    global consumer
    global last_date
    global source_unem
    global update_time

    sleep(sleep_time)

    if last_date >= date_stop:

        pass

    else:


        try:
            # kafka
            # message_stock = consumer_stock.consume()
            # message_unem = consumer_unem.consume()

            message = consumer.consume()

            # if message_stock is not None and message_unem is not None:

            if message is not None:

                # kafka
                # value_stock = message_stock.value
                # value_unem = message_unem.value
                #
                # dict_message_stock = ast.literal_eval(value_stock)
                # dict_message_unem = ast.literal_eval(value_unem)

                value = message.value
                dict_message = ast.literal_eval(value)

                # dict_message = dict()
                # dict_message['Date'] = dict_message_stock['Date']
                # dict_message['EEUU_DJI'] = dict_message_stock['DJI']['Value']
                # dict_message['UK_LSE'] = dict_message_stock['LSE']['Value']
                # dict_message['Spain_IBEX35'] = dict_message_stock['IBEX35']['Value']
                # dict_message['Japan_N225'] = dict_message_stock['N225']['Value']
                # dict_message['EEUU_Unem'] = dict_message_unem['DJI']['Value']
                # dict_message['UK_Unem'] = dict_message_unem['LSE']['Value']
                # dict_message['Spain_Unem'] = dict_message_unem['IBEX35']['Value']
                # dict_message['Japan_Unem']  = dict_message_unem['N225']['Value']


                # for source, column_names in zip(sources, all_column_names):
                #     data_dict = {name: [dict_message[name]] for name in column_names if name != "time"}
                #
                #     print(dict_message["Date"])
                #
                #     year, month = dict_message["Date"].split("-")
                #     data_dict[column_names[0]] = [dt(int(year), int(month), 1)]
                #
                #     source.stream(data_dict, 1000)
                #
                #     last_date = dt(int(year), int(month), 1)


                for source, column_names in zip(sources, all_column_names):
                    data_dict = {name: [dict_message[name]] for name in column_names if name != "time"}

                    year, month = dict_message["Date"].split("-")

                    curr_date = dt(int(year), int(month), 1)

                    if curr_date > dt(2000, 1, 1):

                        data_dict[column_names[0]] = [curr_date]
                        print('Received new message ', dict_message["Date"])
                        source.stream(data_dict, 1000)
                        last_date = dt(int(year), int(month), 1)
        except:
            pass


def main():

    global sources
    global all_column_names
    global counter
    global consumer
    global all_names
    global unem_options
    global unem_values
    global source_unem
    global update_time
    global sleep_time
    global velocity_options


    def update_select_vel(attr, old, new):
        global sleep_time
        global velocity_options

        speed = select_vel.value

        print("Changing speed to ", speed, velocity_options[speed])

        sleep_time = velocity_options[speed]


    figure_info1 = {"names":["time", "EEUU_Unem", "EEUU_DJI"],
                   "x_name":"time", "line_widths":[2,2,2,2] ,
                    "alphas":[0.85, 0.85, 0.85, 0.85],
                    "colors":["blue", "red", "black", "orange"],
                    "legends":["Unem", "DJI"],
                    "y_range":[0, 30],
                    "plot_width":450, "plot_height":350,
                    "title":"EEUU", "legend_location":"top_left",
                    "xaxis_label":"Date", "yaxis_label":"Stock Market Index",
                    "title_align":"center",
                    "max_unemployment":15,
                    "secondary_y_label":"Unemployment"}


    figure_info2 = {"names":["time", "Spain_Unem", "Spain_IBEX35"],
                   "x_name":"time", "line_widths":[2,2,2,2] ,
                    "alphas":[0.85, 0.85, 0.85, 0.85],
                    "colors":["blue", "red", "black", "orange"],
                    "legends":["Unem", "IBEX35"],
                    "y_range":[0, 30],
                    "plot_width":450, "plot_height":350,
                    "title":"Spain", "legend_location":"top_left",
                    "xaxis_label":"Date", "yaxis_label":"Stock Market Index",
                    "title_align":"center",
                    "max_unemployment":30,
                    "secondary_y_label": "Unemployment"}


    figure_info3 = {"names":["time", "Japan_Unem", "Japan_N225"],
                   "x_name":"time", "line_widths":[2,2,2,2] ,
                    "alphas":[0.85, 0.85, 0.85, 0.85],
                    "colors":["blue", "red", "black", "orange"],
                    "legends":["Unem", "N255"],
                    "y_range":[0, 30],
                    "plot_width":450, "plot_height":350,
                    "title":"Japan", "legend_location":"top_left",
                    "xaxis_label":"Date", "yaxis_label":"Stock Market Index",
                    "title_align":"center",
                    "max_unemployment":8,
                    "secondary_y_label": "Unemployment"}


    figure_info4 = {"names":["time", "UK_Unem", "UK_LSE"],
                   "x_name":"time", "line_widths":[2,2,2,2] ,
                    "alphas":[0.85, 0.85, 0.85, 0.85],
                    "colors":["blue", "red", "black", "orange"],
                    "legends":["Unem", "LSE"],
                    "y_range":[0, 30],
                    "plot_width":450, "plot_height":350,
                    "title":"UK", "legend_location":"top_left",
                    "xaxis_label":"Date", "yaxis_label":"Stock Market Index",
                    "title_align":"center",
                    "max_unemployment":10,
                    "secondary_y_label": "Unemployment"}



    figure_info5 = {"names":["time", "EEUU_Unem", "Spain_Unem", "Japan_Unem", "UK_Unem"],
                   "x_name":"time", "line_widths":[2,2,2,2] ,
                    "alphas":[0.85, 0.85, 0.85, 0.85],
                    "colors":["blue", "red", "black", "orange"],
                    "legends":["EEUU_Unem", "Spain_Unem", "Japan_Unem", "UK_Unem"],
                    "y_range":[0, 30],
                    "plot_width":450, "plot_height":350,
                    "title":"Unemployment comparison", "legend_location":"top_left",
                    "xaxis_label":"Date", "yaxis_label":"Unemployment",
                    "title_align":"center"}


    figure_info6 = {"names":["time", "EEUU_DJI", "Spain_IBEX35", "Japan_N225", "UK_LSE"],
                   "x_name":"time", "line_widths":[2,2,2,2] ,
                    "alphas":[0.85, 0.85, 0.85, 0.85],
                    "colors":["blue", "red", "black", "orange"],
                    "legends":["EEUU_DJI", "Spain_IBEX35", "Japan_N225", "UK_LSE"],
                    "y_range":[0, 30],
                    "plot_width":450, "plot_height":350,
                    "title":"Stock exchange comparison", "legend_location":"top_left",
                    "xaxis_label":"Date", "yaxis_label":"Stock Market Index",
                    "title_align":"center"}

    source_all = source_bokeh_kafka(all_names)
    dict_unem = {"time":source_all.data["time"],
                 unem_values[0]: source_all.data[unem_values[0]],
                 unem_values[0]: source_all.data[unem_values[0]]}

    source_unem = ColumnDataSource(dict_unem)

    fig1 = multi_plot(figure_info1 ,source_all)
    fig2 = multi_plot(figure_info2, source_all)
    fig3 = multi_plot(figure_info3, source_all)
    fig4 = multi_plot(figure_info4, source_all)
    fig5 = multiline_plot(figure_info5, source_all)
    fig6 = multiline_plot(figure_info6, source_all)

    select_vel = Select(value='Slow', options=vel_options)
    select_vel.on_change('value', update_select_vel)


    def update_buttom_increase():
        global sleep_time
        sleep_time -= 0.15
        print("increasing velocity")


    def update_buttom_decrease():
        global sleep_time
        sleep_time += 0.15
        print("increasing velocity")


    buttom_increase = Button(label="Increase velocity")
    buttom_increase.on_click(update_buttom_increase)

    buttom_decrease = Button(label="Decrease velocity")
    buttom_decrease.on_click(update_buttom_decrease)


    sources.append(source_all)
    all_column_names.append(all_names)

    curdoc().add_periodic_callback(update_data, update_time)

    curdoc().add_root(layout([[fig1, fig2, fig5],
                              [fig3, fig4, fig6]]))


main()
