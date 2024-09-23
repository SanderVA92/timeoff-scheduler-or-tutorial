# Operations Research problem-solving case

This repository accompanies a workshop on Operations Research problem solving using an exact optimization model formulation. During the workshop we covered subsequent steps of problem refinement, (initial) model formulation, followed by the actual implementation in Jupyter notebooks. Within the notebooks, `PuLP` is used as wrapper to define the model and solve it with CBC, an open-source optimization model solver developed within the COIN-OR project.

This repository contains
- [datasets](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/datasets) with the public holidays for Berlin and Munich
- some code to aid in implementation, focus on [domain modelling](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/src/mdl) and [visualization](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/tree/main/src/plotting)
- Jupyter notebooks with [some preparation to implement the model](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/blob/main/notebooks/tutorial.ipynb) independently, and a [completely implemented solution](https://github.com/SanderVA92/timeoff-scheduler-or-tutorial/blob/main/notebooks/tutorial-solution.ipynb)
  - Note that the "empty" notebook already contains quite some snippets and focusses on the actual optimization model implementation, i.e. creating variables and using those to define the objective function and constraints


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
>Both have their own **generic preferences**
> - Julie has a preference for Mondays off
> -Trevor likes Fridays more
>
> and **preferred dates** for having time off
> - 2025 June 19th: for the hangover after that wedding party on Wednesday
>
>Additional considerations
> - Being 2 days off? Not sufficient to rest
>  - The longer we are off, the better we rest
> - More than 30 consecutive calendar days away? Not even trying to get that approved
> 
> ... oh and let’s be opportunistic: weekends and holidays do not “cost” us a day
