import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm # Please run < pip install tqdm > to install progress bar

def baseball_simulation(world_record, success_rate):
    failure_rate = 1 - success_rate
    home_run = 0
    num_play = 0
    num_atbat = 0

    while home_run < world_record:
        # Increase this every game play
        num_play += 1
        # Check if player hit the ball
        is_atbat = np.random.choice([0,1], size=1, p=[0.5,0.5])
        if is_atbat: # If player hit the ball
            # Player start to run (home run)
            is_success = np.random.choice([0,1], size=1, p=[failure_rate, success_rate])
            home_run += is_success
            num_atbat += 1

    return num_atbat, num_play

if __name__ == "__main__":
    print('Welcome to our baseball simmulation.')
    print('Please note that the longer the simmulation, the better the model.')

    simulations = []
    num_simulation = input('Number of simulations (recommend 10000 ~ 10 mins or 1000 ~ 2 mins): ')
    num_simulation = int(num_simulation)
    
    Maris_success_rate = 1 / float(input('Home run rate (e.g. once every 14.7 opportunities): '))

    for i in tqdm(range(num_simulation)):
        num_atbat, _ = baseball_simulation(world_record=60, success_rate=Maris_success_rate)
        simulations.append(num_atbat) 

    print('Maris\'s mean opportunities per home run:', np.mean(simulations))
    print('Maris\'s standard deviation:', np.std(simulations))
    density, atbat, _ = plt.hist(simulations, bins=50)
    plt.show()

    # This section threshold the world's record home runs 
    # based on the number of opportunities Maris had that year (1961)
    # using probability cummulative function (PCF / PDF)
    atbat_Maris_1961 = 590
    valid_simulation = 0
    for i in range(len(atbat)):
        if atbat[i] <= atbat_Maris_1961:
            valid_simulation += density[i]
        else:
            break

    # compute Probablity of one player gets 60 home runs in one season
    candidate_prob = valid_simulation / np.sum(density)
    print('Probability of breaking 60 home runs with {} at bat for one player in a season:'.format(atbat_Maris_1961), candidate_prob)
    
    T = int(input('Amount of time to break the record (in seasons) e.g. 70: '))
    num_candidates = T // 3 # 1 good player produced every 3 years (or seasons)
    
    # Compute Probability at least one candidate gets 60 home runs in one season
    candidate_season_prob = 1 - (1-candidate_prob) ** num_candidates
    print('Probability of breaking 60 home runs with {} candidates in a season:'.format(num_candidates), candidate_season_prob)
    
    # Compute Probability at least one candidate gets 60 home runs over the period of T years
    prob = 1 - (1-candidate_season_prob)**T
    print('Probability of breaking 60 home runs with {} candidates during the period of {} years:'.format(num_candidates, T), prob)
    
