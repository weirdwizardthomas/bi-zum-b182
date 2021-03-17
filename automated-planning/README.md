# Automated planning

# Requirements
Fast Downward planner - follow instructions [here](https://courses.fit.cvut.cz/BI-ZUM/tutorials/planovani/index.html).

# Running
Problems and domains (alternative scenarios) come in pairs. To solve a problem, query a problem against its respective domain,
```
./fast_downward.py ../vanilla-domain.pddl ../vanilla-problem.pddl --search "astar(lmcut())"
```
Solution, if any, will be located in `./sas_plan`.

# Scenarios

|Scenario                            | Domain                                                                          | Problem                                                                          |
|---                                 |---                                                                              |---                                                                               |
| Default                            | [vanilla-domain.pddl](vanilla-domain.pddl)                                      | [vanilla-problem.pddl](vanilla-problem.pddl)                                     |
| Academy and Town not connected     | [academy-town-disconnected-domain.pddl](academy-town-disconnected-domain.pddl)  | [academy-town-disconnected-problem.pddl](academy-town-disconnected-problem.pddl) |
| No boat at river                   | [boats-secured-domain.pddl](boats-secured-domain.pddl)                          | [boats-secured-problem.pddl](boats-secured-problem.pddl)                         |
| Retired pirate does not have a map | [expirate-out-of-maps-domain.pddl](expirate-out-of-maps-domain.pddl)            | [expirate-out-of-maps-problem.pddl](expirate-out-of-maps-problem.pddl)           | 
| No pearls at sea                   | [extinct-pearls-domain.pddl](extinct-pearls-domain.pddl)                        | [extinct-pearls-problem.pddl](extinct-pearls-problem.pddl)                       |