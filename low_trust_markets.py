#!/usr/bin/python

import random           

class VariableCounter(): 
	"""Container for counters and histories for primary model variables
	and secondary details. Model variables are kills and deals, 
	and secondary details are memory overwrites, memory additions,
	memory alterations, and memory delations. 
	"""
	def __init__(self):
		self.kill_counter = 0
		self.deal_counter = 0 
		self.memory_overwrite_counter = 0 
		self.memory_addition_counter = 0
		self.memory_alteration_counter = 0
		self.memory_deletion_counter = 0
		
		self.kill_history = []
		self.deal_history = []
		self.overwrite_history = []
		self.addition_history = []
		self.alteration_history = []
		self.deletion_history = []

class Observer(): 
	""" Initializes market, recorder, and agents, replaces dead agents, deletes 
	agents who have died in simulation, maintains counters, runs main model processes, and 
	outputs results to console.  
	"""
	def __init__(self, number_of_agents, number_of_model_years, dunbar_option, trade_volume):
		self.number_of_agents = number_of_agents
		self.number_of_model_years = number_of_model_years
		self.dunbar_option = dunbar_option 
		self.trade_volume = trade_volume 
		
	def modelSetup(self):
		""" Main method of model. Initializes agents, runs through model, outputs 
		results to file when model has reached time limit. 
		"""
		# create a market and populate it with agents 
		market = Market() 
		market.getAgents(self.number_of_agents, self.dunbar_option)

		# initialize data structure to hold records
		variableCounter = VariableCounter()

		# start main loop and terminate when done
		counter = 0 
		runs = self.number_of_model_years 
		trade_volume = self.trade_volume
		for run in range(runs): 
			
			# reset counters
			variableCounter.kill_counter = 0 
			variableCounter.deal_counter = 0
			variableCounter.memory_overwrite_counter = 0 
			variableCounter.memory_alteration_counter = 0 
			variableCounter.memory_addition_counter = 0
			variableCounter.memory_deletion_counter = 0
			
			# loop through main market method
			self.marketStep(market, variableCounter, trade_volume)
			counter += 1

			# write to main records
			variableCounter.kill_history.append(variableCounter.kill_counter)
			variableCounter.deal_history.append(variableCounter.deal_counter)
			variableCounter.overwrite_history.append(variableCounter.memory_overwrite_counter)
			variableCounter.alteration_history.append(variableCounter.memory_alteration_counter)
			variableCounter.addition_history.append(variableCounter.memory_addition_counter) 
			variableCounter.deletion_history.append(variableCounter.memory_deletion_counter)

		# when model is done, totals and means are pushed to command line

		print "total kills",
		print sum(variableCounter.kill_history)
		print "total deals",
		print sum(variableCounter.deal_history)
		print "total memory alterations",
		print sum(variableCounter.alteration_history)
		print "total memory additions", 
		print sum(variableCounter.addition_history)
		print "total memory overwrites"
		print sum(variableCounter.overwrite_history)
		print "total memory deletions"
		print sum(variableCounter.deletion_history)

		model_years = float(self.number_of_model_years)
		total_kills = sum(variableCounter.kill_history)
		total_deals = sum(variableCounter.deal_history)
		total_memory_delations = sum(variableCounter.deletion_history)
		total_memory_additions = sum(variableCounter.addition_history)
		total_memory_overwrites = sum(variableCounter.overwrite_history)
		total_memory_alterations = sum(variableCounter.alteration_history)
		mean_kills = total_kills/model_years 
		mean_deals = total_deals/model_years 
		mean_alterations = total_memory_alterations/model_years 
		mean_deletions = total_memory_delations/model_years 
		mean_additions = total_memory_additions/model_years 
		mean_overwrites = total_memory_overwrites/model_years

		print "mean kills",
		print mean_kills 
		print "mean deals",
		print mean_deals 
		print "mean memory alterations", 
		print mean_alterations 
		print "mean memory additions",
		print mean_additions 
		print "mean memory overwrites", 
		print mean_overwrites 
		print "mean memory deletions", 
		print mean_deletions 

		print "number of agents",
		print self.number_of_agents
		print "number of runs", 
		print self.number_of_model_years
		print "dunbar option (1 = Dunbar, 2 = No Dunbar)",
		print self.dunbar_option
		
	def marketStep(self, market, variableCounter, trade_volume): 
		"""Replace dead agents if any agents have been killed and 
		schedule number of trades specified by the trade volume.
		"""
		
		# check to see if dead agents need to be replaced
		if len(market.agents) != self.number_of_agents: 
			market.replaceAgents(self.number_of_agents, self.dunbar_option) 

		# schedule trades
		for trade in range(trade_volume): 
			market.scheduleTrade(variableCounter)

