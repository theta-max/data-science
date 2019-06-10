import numpy as np
import pandas as pd
import networkx as nx
import random

def SIR(G, i_rate=0.5, r_rate=1, init=1, max_time=20):
    """Simulate an SIR epidemic on a network.
    
    Arguments:
    G -- A NetworkX graph object
    
    Keyword arguments:
    i_rate -- the constant per-edge rate of infection (default 0.5)
    r_rate -- the constant recovery rate of infected nodes (default 1)
    init -- the initial number of infections (default 1)
    max_time -- belt & braces variable to ensure loop terminates (default 20)
    """
    # initialise network and event queue
    queue = []
    nx.set_node_attributes(G, "S", "status")
    init_infecteds = random.sample(list(G.nodes()), init)
    for node in init_infecteds:
        G.nodes[node]["status"] = "I"
        r_time = np.random.exponential(r_rate)
        queue.append({"time": r_time,
                      "node": node,
                      "type": "R"})
        for neighbor in G.neighbors(node):
            i_time = np.random.exponential(i_rate)
            if i_time < r_time:
                queue.append({"time": i_time,
                      "node": neighbor,
                      "type": "I"})
    queue.sort(key=lambda k: k["time"], reverse=True)
    s_count = nx.number_of_nodes(G) - init
    i_count = init
    r_count = 0
    output = [{"time": 0,
               "S": s_count,
               "I": i_count,
               "R": r_count}]
    
    # Main loop
    while queue and queue[-1]["time"] < max_time:
        # unpack the event variables from the queued event
        time, node, event_type = (queue[-1]["time"],
                                  queue[-1]["node"],
                                  queue[-1]["type"])
        # if it's a revovery event and the node is infected, the node recovers
        if event_type == "R" and G.nodes[node]["status"] == "I":
            G.nodes[node]["status"] = event_type
            i_count -= 1
            r_count += 1
            output.append({"time": time,
                           "S": s_count,
                           "I": i_count,
                           "R": r_count})
        # if it's an infection event and the node is susceptible, infect!
        if event_type == "I" and G.nodes[node]["status"] == "S":
            G.nodes[node]["status"] = event_type
            # create a recovery event and queue it
            r_time = np.random.exponential(r_rate)
            queue.append({"time": r_time + time,
                          "node": node,
                          "type": "R"})
            s_count -= 1
            i_count += 1
            output.append({"time": time,
                           "S": s_count,
                           "I": i_count,
                           "R": r_count})
            # then create infection events for neighbors
            for neighbor in G.neighbors(node):
                i_time = np.random.exponential(i_rate)
                if i_time < r_time:
                    queue.append({"time": i_time + time,
                                  "node": neighbor,
                                  "type": "I"})
        # sort the queue by time and pop the event we've just processed
        queue.sort(key=lambda k: k["time"], reverse=True)
        queue.remove(queue[-1])
    # convert output to a DataFrame and rename the columns
    df = pd.DataFrame(output)
    df.rename(columns={"S": "Susceptible", "I": "Infected", "R": "Recovered"},
              inplace=True)
    return df

def timeshift(df, threshold, criterion="Infected", time="time"):
    """Add a series of adjusted times, zeroed on a threshold number
    of infections.
    
    Arguments:
    df -- A Pandas dataframe in the format output by the SIR function
    threshold -- an integer number of infections to be set to time zero
    
    Keyword arguments:
    criterion -- the column in df containing the critrion to which the
    threshold applies (default "Infected")
    time -- the column in df containing the time variable to adjust (default
    "time")
    """
    timeshift = df[df[criterion] >= threshold][time].min()
    df["time_adj"] = df[time] - timeshift
    return df
