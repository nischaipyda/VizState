from transitions.extensions.states import Timeout, Tags, add_state_features
from transitions.extensions.diagrams import GraphMachine
import io
from IPython.display import Image, display

FILE_NAME = "my_state_diagram.png"
FILE_TYPE = ".png"


@add_state_features(Timeout, Tags)
class CustomMachine(GraphMachine):
    pass


class Model:
    def show_graph(self, **kwargs):
        stream = io.BytesIO()
        self.get_graph(**kwargs).draw(stream, prog='dot', format='png')
        display(Image(stream.getvalue()))

    def cache_data(self, event):
        pass

    def mutate_data(self, event):
        pass

    def write_to_file(self, event):
        pass


model = Model()

states = [
    {'name': 'INIT'},
    {'name': 'VERSUS_BUILD', 'on_enter': model.cache_data},
    {'name': 'SERIES_BUILD', 'on_enter': model.cache_data},
    {'name': 'SERIES_MUTATE', 'on_enter': model.mutate_data},
    {'name': 'TOURNAMENT_BUILD', 'on_enter': model.cache_data},
    {'name': 'TOURNAMENT_MUTATE', 'on_enter': model.mutate_data},
    {'name': 'GROUP_BUILD', 'on_enter': model.cache_data},
    {'name': 'GROUP_MUTATE', 'on_enter': model.mutate_data},
    {'name': 'TOSS_BUILD', 'on_enter': model.cache_data},
    {'name': 'OUTCOME_BUILD', 'on_enter': model.cache_data},
    {'name': 'VENUE_BUILD', 'on_enter': model.cache_data},
    {'name': 'FIXTURE_BUILD', 'on_enter': model.cache_data},
    {'name': 'FIXTURE_MUTATE', 'on_enter': model.mutate_data},
    {'name': 'INNINGS_BUILD', 'on_enter': model.cache_data},
    {'name': 'FIXTURE_OFFICIALS_BUILD', 'on_enter': model.cache_data},
    {'name': 'PLAYING_XI_BUILD', 'on_enter': model.cache_data},
    {'name': 'DELIVERY_BUILD', 'on_enter': model.cache_data},
    {'name': 'DELIVERY_MUTATE', 'on_enter': model.mutate_data},
    {'name': 'TERMINATE', 'on_enter': model.write_to_file}
]

transitions = [
    {'trigger': 'versus_create', 'source': 'INIT', 'dest': 'VERSUS_BUILD'},
    {'trigger': 'series_create', 'source': 'VERSUS_BUILD', 'dest': 'SERIES_BUILD'},
    {'trigger': 'series_save', 'source': 'SERIES_BUILD',
        'dest': 'SERIES_MUTATE', 'unless': 'is_exists'},
    {'trigger': 'tournament_create', 'source': [
        'SERIES_MUTATE', 'SERIES_BUILD'], 'dest': 'TOURNAMENT_BUILD'},
    {'trigger': 'tournament_save', 'source': 'TOURNAMENT_BUILD', 'dest': 'TOURNAMENT_MUTATE',
     'unless': 'is_exists'},
    {'trigger': 'group_create', 'source': [
        'TOURNAMENT_BUILD', 'TOURNAMENT_MUTATE'], 'dest': 'GROUP_BUILD'},
    {'trigger': 'group_save', 'source': 'GROUP_BUILD',
        'dest': 'GROUP_MUTATE', 'unless': 'is_exists'},
    {'trigger': 'toss_create', 'source': [
        'GROUP_BUILD', 'GROUP_MUTATE'], 'dest': 'TOSS_BUILD'},
    {'trigger': 'outcome_create', 'source': 'TOSS_BUILD', 'dest': 'OUTCOME_BUILD'},
    {'trigger': 'venue_create', 'source': 'OUTCOME_BUILD', 'dest': 'VENUE_BUILD'},
    {'trigger': 'innings_create', 'source': 'VENUE_BUILD', 'dest': 'INNINGS_BUILD'},
    {'trigger': 'fixture_officials_create',
        'source': 'INNINGS_BUILD', 'dest': 'FIXTURE_OFFICIALS_BUILD'},
    {'trigger': 'playing_xi_create',
        'source': 'FIXTURE_OFFICIALS_BUILD', 'dest': 'PLAYING_XI_BUILD'},
    {'trigger': 'fixture_create', 'source': 'PLAYING_XI_BUILD', 'dest': 'FIXTURE_BUILD'},
    {'trigger': 'fixture_save', 'source': 'FIXTURE_BUILD',
        'dest': 'FIXTURE_MUTATE', 'unless': 'is_exists'},
    {'trigger': 'delivery_create', 'source': [
        'FIXTURE_MUTATE', 'FIXTURE_BUILD'], 'dest': 'DELIVERY_BUILD'},
    {'trigger': 'delivery_save', 'source': 'DELIVERY_BUILD', 'dest': 'DELIVERY_MUTATE'},
    {'trigger': 'stop', 'source': [
        'DELIVERY_BUILD', 'DELIVERY_MUTATE'], 'dest': 'TERMINATE'},
    {
        'trigger': 'internal_state_update',
        'source': ['SERIES_BUILD', 'TOURNAMENT_BUILD', 'GROUP_BUILD'],
        'dest': None,
        'after': 'update_data'
    },
]

machine = CustomMachine(model=model, states=states, transitions=transitions, initial='INIT', title='System State',
                        show_conditions=True, show_state_attributes=True)

print("Please wait... Generating state machine as {} file".format(FILE_TYPE))
model.get_graph().draw(FILE_NAME, prog='dot')
print("{} created".format(FILE_NAME))
