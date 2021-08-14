"""

Dev serve command on Windows
`python -m bokeh serve --dev --show zviewer`
"""

#region IMPORTS
import os.path
import sys

import bokeh.io as io
import bokeh.layouts as layouts
import bokeh.models as models
import bokeh.plotting as plotting

app_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, app_path)

import zebra.path
import zebra.data
#endregion

#region SETTINGS
# Line colors for robots in positions blue 1-3 and red 1-3 respectively.
PATH_COLORS = ['darkblue', 'royalblue', 'deepskyblue',
               'darkred', 'crimson', 'lightcoral']
#endregion

#region READ DATA FILES
# Robot path data
data_path = os.path.abspath(os.path.join(app_path, 'data', '2020wasno.jsonl'))
zcomp = zebra.path.Competitions(data_path)

# Season-specific field data
field_path = os.path.abspath(os.path.join(app_path, 'data', 'field2020.json'))
field = zebra.data.read_field(field_path)
#endregion

#region PLOTTING CONTROLS
event_selector = models.Select(
    title='Select Competition',
    options=zcomp.events,
    value=zcomp.events[0]
)
curr_event_matches = zcomp.matches(event_selector.value)
match_selector = models.Select(
    title='Select Match',
    options=curr_event_matches,
    value=curr_event_matches[0]
)
match_select_row = models.layouts.Row(event_selector, match_selector)

time_range_selector = models.RangeSlider(start=0, end=160, step=1, value=(0, 160),
                                   title='Select Time Range in Seconds')

time_span_selector = models.Slider(start=0, end=160, step=1, value=10,
                                   title='Select Time Span End')

time_select_type = models.CheckboxButtonGroup(
    labels=['All', 'Span', 'Range'],
    active=[2],
)
def update_time_select(attr, old, new):
    """Ensure only one option can be selected at a time."""
    if len(new) == 0:
        time_select_type.active = old
    if len(new) - len(old) == 1:
        time_select_type.active = list(set(new) - set(old))

    time_range_selector.visible = (time_select_type.active[0] == 2)


time_select_type.on_change('active', update_time_select)

time_select_row = models.layouts.Row(time_select_type, time_range_selector)


#endregion

#region OBTAIN PLOTTING DATA
data_sources = [
    {'position': None,
    'team': None,
    'path': models.ColumnDataSource(data={'x': [], 'y': []}),
    'path_len': None,
    'color': PATH_COLORS[idx]
    }
    for idx in range(6)]

def update_datasources(start_time, end_time):
    global data_sources
    zmatch = zcomp[match_selector.value]
    teams = zmatch.blue + zmatch.red
    positions = ['blue1', 'blue2', 'blue3', 'red1', 'red2', 'red3']
    start = start_time * 10
    end = end_time * 10
    print(start, end)
    for idx in range(6):
        data_sources[idx]['position'] = positions[idx]
        data_sources[idx]['team'] = teams[idx]
        data_sources[idx]['path'].data = {'x': zmatch.paths[2*idx][start:end],
                                          'y': zmatch.paths[2*idx+1][start:end]}
        data_sources[idx]['path_len'] = zmatch.paths.shape[1]

update_datasources(0, 160)
#endregion

#region PLOT ROBOT PATHS
def add_field(figure, field):
    for line in field['lines']:
        color = field['colors'][line['class']]
        figure.line(line['x'], line['y'], line_color=color)

def add_path(figure, data):
    figure.line(x='x', y='y', source=data['path'],
                line_color=data['color'], legend_label=data['team'])


def plot_match(field, height=350):    
    fig = plotting.figure(title=match_selector.value, match_aspect=True,
                          plot_height=height, plot_width=height*2,
                          x_range=(-2, 58))
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    add_field(fig, field)
    
    for ds in data_sources:
        add_path(fig, ds)

    fig.legend.click_policy = 'hide'

    return fig


fig = plot_match(field, 600)
#endregion

#region MAKE PAGE UPDATEABLE
def update():
    global data_sources, fig
    start_time = 0
    end_time = 160
    curr_event_matches = zcomp.matches(event_selector.value)
    event_selector.options = curr_event_matches
    if time_select_type.active[0] == 1:
        end_time = time_span_selector.value
        start_time = max(0, end_time - 10)
    elif time_select_type.active[0] == 2:
        start_time = time_range_selector.value[0]
        end_time = time_range_selector.value[1]

    update_datasources(start_time, end_time)


    fig.title.text = match_selector.value

match_selector.on_change('value', lambda attr, old, new: update())
time_range_selector.on_change('value', lambda attr, old, new: update())
#endregion

#region LAYOUT PAGE
title_div = models.Div(text='<h1>FRC Match</h1>')
plot_layout = layouts.column(title_div, fig, match_select_row, time_select_row, 
                             models.Div(text='<br/>'))
page_layout = layouts.Row(models.Div(text='<p></p>'), plot_layout)

io.curdoc().add_root(page_layout)
io.curdoc().title = 'FRC Zebra Path Viewer'
#endregion