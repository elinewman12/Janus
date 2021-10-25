from markov_chain import MarkovChain

class MarkovLibrary:

    def __init__(self):
        self.chains = {}
    
    def add_markov_chain(self, chain):
        self.chains[chain.name] = chain
