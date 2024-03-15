import logging
import time
from taipy.gui import Gui, navigate
import taipy.gui.builder as tgb
import pandas as pd

logging.basicConfig(level=logging.INFO)

df = pd.read_csv("data/cleaned/indeed/2024_03_15.csv")

links = [
    (
        '',
        '',
        '',
        ''
    )
]


def get_chunks(df, chunk_size=25):
    n_chunks = len(df) // chunk_size+1
    for i in range(n_chunks):
        yield df.iloc[i * chunk_size : (i + 1) * chunk_size]


for chunk in get_chunks(df, 25):
    links = [(row["title"], row["link"]) for index, row in chunk.iterrows()]
    # Now you can use the links list


def navigate_to_link(state, id, payload=None):
    # The correct url is passed through the id
    link_url = id
    navigate(state, to=link_url, force=True)


def refresh_links(state):
    with tgb.Page() as link_part:
        with tgb.layout("1"):
            for link in state.links:
                if len(link) == 4:
                    job_title, company, location, link_url = link
                    with tgb.part("card"):  # Just to make i into a card (not necessary)
                        tgb.text(job_title, class_name="h2")
                        with tgb.layout("1 1"):
                            tgb.text(company, class_name="h4")
                            tgb.text(location)
                        tgb.button(
                            "apply",
                            on_action=navigate_to_link,
                            id=link_url,
                            class_name="plain",
                        )
    state.link_partial.update_content(state, link_part)


def simulate_adding_more_links(state):
    state.links =[]
    for i,chunk in enumerate(get_chunks(df, 25)):
        logging.info(f'processing chunk {i}')
        logging.info(chunk.index[0])
        state.links += [
            (row["title"], row["company"], row["location"], row["link"])
            for _, row in chunk.iterrows()
        ]
        refresh_links(state)
        time.sleep(0.1)


with tgb.Page() as main_page:
    tgb.button("Add links", on_action=simulate_adding_more_links)
    tgb.part(partial="{link_partial}")


def on_init(state):
    # When you open the client, this function is triggered
    # and initialize the links
    simulate_adding_more_links(state)
    refresh_links(state)


gui = Gui(main_page)
link_partial = gui.add_partial("")  # Initialization of the partial
gui.run(debug=True, use_reloader=True)
