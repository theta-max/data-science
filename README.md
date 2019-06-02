# data-science #

This repository contains examples of work in data science and analytics.

## Stochastic processes on networks ##
<details>
<summary>The [Epidemics](Epidemics) directory contains a Python implementation of an SIR infection model, which simulates the spread of an infectious disease through a networked population. The file contains two functions. The model simulates infection as a per-edge Poisson point process and uses the event-queue method.

</summary>

The **SIR function** takes arg *G* (a networkx graph object) and kwargs *beta* (per-edge infection rate), *gamma* (recovery rate), *init* (number of initial infections), and *max_time* (maximum time to run the simulation; since SIR models should always reach equilibrium infinite loops should not occur, but this kwarg is included on a belt-and-braces basis).

The **timeshift function** is an auxiliary function which aligns multiple model runs with time = 0 at the specified threshold level of infections. It takes two args and two kwargs. The positional arguments are: *df* (a Pandas dataframe containing model output), and *threshold* (the number of infections to set at time = 0). The two keyword arguments can be ignored if using output from the SIR function. They specify the criterion to which the threshold value relates (*criteria*), and the dataframe column containing the time values (*time*).

Together, these functions allow multiple model runs to be collated and aligned. It is straightforward to then, for example, plot the results:

![Plot of 50 SIR model runs](Epidemics/50_runs.png  "Plot of 50 SIR model runs")
 
</details>
