the word is finite

three keys to use State Machine

#1. Artificial Intelligence
#2. modeling simulations
#3. refactor


- adding a state or status field to your model is the most obvious sign of state machine.
- boolean fields are usually also a good indication, like published or paid. Also timestamps that can have a NUL value like published_at and paid_at are a usable sign
- Finally, having records that are only valid for a given period in time, like subscriptions with a start and end date.


before_transition
after_transition
