import pandas as pd
import networkx as nx

df = pd.read_csv("Data/waiting_list.csv")
df.sort_values("Datetime", inplace=True)

G = nx.from_pandas_edgelist(df, "From", "To", edge_attr=True,
                            create_using=nx.MultiDiGraph)
students = df.shape[0]

# Returns candidate swapchains
swaps, chain_no = [], 1
for cycle in list(nx.simple_cycles(G)):
    n = len(cycle)
    step = 1
    for u, v in zip(cycle, cycle[1:] + [cycle[0]]):
        for i in range(students):
            if df.iloc[i,1] == u and df.iloc[i,2] == v:
                swaps.append({"chain_no": chain_no, 
                                "chain_size": n,
                                "Step": step,
                                "Student": df.iloc[i,0],
                                "From": u,
                                "To": v})
                step +=1
                break
    chain_no += 1

# Sort and filter output csv
output = pd.DataFrame(swaps)
output.sort_values(["chain_size", "chain_no", "Step"],
                            ascending=[False, True, True],
                            inplace=True)
output.set_index("Step", inplace=True)
cols = ["chain_no", "chain_size", "Student", "From", "To"]
output = output[cols]
output.to_csv(path_or_buf="Data/swapchain.csv")