class Market(): 
	"""Contains all agents, takes commands from Observer to execute core 
	model processes. Implements a brag mechanism for killer agents to tell 
	contacts that murderer has killed someone. Core method is the trade mechanism. 
	Some market operations contain counters to collect model data. 
	"""
	def __init__(self): 
		self.agents = []
	
	def getAgents(self, agent_limit, dunbar_option): 
		"""Initialize agents, give them a Dunbar setting, 
		give them a unique ID, and add them to the agent 
		collection.
		"""
		while len(self.agents) != agent_limit:  
			agent = Agent(dunbar_option) 
			agent.id = id(agent)  
			self.agents.append(agent)

	def replaceAgents(self, agent_limit, dunbar_option): 
		"""Check to see if agents are dead and replace them
		with new agents w/ IDs and Dunbar settings.
		"""
		while len(self.agents) != agent_limit: 
			agent = Agent(dunbar_option)
			agent.id = id(agent)
			self.agents.append(agent) 

	def brag(self, killer, victim, variableCounter):
		"""Iterate through all of the killer's contacts. For 
		all contacts, alter memory to accommodate new knowledge 
		of killer and delete the victim from memory.
		"""
		for agent in self.agents: 
			if killer.id in agent.social_circle:
				agent.alterMemory(killer, variableCounter)
				agent.deleteAgentFromMemory(victim, variableCounter)

	def delete(self, victim): 
		# remove victim from agent collection 
		for agent in self.agents: 
			if agent.id == victim.id: 
				self.agents.remove(agent)

	def scheduleTrade(self, variableCounter): 
		"""Get two random agents from the market, begin the trade process, and 
		move to either successful trade, murder or duel scenario depending on 
		whether one or both agents choose to honor arrangement. 
		"""

		# get random agent from market collection
		agent1 = random.choice(self.agents)  
		agent2 = random.choice(self.agents)

		# prevents scenario in which same agent chosen twice
		if agent1.id == agent2.id: 	
			agent2 = random.choice(self.agents)

		# agents begin deal process 
		agent1.deal(agent2)
		agent2.deal(agent1)

		# schedule exchange of contacts + murder, and duel scenarios
		if agent1.decision and agent2.decision == 1: 
			variableCounter.deal_counter += 1
			agent1.memoryAddition(agent2, variableCounter)
			agent2.memoryAddition(agent1, variableCounter) 

		if agent1.decision == 1 and agent2.decision == 2: 
			variableCounter.kill_counter += 1
			self.brag(agent1, agent2, variableCounter)
			self.delete(agent2)

		if agent1.decision == 2 and agent2.decision == 1:
			variableCounter.kill_counter += 1
			self.brag(agent2, agent1, variableCounter)
			self.delete(agent2)

		if agent1.decision == 2 and agent2.decision == 2: 
			variableCounter.kill_counter += 2
			self.delete(agent1)
			self.delete(agent2)		

class Agent(): 
	"""Agents have Dunbar options, unique IDs, social circles,
	a Dunbar memory limit when enabled, and a decision container. 
	Agents may deal with counterparties, add a counterparty to memory,
	delete an counterparty from memory, or alter a counterparty's 
	representation in memory. Some agent operations have counters 
	to record model data. 
	"""
	def __init__(self, dunbar_option): 
		# dunbar option and unique ID 
		self.dunbar_option = dunbar_option 
		self.id = 0

		# social circle entries hold key-value pairs of agent id, violence status 
		# 1 = nonviolent and 2 = violent 
		self.social_circle = {}  # SC is agent contact list
		
		# when dunbar limit enabled, this is maximum allowed size of agent social circle 
		self.dunbar_limit = 150

		# decision 
		self.decision = 0 	# honor deal = 1, break deal = 2	

	# two settings -- if agent knows counterparty is nonviolent or 
	# has never met him before, situational decision process. 
	# but if agent knows counterparty is violent, will always 
	# deal fairly 

	def deal(self, counterparty):
		"""If agent knows counterparty is violent, agent will always deal fairly 
		with counterparty. However, if counterparty is either absent from memory or 
		in memory and known to be nonviolent, agent will decide randomly
		about whether or not to honor the deal.
		"""

		if counterparty.id in self.social_circle and counterparty.id == 1: 
			self.decision = random.randint(1, 2)

		if counterparty.id not in self.social_circle: 
			self.decision = random.randint(1, 2)
		
		if counterparty.id in self.social_circle and counterparty.id == 2: 
			self.decision = 1		
	
	def memoryAddition(self, counterparty, variableCounter): 
		"""When Dunbar memory is enabled, the agent will pop a 
		memory entry off the memory structure to make room if the 
		Dunbar limit has been reached. Otherwise, just add the counterparty
		to memory as key-value pair of unique ID and nonviolent setting.
		"""
		if self.dunbar_option == 1 and len(self.social_circle) == self.dunbar_limit: 
			self.social_circle.popitem()
			variableCounter.memory_overwrite_counter += 1

		if counterparty.id not in self.social_circle:
			self.social_circle[counterparty.id] = 1   
			variableCounter.memory_addition_counter +=1

	def deleteAgentFromMemory(self, victim, variableCounter):
		""" If the agent knows the victim, delete them from their memory 
		as there's little point in keeping around a dead contact.
		"""
		try: 
			del self.social_circle[victim.id]
			variableCounter.memory_deletion_counter += 1
		except KeyError: 
			pass 

	def alterMemory(self, killer, variableCounter): 
		""" When notified that a contact has killed, change his status to 
		violent. 
		"""
		self.social_circle[killer.id] = 2
		variableCounter.memory_alteration_counter += 1

def main():  
	"""
	User inputs the desired number of agents, time limit, and Dunbar setting. 
	Model gets a trade volume by dividing number of agents in half. Model makes 
	an observer object with core model parameters and runs the simulation. 
	"""
	# get user input for key parameters 
	NUMBER_OF_AGENTS = int(input('Enter any even integer to set number of agents '))
	TIME_LIMIT = int(input('Enter any integer above 0 to set model years '))
	# 1 = Dunbar and 2 = no Dunbar settings
	DUNBAR_OPTION = int(input('Enter 1 for Dunbar or 2 for no Dunbar '))

	# number of trades that will be performed each turn 
	TRADE_VOLUME = NUMBER_OF_AGENTS/2
    
	# initialize observer object to control model 
	observer = Observer(NUMBER_OF_AGENTS, TIME_LIMIT, DUNBAR_OPTION, TRADE_VOLUME) 

    # run model 
	observer.modelSetup()

if __name__ == "__main__":
	main()