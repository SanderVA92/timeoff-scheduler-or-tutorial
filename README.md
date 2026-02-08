# Operations Research problem-solving case

This repository accompanies a workshop on Operations Research problem solving using an exact optimization model formulation.

During the workshop we covered subsequent steps of problem refinement, (initial) model formulation, followed by the actual implementation in Jupyter notebooks. Within the notebooks, `PuLP` is used as wrapper to define the model and solve it with CBC, an open-source optimization model solver developed within the COIN-OR project.

This repository contains
- [datasets](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/datasets) with the public holidays for Berlin and Munich
- some code to aid in implementation, focus on [domain modelling](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/src/mdl) and [visualization](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/src/plotting)
- Jupyter notebook with [completely implemented version](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/blob/main/notebooks/tutorial-demo.ipynb) which you can browse independently.
   - Changing the model configuration, e.g. preferences and bonus preferrences is possible in the configuration file  (`src/config.py`)
   - Want to change the cost and/or utility calculation? Check `src/utils/calculators.py`

## Case study

During the workshop, we used the problem below as a case study.

> Julie and Trevor like planning things long ahead, one such thing: the days they take their
time off during the year 2025.
> 
> Makes sense right?
>
> Holidays are a scarce resource: we only have our yearly budget. J and T want to coordinate 
and take off on the same days
> 
> Both have their own **generic preferences**
> - Julie has a preference for Mondays off
> - Trevor likes Fridays more
>
> and **preferred dates** for having time off
> - 2025 June 19th: for the hangover after that wedding party on Wednesday
>
> Additional considerations
> - Being 2 days off? Not sufficient to rest
> - The longer we are off, the better we rest
> - More than 30 consecutive calendar days away? Not even trying to get that approved
> 
> ... oh and let’s be opportunistic: weekends and holidays do not “cost” us a day

## Modelling approach and optimization model formulation

_Disclaimer: the notebooks implement a particular modelling approach. This is only one out of a range of possible modelling approach, and is considered the easiest one to grasp the combined aspects of day-level attributes and period-level attributes._

Instead of defining the decision variables representing "on which days to schedule a day off", a period-level modelling approach is used. A **period** is characterized by the starting date $d$ and the duration of the period in days $l$. We can then represent some examples for the month of May 2024 in the visual below. Red squares represent public holidays.
- (May 1, 2024; 5 days) in green require 2 days from the budget as May 1, 4 and 5 are either public holidays or weekends.
- (May 9, 2024; 4 days) in yellow requires 1 day from the budget
- (May 9, 2024; 5 days) in orange requires 2 days from the budget

For each of these periods, the cost in terms of holiday units and value / utility - as sum of marginal day-level value and duration-level value - can be predetermined.

![image](https://github.com/user-attachments/assets/8d963c3b-98cd-4d4e-93e0-d482a198aa85)

### Variables and sets
$p_{d, l}$: binary variable to indicate whether we take time off starting on day $d$ for a duration of $l$ days (1) or not (0)

$P$: set of all periods (d, l) with start and end date within the planning period

$P_{\delta}  \subset P$: Subset of all existing periods which overlap with day $\delta$, i.e. meaning $\delta$ falls inbetween $d$ and $d+l-1$

### Parameters
$c_{d, l}$: number of units to be used from holiday budget for taking time off starting on day $d$ for a duration of $l$ days

$u_{d, l}$: utility / value we get from taking time off starting on day $d$ for a duration of $l$ days

$B$: holiday budget, e.g. we can take 30 days off on a yearly basis

### Optimization model
#### Objective function

$\max \sum_{(d, l) \in P}{u_{d,l} * p_{d, l}}$

#### Constraint 1: holiday budget

$\sum_{(d, l) \in P}{c_{d,l} * p_{d,l}} \leq B$

#### Constraint 2: single-day coverage
We can only get the value of a specific day once, and hence it does not make sense to have two periods which cover a specific date. To model this, we can add a constraint for each day $d$ in the year (or more generic: the planning period) and enforce that at most one period containing that date can be selected.

$\sum_{(d, l) \in P_{\delta}}{x_{d,l}} \leq 1$

#### [optional] Constraint 3: longer period required
To illustrate that we can extend the model with additional constraints to come closer to our own preferences, a third constraint states that we should have at least one period with $M$ consecutive days off. 

Set $P^{\geq M}$ represents all periods $p_{d, l}: l \geq M$. Then we can add the following constraint:

$\sum_{(d, l) \in P^{\geq M}}{p_{d,l}} \geq 1$


## Installation

### Using uv (recommended)
```bash
uv sync
```

### Using pip (alternative)
```bash
pip install -r requirements.txt
``` 