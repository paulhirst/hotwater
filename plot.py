from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from bokeh.layouts import row, column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, DatetimePicker, Band

from orm import Temps

from config import dbname

engine = create_engine(dbname, echo=False)

datetimes = []
t0s = []
t1s = []
t2s = []
t3s = []
linkdeltas = []
pumps = []
timers = []
heaters = []
color = ['red', 'purple', 'orange', 'blue', 'yellow']
labels = ['TankTop', 'Mixer', 'Downlink', 'Uplink', 'LinkDelta']

p = figure(title="Hotwater monitoring",
           x_axis_label='Date Time',
           x_axis_type='datetime',
           y_axis_label='Temperature',
           height=512,
           width=1024,
           )

# Add the scatter plot, with dummy data but configure the color mapper
xs = [datetimes, datetimes, datetimes, datetimes, datetimes]
ys = [t0s, t1s, t2s, t3s, linkdeltas]
cds = ColumnDataSource(data=dict(xs=xs, ys=ys, color=color, labels=labels))
bcds = ColumnDataSource(data=dict(x=datetimes, timers=timers, pumps=pumps, heaters=heaters))
l = p.multi_line(xs='xs', ys='ys', source=cds, line_color='color', legend_field='labels')
tva = p.varea(x='x', y1=0, y2='timers', alpha=0.4, fill_color='cyan', source=bcds)
hva = p.varea(x='x', y1=0, y2='heaters', alpha=0.4, fill_color='red', source=bcds)
pva = p.varea(x='x', y1=0, y2='pumps', alpha=0.4, fill_color='yellow', source=bcds)

# Add the widgets
startdt_picker = DatetimePicker(title="Start")
enddt_picker = DatetimePicker(title="End")
button = Button(label="Plot")

def update_cds():
    global cds
    global bcds
    print ("Updating")

    datetimes = []
    t0s = []
    t1s = []
    t2s = []
    t3s = []
    linkdeltas = []
    pumps = []
    timers = []
    heaters = []

    with Session(engine) as session:
        stmt = select(Temps)
        for t in session.scalars(stmt):
            datetimes.append(t.datetime)
            t0s.append(t.temp0)
            t1s.append(t.temp1)
            t2s.append(t.temp2)
            t3s.append(t.temp3)
            linkdeltas.append(t.temp2 - t.temp3)
            pumps.append(100.0 * t.pump)
            timers.append(100.0 * t.timer)
            heaters.append(100.0 * t.heater)

    xs = [datetimes, datetimes, datetimes, datetimes, datetimes]
    ys = [t0s, t1s, t2s, t3s,  linkdeltas]
    cds.data = dict(xs=xs, ys=ys, color=color, labels=labels)
    bcds.data = dict(x=datetimes, timers=timers, pumps=pumps, heaters=heaters)
    print(f"Updated cds with {len(datetimes)} values")


# Setup Callbacks
button.on_event('button_click', update_cds)

# Set up document
toprow = row(startdt_picker, enddt_picker, button)
col = column(toprow, p)

curdoc().add_root(col)
