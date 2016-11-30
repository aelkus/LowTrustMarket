#!/usr/bin/env python

"""
An earlier version of the LowTrustMarket sim (from early 2014). In retrospect I like this one better than the later one.
Found it while digging through some of my old files for a blog post I was writing. How time flies!
"""



import sys
import random
import argparse

class Records(object):
    def __init__(self):
        self.averageGoodAgentWealthHistory = []
        self.averageBadAgentWealthHistory = []
        self.tradesPerTurnHistory = []

records = Records()

class Trader(object):
    def __init__(self, id):
        #how much money and price. Price is set on initialization by market class
        self.money = 100
        self.price = 0    #can be 2 or 4

        #hold good and bad agents
        self.memoryListGoodAgent = []
        self.memoryListBadAgent = []

        #whether it is a greedy or fair agent. Set on initialization
        self.agentType = random.randint(0,1)

        #unique ID used in trading determinations. Set on trader objects instantiation by Market()
        self.agentNumber = id

class Market(object):
    def __init__(self, numOfAgents, transactionLimit, dunbarNumberOption):
        # Instantiate a list of the agents in the simulation and give them unique IDs
        self.agentList = [Trader(x) for x in range(numOfAgents)]

        self.dunbarNumberOption = dunbarNumberOption
        self.transactionLimit = transactionLimit

        self.tradeStatus = 0    #both partners in a trade must agree to trade status to be true, with true = 2
        self.totalTrades = 0


        self.marketClock = 0 #timekeeping within the market used for debugging

    def setupMarketMethod(self):
        """
        Run at the beginning of every simulation to create agent characteristics, but not afterwards
        """
        self.assignAgentPrice()       #assign agents their price by agent type

    def simRun(self):
        """
        Run every turn of a simulation
            Do as many transactions as needed
            Update reporters
            Write to file
            Reset the trade counter
        """
        self.randomPairControl()   #run the transaction method
        self.report()
        self.totalTrades = 0 #resets trade counter to zero after full run of market submodel

    def assignAgentPrice(self):
        """
        give agents price
       
        Bad agents (1) get 4, good agents (0) get 2
        """

        for traderAgent in self.agentList:      #set the prices based on type. If 0, fair agent charges 2. If 1, bad agents charges 4
            if traderAgent.agentType == 0:
                traderAgent.price = 2
            else:
                traderAgent.price = 4

    def randomPairControl(self):         #runs for as many times as the transaction limit provided at runtime
        for x in range(self.transactionLimit):
            self.randomPair(self.dunbarNumberOption)


    def randomPair(self, dunbar):
        """
        Initialize a counter that will stop at 2 agents
        Initialize a data structure to hold a pair of agents that trade

        Shuffle the list order to randomize it
        Take first 2 agents from the shuffled list

        If both agents agree to trade after doing a check of their memories, trade
        Trade, assess whether trade was good or bad and mark agent as type if not already in memory list

        If agent's memory list is full, just increment the trade counter
        Else if agent's memory list is not full, do memory processes (see additional documentation) and increment trade counter

        Increment the timer for keeping time within the market

        If dunbar == True,  there is a memory limit of 150
        on combined length of good agent and bad agent lists
        if it exceeds length, can't add to list

        """
        DUNBAR_NUMBER = 150
        counter = 0
        pair = []

        random.shuffle(self.agentList)

        for traderAgent in self.agentList:
            if counter != 2:
                pair.append(traderAgent)
                counter += 1

        agent1 = pair[0]
        agent2 = pair[1]

        # Trade if other agent is in Good list or not present in Bad list
        if agent2.agentNumber in agent1.memoryListBadAgent:
            self.tradeStatus += 1
            agent2.money = agent2.money - 1

        if agent2.agentNumber in agent1.memoryListGoodAgent:
            agent2.money = agent2.money + 0.5

        if agent1.agentNumber in agent2.memoryListBadAgent:
            self.tradeStatus += 1
            agent1.money = agent1.money - 1

        if agent1.agentNumber in agent2.memoryListGoodAgent:
            agent1.money = agent1.money + 0.5

        if self.tradeStatus == 0:

            agent1.money = agent1.money - agent2.price
            agent2.money = agent2.money - agent1.price
            agent1.money += agent1.price
            agent2.money += agent2.price

            self.totalTrades += 1

            if dunbar == False:

                if agent2.price == 4:
                    agent1.memoryListBadAgent.append(agent2.agentNumber)

                if agent2.price == 2 and agent2.agentNumber not in agent1.memoryListGoodAgent:
                    agent1.memoryListGoodAgent.append(agent2.agentNumber)

                if agent1.price == 4:
                    agent2.memoryListBadAgent.append(agent1.agentNumber)

                if agent1.price == 2 and agent1.agentNumber not in agent2.memoryListGoodAgent:
                    agent1.memoryListGoodAgent.append(agent1.agentNumber)

                for badAgentNumber in agent2.memoryListBadAgent:
                    if badAgentNumber not in agent1.memoryListBadAgent:
                        agent1.memoryListBadAgent.append(badAgentNumber)

                for goodAgentNumber in agent2.memoryListGoodAgent:
                    if goodAgentNumber not in agent1.memoryListGoodAgent:
                        agent1.memoryListGoodAgent.append(goodAgentNumber)

                for goodAgentNumber in agent1.memoryListGoodAgent:
                    if goodAgentNumber not in agent2.memoryListGoodAgent:
                        agent2.memoryListGoodAgent.append(goodAgentNumber)

                for badAgentNumber in agent1.memoryListBadAgent:
                    if badAgentNumber not in agent2.memoryListBadAgent:
                        agent2.memoryListBadAgent.append(badAgentNumber)

            elif dunbar == True:
                if (len(agent1.memoryListBadAgent) + len(agent1.memoryListGoodAgent)) <= DUNBAR_NUMBER:

                    if agent2.price == 4:
                        agent1.memoryListBadAgent.append(agent2.agentNumber)

                    if agent2.price == 2 and agent2.agentNumber not in agent1.memoryListGoodAgent:
                        agent1.memoryListGoodAgent.append(agent2.agentNumber)

                if (len(agent2.memoryListBadAgent) + len(agent2.memoryListGoodAgent)) <= DUNBAR_NUMBER:
                    if agent1.price == 4:
                        agent2.memoryListBadAgent.append(agent1.agentNumber)

                    if agent1.price == 2 and agent1.agentNumber not in agent2.memoryListGoodAgent:
                        agent1.memoryListGoodAgent.append(agent1.agentNumber)

                if (len(agent1.memoryListBadAgent) + len(agent1.memoryListGoodAgent)) <= DUNBAR_NUMBER:

                    for badAgentNumber in agent2.memoryListBadAgent:
                        if badAgentNumber not in agent1.memoryListBadAgent:
                            agent1.memoryListBadAgent.append(badAgentNumber)

                    for goodAgentNumber in agent2.memoryListGoodAgent:
                        if goodAgentNumber not in agent1.memoryListGoodAgent:
                            agent1.memoryListGoodAgent.append(goodAgentNumber)

                if (len(agent2.memoryListBadAgent) + len(agent2.memoryListGoodAgent)) <= DUNBAR_NUMBER:

                    for goodAgentNumber in agent1.memoryListGoodAgent:
                        if goodAgentNumber not in agent2.memoryListGoodAgent:
                            agent2.memoryListGoodAgent.append(goodAgentNumber)

                    for badAgentNumber in agent1.memoryListBadAgent:
                        if badAgentNumber not in agent2.memoryListBadAgent:
                            agent2.memoryListBadAgent.append(badAgentNumber)

        self.tradeStatus = 0

    def report(self):

        self.marketClock += 1

        goodAgentMoneyReportList = []
        badAgentMoneyReportList = []

        sumGoodAgentMoneyReportList = 0
        sumBadAgentMoneyReportList = 0

        dividerForAverages = len(self.agentList)

        averageGoodAgentMoney = 0
        averageBadAgentMoney = 0


        for traderAgent in self.agentList:

            if traderAgent.agentType == 0:
                goodAgentMoneyReportList.append(traderAgent.money)
            else:
                badAgentMoneyReportList.append(traderAgent.money)

        sumGoodAgentMoneyReportList = sum(goodAgentMoneyReportList)
        sumBadAgentMoneyReportList = sum(badAgentMoneyReportList)

        averageGoodAgentMoney = sumGoodAgentMoneyReportList/dividerForAverages
        averageBadAgentMoney = sumBadAgentMoneyReportList/dividerForAverages

        records.averageGoodAgentWealthHistory.append(averageGoodAgentMoney)
        records.averageBadAgentWealthHistory.append(averageBadAgentMoney)
        records.tradesPerTurnHistory.append(self.totalTrades)

        return None

