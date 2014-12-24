LowTrustMarket
==============

# Summary 

A simple model of low-trust markets I did for a course on agent-based computational economics. Both the program design and PEP8 compliance are extremely shoddy due to some last minute conceptual changes that forced me to completely redo the conceputal model design 24 hours prior to the deadline and then hack something together by virtue of Red Bull IV drip (the nectar of PhD students). If this is interest to me next year I'll redo it to make it PEP8 compliant and not spaghetti code-ish. What I found interesting about the process of making it was experimenting with ways in which agents could manipulate their own memories, and perhaps in the future I'll fork this to add memory decay and reinforcement, flashbulb memory, and/or unreliable memory. 

# Theory 

The model simulates an informal market where agents will often break contracts they have entered into, either provoking their counterparty to murder them or leading to a duel in which both agents die. A successful trade leads to each agent putting their counterparty in a memory structure called a social circle and initializing the counterparty's representation to nonviolent. When one agent kills a counterparty, they display the kill to their contacts (brag). Contacts can then alter their own memories to change the killing agent's representation to violent and remove the victim from memory. 

Agents decide on whether or not to honor their contractual arrangements by looking up the counterparty in memory. If the counterparty is in memory and registered as violent, they will always trade fairly. If the counterparty is in memory and registered as nonviolent (or out of memory altogether), they will make a situational decision which is modeled by a randint() function. In a previous model I used Robin Dunbar's 150 social contact cap as a structural limit on memory size, and it is enabled here as well as an input option. 

# Use notes 

Download and run the model as a Python script. The model will prompt for input parameters and specify their requirements. The market is intended to be small, so I mostly fed it inputs of between 100 to 500 agents. I also haven't tested it on a wide variety of input levels for number of agents and number of simulated model years. To facilitate the purpose of prototyping/playing around with agent memory settings output is pushed to the shell rather than an an external data file. 
