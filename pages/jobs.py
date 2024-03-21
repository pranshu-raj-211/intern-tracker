import logging
from taipy.gui import Gui, navigate, notify
import taipy.gui.builder as tgb
import pandas as pd
from datetime import datetime


current_date = datetime.now().strftime("%Y_%m_%d")

logging.basicConfig(
    filename=f"logs/job_log_{current_date}.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

df = pd.read_csv("data/aggregate/aggregate.csv")

filtered_df = df
selected_locations = list(df["location"].unique())
selected_queries = [
    "python developer",
    "data analyst",
    "machine learning engineer",
    "software engineer",
    "backend developer",
    "devops engineer",
    "automation engineer",
    "network engineer",
    "vuejs developer",
    "react developer",
    "nodejs developer",
    "frontend developer",
    "full stack developer",
    "ui developer",
    "web application developer",
    "javascript engineer",
    "mobile app developer",
    "other",
]
selected_sources = ["indeed", "yc"]
links = {}
chunk_index = 0


def init_selector_vars(state):
    state.selected_sources = "indeed"
    state.selected_queries = "python developer"
    state.selected_locations = "remote"


def get_chunks(df, chunk_size=20):
    n_chunks = len(df) // chunk_size + 1
    for i in range(n_chunks):
        yield df.iloc[i * chunk_size : (i + 1) * chunk_size]


chunks = list(get_chunks(filtered_df))


def filter_data(state):
    print(state.selected_locations, state.selected_sources, state.selected_queries)
    state.filtered_df = df[
        df["location"].isin([state.selected_locations])
        & df["source"].isin([state.selected_sources])
        & df["query"].isin([state.selected_queries])
    ]
    state.chunk_index = 0
    if state.filtered_df.empty:
        logging.warning("No filtered rows available")
        notify(
            state=state,
            message="No jobs found for the given filters",
            notification_type="e",
            system_notification=True,
        )
        # init_selector_vars(state=state)

    simulate_adding_more_links(state)


def navigate_to_link(state, link_url, payload=None):
    navigate(state, to=link_url, force=True)


# todo : On interacting with selector, it refreshes chunk without actually filtering, fix this


def simulate_adding_more_links(state):
    state.chunks = list(get_chunks(state.filtered_df))
    if state.chunk_index < len(state.chunks):
        chunk = state.chunks[state.chunk_index]
        if not chunk.empty:
            logging.info(f"processing chunk {state.chunk_index}")
            logging.info(chunk.index[0])
            chunk.reset_index(drop=True, inplace=True)
            state.links = {"link_" + str(i): row for i, row in chunk.iterrows()}
        state.chunk_index += 1


def is_card_rendered(links, nb_link):
    return "link_" + str(nb_link) in list(links)


def get_title(links, i):
    return links["link_" + str(i)]["title"] if is_card_rendered(links, i) else ""


def get_company(links, i):
    return links["link_" + str(i)]["company"] if is_card_rendered(links, i) else ""


def get_location(links, i):
    return links["link_" + str(i)]["location"] if is_card_rendered(links, i) else ""


def get_link(links, i):
    return links["link_" + str(i)]["link"] if is_card_rendered(links, i) else ""


def card_link(i):
    with tgb.part(
        "card", render="{is_card_rendered(links, " + str(i) + ")}"
    ) as card_part:
        tgb.text("{get_title(links, " + str(i) + ")}", class_name="h3")
        tgb.html("br")
        with tgb.layout("1 1"):
            tgb.text("{get_company(links, " + str(i) + ")}", class_name="h5")
            tgb.text("{get_location(links, " + str(i) + ")}", class_name="h5")
        tgb.button(
            "Apply",
            on_action=navigate_to_link,
            id="{get_link(links, " + str(i) + ")}",
            class_name="plain",
        )
    return card_part


with tgb.Page() as link_part:
    tgb.text("Find Jobs", class_name="h2")
    tgb.html("br")
    with tgb.layout("4 1 1"):
        tgb.selector(
            value="{selected_queries}",
            lov=selected_queries,
            on_change=filter_data,
            dropdown=True,
            multiple=False,
            class_name="fullwidth",
        )
        tgb.selector(
            value="{selected_locations}",
            lov=selected_locations,
            on_change=filter_data,
            dropdown=True,
            multiple=False,
            class_name="fullwidth",
        )
        tgb.selector(
            value="{selected_sources}",
            lov=selected_sources,
            on_change=filter_data,
            dropdown=True,
            multiple=False,
            class_name="fullwidth",
        )
    with tgb.layout("1 1 1 1"):
        for i in range(20):
            card_link(i)
    tgb.button("See more jobs", on_action=simulate_adding_more_links)


def on_init(state):
    init_selector_vars(state)
    simulate_adding_more_links(state)


# * do not use the following line if running the multi page app, it is only for debugging
Gui(link_part).run(debug=True, use_reloader=True)
