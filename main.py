from taipy import Gui
from taipy.gui import builder as tgb
from pages.home import home_page 
from pages.jobs import link_part as data_page
from pages import jobs
from pages.analysis import analysis_page

with tgb.Page() as root_page:
    tgb.navbar()

pages = {"/": root_page,
         'home':home_page,
         "data": data_page,
         "analysis":analysis_page}

def on_init(state):
    jobs.init_selector_vars(state)
    jobs.simulate_adding_more_links(state)
    jobs.filter_data(state)

if __name__ =='__main__':
    Gui(pages=pages).run(debug=False)