from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from bokeh.layouts import row, column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, DatePicker, TimePicker

import datetime

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
color = ['red', 'purple', 'orange', 'blue', 'orange']
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
start_datetime = None
end_datetime = None
startdate_picker = DatePicker(title="Start Date")
enddate_picker = DatePicker(title="End Date")
plot_button = Button(label="Plot")
today_button = Button(label="Today")

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
        if start_datetime is not None:
            stmt = stmt.where(Temps.datetime >= start_datetime)
        if end_datetime is not None:
            stmt = stmt.where(Temps.datetime <= end_datetime)
        for t in session.scalars(stmt):
            datetimes.append(t.datetime)
            t0s.append(t.temp0)
            t1s.append(t.temp1)
            t2s.append(t.temp2)
            t3s.append(t.temp3)
            linkdeltas.append((t.temp2 - t.temp3) if t.pump else None)
            pumps.append(100.0 * t.pump)
            timers.append(100.0 * t.timer)
            heaters.append(100.0 * t.heater)

    xs = [datetimes, datetimes, datetimes, datetimes, datetimes]
    ys = [t0s, t1s, t2s, t3s,  linkdeltas]
    cds.data = dict(xs=xs, ys=ys, color=color, labels=labels)
    bcds.data = dict(x=datetimes, timers=timers, pumps=pumps, heaters=heaters)
    print(f"Updated cds with {len(datetimes)} values")

def today():
    global start_datetime, end_datetime

    today_date = datetime.date.today()
    startdate_picker.value = today_date.isoformat()
    enddate_picker.value = today_date.isoformat()

    start_time = datetime.time(hour=5, minute=0, second=0)
    end_time = datetime.time(hour=21, minute=0, second=0)
    start_datetime = datetime.datetime.combine(today_date, start_time)
    end_datetime = datetime.datetime.combine(today_date, end_time)

    update_cds()

def plot():
    global start_datetime, end_datetime

    sd = datetime.date.fromisoformat(startdate_picker.value)
    ed = datetime.date.fromisoformat(enddate_picker.value)

    print(f"{type(sd)} {sd}")

    day = datetime.timedelta(days=1)
    ed += day
    zh = datetime.time(hour=0, minute=0, second=0)
    start_datetime = datetime.datetime.combine(sd, zh)
    end_datetime = datetime.datetime.combine(ed, zh)

    update_cds()


# Setup Callbacks
plot_button.on_event('button_click', plot)
today_button.on_event('button_click', today)

# Set up document
toprow = row(startdate_picker, enddate_picker, plot_button, today_button)
col = column(toprow, p)

curdoc().add_root(col)
