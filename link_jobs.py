import logging
import time
from taipy.gui import Gui, navigate
import taipy.gui.builder as tgb
import pandas as pd

logging.basicConfig(level=logging.INFO)

df = pd.read_csv("data/cleaned/indeed/2024_03_15.csv")

links = [("", "", "", "")]
chunk_index = 0


def get_chunks(df, chunk_size=25):
    '''
    Generator function to get a chunk of the dataframe at a time.'''
    n_chunks = len(df) // chunk_size + 1
    for i in range(n_chunks):
        yield df.iloc[i * chunk_size : (i + 1) * chunk_size]


def navigate_to_link(state, id, payload=None):
    """
    Redirects to the link provided in the item(row) based on its id."""
    link_url = id
    navigate(state, to=link_url, force=True)


def refresh_links(state):
    """
    Refreshes the items shown on the page after updates are made."""
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
    """
    Adds more items to the state's link variable."""
    global chunk_index
    chunks = list(get_chunks(df))
    state.links = []
    if chunk_index < len(chunks):
        chunk = chunks[chunk_index]
        if not chunk.empty:
            logging.info(f"processing chunk {chunk_index}")
            logging.info(chunk.index[0])
            state.links = [
                (row["title"], row["company"], row["location"], row["link"])
                for _, row in chunk.iterrows()
            ]
            refresh_links(state)
        chunk_index += 1


with tgb.Page() as main_page:
    tgb.button("Add links", on_action=simulate_adding_more_links)
    tgb.part(partial="{link_partial}")


def on_init(state):
    """
    Triggered upon opening the client."""
    simulate_adding_more_links(state)
    refresh_links(state)


gui = Gui(main_page)
link_partial = gui.add_partial("")  # Initialization of the partial
gui.run(debug=True, use_reloader=True)
