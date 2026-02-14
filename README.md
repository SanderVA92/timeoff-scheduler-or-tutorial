# Operations Research problem-solving case

This repository demonstrates Operations Research problem-solving using an exact optimization model formulation. It covers the steps of problem refinement, model formulation, and implementation in a Jupyter notebook. `PuLP` is used as a wrapper to define the model and solve it with CBC, an open-source optimization solver from the COIN-OR project.  This repository has been used for:
1. a company internal tutorial - A hands-on workshop covering the full OR workflow: problem understanding, mathematical modelling, and Python implementation.
2. a talk for the [PyBerlin community on February 18th, 2026](https://www.meetup.com/pyberlin/events/312719130/) - description below


<details>
<summary><strong>Talk - Maximum time off, minimum leave: solving the holiday equation with Python and math</strong></summary>

Around the beginning of the year, German news sources publish tips on how to optimize your vacation by cleverly using Brückentage: taking a few strategic days of leave to connect weekends and public holidays into long breaks. But how can this be computed systematically? And how can it be tailored to your personal preferences?

Operations Research (OR) and mathematical optimization are powerful but often underrepresented disciplines within the broader AI and analytics landscape. In this beginner-friendly talk, we treat holiday planning as a mathematical optimization problem. Using the question "How do I maximize my benefit from taking time off?", we will walk through the full process from problem formulation to a working Python solution.
</details>

## Repository contents

- [datasets](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/datasets) with public holidays for Berlin and Munich
- [domain modelling](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/src/mdl) and [visualization](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/src/plotting) code
- [Jupyter notebook](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/blob/main/tutorial-demo.ipynb) with the complete implementation
   - Model configuration (preferences, bonus preferences): `src/config.py`
   - Cost and utility calculations: `src/utils/calculators.py`

## Case study

During the workshop, we used the problem below as a case study.

> F. likes planning things long ahead, one such thing: the days they take their time off during the year 2026.
> 
> Makes sense, right?
>
> Holidays are a scarce resource: we only have our yearly budget so we want to make the most out of it.
>
> Some of F’s considerations:
> - He likes to have Fridays off
> - He needs to do his share of covering school vacations (obligation)
> - He likes to ski
> - He really needs a 2-week vacation to go somewhere warm
> - Being 3 days off? Not sufficient to rest
> - The longer he is off, the better he rests
> - More than 20 days in a row? Not even trying to get that approved
> 
> ... oh and let’s be opportunistic: weekends and holidays come for free

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

#### [optional] Constraint 3: must-have dates off
We can enforce that specific dates must be taken off. For each must-have date $\delta$, at least one period covering that date must be selected.

$\sum_{(d, l) \in P_{\delta}}{p_{d,l}} \geq 1 \quad \forall \delta \in \text{MustHaveDates}$


#### [optional] Constraint 4: longer period required
To illustrate that we can extend the model with additional constraints to come closer to our own preferences, a third constraint states that we should have at least one period with $M$ consecutive days off.

Set $P^{\geq M}$ represents all periods $p_{d, l}: l \geq M$. Then we can add the following constraint:

$\sum_{(d, l) \in P^{\geq M}}{p_{d,l}} \geq 1$


## Installation and running the notebook

### Using uv (recommended)
```bash
uv sync
uv run --with jupyterlab jupyter lab tutorial-demo.ipynb
```

### Using pip (alternative)
```bash
pip install -r requirements.txt
pip install jupyterlab
jupyter lab tutorial-demo.ipynb
```