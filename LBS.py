# Chuanyue You
# Test by Python 2.7
# Local Beam Search for 8-queens
# goal states are states that have 0 pairs of attacking queens
# Start with k randomly generated states
# At each iteration, all the successors of all k states are generated
# If any one is a goal state, stop; else select the k best successors from the complete list and repeat.


# function to detect attack in row and diag
def row_diag(current_col,substate):
    count = 0
    for i,position in enumerate(substate):
        # attack in row
        if current_col == position:
            count += 1
        # attack in diagonal
        if abs(int(position)-int(current_col)) == i+1:
            count += 1
    return count

# function to count # of pairs of attacking queens
def violation(state):
    count = 0
    while len(state) != 1:
        current_col = state[0]
        state = state[1:]
        count += row_diag(current_col,state)
    return count

# function to generate successor for state
def generate_successor(state,successors):
    count = 0
    for i in range(len(state)):
        move = int(state[i])
        change = range(len(state))
        print(change)
        change.remove(move)
        for j in change:
            neighbor = state[:i]+str(j)+state[i+1:]
            successors[neighbor] = violation(neighbor)
            count += 1
            # stop once find goal state
            if violation(neighbor) == 0:
                break
        else:
            continue
        break
    return successors,count

import random


def LBS(K, printResult = True):
    
    # initial states generate function
    randInitial = lambda size,chars: ''.join(random.choice(chars) for i in range(size))
    
    # generate K initial states
    successors = {}
    for i in range(K):
        initial = randInitial(8,'01234567')
        successors[initial] = violation(initial)
        
    # termination condition
    Continue = True
    
    # total number of nodes visited
    n_node = 0
    
    # total steps(iterations) takes before terminate local beam search
    step = 0
    
    # list to store goal state
    goal_state = []
    
    # check if there is goal state in initial states
    if 0 in successors.values():
        Continues = False
        for state,vio in successors.items():
            if vio == 0:
                goal_state.append(state)
    
    # minimum violation of initial states
    previous_minimum = min(successors.values())
    
    # do local beam search
    local_minima = []
    while Continue:
        current_successors = {}
        for successor in successors:
            current_successors,count = generate_successor(successor,current_successors)
            n_node += count
        # select K best
        successors_keys = sorted(current_successors, key=current_successors.get, reverse=False)[:K]
        successors = {key:current_successors[key] for key in successors_keys}
        current_minimum = min(successors.values())
        step += 1
        # termination when finding goal state
        if 0 in successors.values():
            Continues = False
            for state,vio in successors.items():
                if vio == 0:
                    goal_state.append(state)
        # termination when ending in local minima
        if previous_minimum <= current_minimum:
            Continue = False
            for state,vio in successors.items():
                if vio == current_minimum:
                    local_minima.append(state)
                    
        previous_minimum = min(current_minimum,previous_minimum)
        
    if printResult:
        print ('Local Beam Search, Beam Size = ',K)
        if len(goal_state) == 0:
            print ('No goal state found in {} iteration(s) of local beam search, {} nodes were visited'.format(step,n_node))
            print ('Search was terminated when trapped in local minima: {} pairs of attacking queens'.format(previous_minimum))
            print ('local minima state(s):',local_minima,'\n')
        else:
            print ('{} goal state(s) found in {} iteration(s) of local beam search, {} nodes were visited'.format(len(goal_state),step,n_node))
            print ('Goal state(s):',goal_state,'\n')
    else:
        return len(goal_state),previous_minimum
        
k1 = 1
k2 = 10
k3 = 50
# run local beam search for 8 queens
print ('Run Local Beam Search one time for K=1, K=10, K=50:\n')
LBS(k1,printResult = True)
LBS(k2,printResult = True)
LBS(k3,printResult = True)


# run for 100 trails

# number of trails to run local beam search
n_trails = 100
# different beam size to try
k_list = [1,10,50]
# list to store average performance of different k
avgGoals = [0]*len(k_list)
avgMinima = [0]*len(k_list)
count = 0

print ('Run Local Beam Search for {} trails for K=1, K=10, K=50:\n'.format(n_trails))

for k in k_list:
    for i in range(n_trails):
        n_goal,n_minima = LBS(k,printResult = False)
        avgGoals[count] += n_goal/float(n_trails)
        avgMinima[count] += n_minima/float(n_trails)
    print ('When K = {}, the average number of goal state(s) found is {:.4f}'.format(k,avgGoals[count]))
    print ('The average pairs of attacking queens in minima is {}\n'.format(avgMinima[count]))
    count += 1