class Simulation(object):
    """
    Create an instance of the market
    
    Run the market setup method once
    
    Run market's main methods for preset number of model time steps

    """
    def __init__(self, traders, transactions, runsNumber, dunbarNumber):
        self.market = Market(traders, transactions, dunbarNumber)   # instantiate market-bound objects
        self.dunbarNumber = dunbarNumber
        self.runsNumber = runsNumber

    def runSim(self):
        self.market.setupMarketMethod()
        for simRun in range(self.runsNumber):
            self.market.simRun()

        return None

def FinalDataReport(fileName, simClock):

    fileObj = open(fileName, 'wb')

    lineList = []

    lineList.append('Step;AverageFairAgentWealth;AverageGreedyAgentWealth;TradesPerTurn;\n')

    numSteps = simClock
    for i in range(numSteps):
        oneLine = "%s;%0.2f;%0.2f;%0.2f;\n" %(i,records.averageGoodAgentWealthHistory[i], records.averageBadAgentWealthHistory[i], records.tradesPerTurnHistory[i])
        lineList.append(oneLine)

    fileObj.writelines(lineList)

    fileObj.close()

def main():

    parser = argparse.ArgumentParser(description="Simulate agent trades with and/or without a Dunbar number.")
    parser.add_argument("number", type=int, help="number of traders (try 300)")
    parser.add_argument("limit", type=int, help="transaction limit (try 150)")
    parser.add_argument("sims", type=int, help="number of simulation runs to run (try 100)")
    parser.add_argument("unique_sims",type=int, help="number of unique simulations to create(try 1)")
    parser.add_argument('-dunbar', action='store_true', default=False, help="whether to use Dunbar number (default: False)")

    args = parser.parse_args()

    # command line output for display of what modeler chose
    print "args.number: ",
    print args.number
    print "args.limit: ",
    print args.limit
    print "args.sims: ",
    print args.sims
    print "args.unique_sims",
    print args.unique_sims
    print "args.dunbar: ",
    print args.dunbar

    # positional arguments: number of agents, transaction limit, use dunbar number, number of simulations to run
    for x in range(args.unique_sims):
        sim = Simulation(args.number, args.limit, args.sims, args.dunbar)
        sim.runSim()

    simClock = args.unique_sims * args.sims

    if args.dunbar == False:
        FinalDataReport("DeceptionSimNoDunbar.txt", simClock)
    if args.dunbar == True:
        FinalDataReport("DeceptionSimDunbar.txt", simClock)

    raw_input("please hit enter: ")
    return None

if __name__ == "__main__":
    main()