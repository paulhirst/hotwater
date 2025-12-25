from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from bokeh.layouts import row, column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, DatetimePicker

from orm import Temps

from config import dbname

engine = create_engine(dbname, echo=False)

datetimes = []
t0s = []
t1s = []
t2s = []
t3s = []
color = ['red', 'blue', 'green', 'black']

p = figure(title="Hotwater monitoring",
           x_axis_label='Date Time',
           x_axis_type='datetime',
           y_axis_label='Temperature',
           height=512,
           width=1024,
           )

# Add the scatter plot, with dummy data but configure the color mapper
xs = [datetimes, datetimes, datetimes, datetimes]
ys = [t0s, t1s, t2s, t3s]
cds = ColumnDataSource(data=dict(xs=xs, ys=ys, color=color))
l = p.multi_line(xs='xs', ys='ys', source=cds, line_color='color')

# Add the widgets
startdt_picker = DatetimePicker(title="Start")
enddt_picker = DatetimePicker(title="End")
button = Button(label="Plot")

def update_cds():
    global cds
    print ("Updating")

    datetimes = []
    t0s = []
    t1s = []
    t2s = []
    t3s = []

    with Session(engine) as session:
        stmt = select(Temps)
        for t in session.scalars(stmt):
            datetimes.append(t.datetime)
            t0s.append(t.temp0)
            t1s.append(t.temp1)
            t2s.append(t.temp2)
            t3s.append(t.temp3)

    xs = [datetimes, datetimes, datetimes, datetimes]
    ys = [t0s, t1s, t2s, t3s]
    cds.data = dict(xs=xs, ys=ys, color=color)
    #l.data_source = cds
    print(f"Updated cds with {len(datetimes)} values")


# Setup Callbacks
button.on_event('button_click', update_cds)

# Set up document
toprow = row(startdt_picker, enddt_picker, button)
col = column(toprow, p)

curdoc().add_root(col)
