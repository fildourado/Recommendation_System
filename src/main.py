import csv
import sys
from random import randint
import numpy as np
import math
import operator
import matplotlib.pyplot as plt

def check_equal(lst):
    return lst[1:]==lst[:-1]

def get_index_of_max(vec, S, num_artists, opt1 = False):

    if opt1:
        temp_vec_1 = []
        index = -1

        for i in range(len(vec)):
            if i not in S:
                temp_vec_1.append( vec[i] )

        all_same = check_equal(temp_vec_1)

        if all_same:
            if index == -1:
                index = index = randint( 0, (num_artists-1) )
            while index in S:
                index = index = randint( 0, (num_artists-1) )
        else:
            index, value = max(enumerate(vec), key=operator.itemgetter(1))

    else:
        index, value = max(enumerate(vec), key=operator.itemgetter(1))


    return index


def rba_UCB1_selectArtist(vec, mab_hist, S, t, num_artists, k):

    MAB_vec = [i for i in vec]

    index = -1
    val_of_max = -1

    # removes already used artists
    artist_indexes = range(num_artists)

    temp = 0.0
    all_same = check_equal(MAB_vec)

    if all_same:
        index = randint( 0, (num_artists-1) )
        return index

    else:
        for i in artist_indexes:
            if mab_hist[i] == 0:
                temp = MAB_vec[i]
            else:
                temp = MAB_vec[i] + math.sqrt( (2.0*np.log(t)) / float(mab_hist[i]) )

            if temp > val_of_max:
                val_of_max = temp
                index = i

            if val_of_max == 0.0:
                index = randint( 0, (num_artists-1) )


            if index == -1:
                print "Error"
            #print "index: %d" %(index)

    return index


def get_ucb_index(MAB_vec, t, mab_hist, S, num_artists):

    index = -1
    val_of_max = -1.0

    artist_indexes = range(num_artists)
    for j in range(k):
        if S[j] != -1:
            #num_removed_artists = num_removed_artists + 1
            artist_indexes.remove(S[j])

    temp = -1.0
    for i in artist_indexes:
        if mab_hist[i] == 0:
            temp = MAB_vec[i]
        else:
            temp = MAB_vec[i] + math.sqrt( (2.0*np.log(t+1) / float(mab_hist[i]) ))

        if temp > val_of_max:
            val_of_max = temp
            index = i

    return index


def iba_UCB1_selectArtist(vec, mab_hist, S, t, num_artists, k, opt2 = False):

    MAB_vec = [float(i) for i in vec]
    
    index = -1
    val_of_max = -1
    #print t
    if opt2:


        if index == -1:
            index = get_ucb_index(MAB_vec, t, mab_hist, S, num_artists)
        while index in S:
            MAB_vec[index] = -1.0
            index = get_ucb_index(MAB_vec, t, mab_hist, S, num_artists)
        return index

    else:

        # if all values in the MAB set are 0, then choose one at random
        # initial condition
        #if t == 0:
        #    return randint( 0, (num_artists-1) )

        # removes already used artists
        artist_indexes = range(num_artists)
        #num_removed_artists = 0

        for j in range(k):
            if S[j] != -1:
                #num_removed_artists = num_removed_artists + 1
                artist_indexes.remove(S[j])


        temp = 0.0
        temp_2 = []
        for i in artist_indexes:
            temp_2.append(MAB_vec[i])

        all_same = check_equal(temp_2)

        if all_same:
            index = randint( 0, (num_artists-1) )
            while index in S:
                index =randint( 0, (num_artists-1) )

            return index

        else:
            for i in artist_indexes:
                if mab_hist[i] == 0:
                    temp = MAB_vec[i]
                else:
                    temp = MAB_vec[i] + math.sqrt( (2.0*np.log(t)) / float(mab_hist[i]) )

                if temp > val_of_max:
                    val_of_max = temp
                    index = i

            if val_of_max == 0.0:
                index = randint( 0, (num_artists-1) )
                while index in S:
                    index =randint( 0, (num_artists-1) )

            if index == -1:
                print "Error"
            #print "index: %d" %(index)
        return index
    

def iba_e_greedy_select_artist( vec, S, e, num_artists, k):

    MAB_vec = [i for i in vec]

    # e = e*100.0
    index = -1

    # remove currently used artists from dict

    # with probability e a random arm is chosen

    # with probability 1-e
    # the arm with the current highest average is played
    if np.random.random() > e:
        #print "\tExploit"

        # Run it through at least once
        if index == -1:
            index = get_index_of_max(MAB_vec, S, num_artists, False)

        while index in S:
            #print "index %d is already in use, get next one" %(index)
            MAB_vec[index] = -1.0
            index = get_index_of_max(MAB_vec, S, num_artists, False)

    else:
        #print "\tExplore"
        if index == -1:
            index = randint( 0, (num_artists-1) )

        while index in S:
            #print "index %d is already in use, get next one" %(index)
            index = randint( 0, (num_artists-1) )

    #print "index: %d" %(index)
    return index

def rba_e_greedy_select_artist( vec, e, num_artists, k):

    MAB_vec = [i for i in vec]

    # e = e*100.0
    index = -1

    g = []

    # remove currently used artists from dict

    # with probability e a random arm is chosen

    # with probability 1-e
    # the arm with the current highest average is played
    if np.random.random() > e:
        #print "\tExploit"

        # Run it through at least once
        index = get_index_of_max(MAB_vec, g, num_artists, True)

    else:
        #print "\tExplore"
        if index == -1:
            index = randint( 0, (num_artists-1) )

    #print "index: %d" %(index)
    return index

def update(value, counts, arm, reward):

    #print "updating..."
    # CMA_n = X_n + n-1*CMA_n / (n)
    counts[arm] = counts[arm] + 1

    n = counts[arm]
    val = value[arm]

    val_1 = ((n-1)/float(n)) * val
    val_2 = (1/float(n))*reward

    new_val = val_1 + val_2

    value[arm] = new_val
    #print new_val
    return value, counts

def IBA_e_Greedy_modified( T, k, rel_mat, e, num_artists, num_users ):

    #num_artists = len(artists_id)
    #arm_rewards = [ 0.0 for i in range( num_artists ) ]

    set_avg = [ 0.0 for i in range( T ) ]

    MAB = [ [ 0.0 for i in range(num_artists) ] for j in range(k) ]
    MAB_histo = [ [ 0 for i in range(num_artists) ] for j in range(k) ]

    current_avg = 0
    sum_set = 0

    #print "Performing IBA e-greedy algo"
    # perform e-greedy IBA
    for t in range(T):

        #if t == 20:
        #    sys.exit()

        #print "time: %d" %(t)
        # select user uid
        uid = randint(0,num_users-1)
        # pre-allocate list for k artists
        S = [ -1 for i in range(k) ]

        end_time = 100
        new_e = 0.0
        if t<=end_time:
            new_e = -(((1-e)/float(100))*t) + 1.0
        else:
            new_e = e

        # select
        for i in range(k):
            S[i] = iba_e_greedy_select_artist(MAB[i], S, new_e, num_artists, k)

        relevant_set = False
        # Feedback
        for i in range(k):
            # get reward if user uid has listened to artist S[i]
            z = int(rel_mat[uid][S[i]])
            if z == 1:
                relevant_set = True
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 1.0)
            else:
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 0.0)

        # measure performance
        # performance is measuredb by the
        # percentage of sets that contained at least one relevant
        # artist
        reward = 0.0
        if relevant_set:
            reward = 1.0
        else:
            reward = 0.0

        #print "Time: %d" %(t)
        #print "Val: %d" %(val)

        if t != 0:
            val = set_avg[t-1]
            val_1 = ((t)/float(t+1)) * val
            val_2 = (1/float(t+1)) * reward
            new_val = val_1 + val_2
            set_avg[t] = new_val
        else:
            set_avg[t] = reward/(t+1)

    return set_avg
def IBA_e_Greedy( T, k, rel_mat, e, num_artists, num_users ):

    #num_artists = len(artists_id)
    #arm_rewards = [ 0.0 for i in range( num_artists ) ]

    set_avg = [ 0.0 for i in range( T ) ]

    MAB = [ [ 0.0 for i in range(num_artists) ] for j in range(k) ]
    MAB_histo = [ [ 0 for i in range(num_artists) ] for j in range(k) ]
    
    current_avg = 0
    sum_set = 0
    
    #print "Performing IBA e-greedy algo"   
    # perform e-greedy IBA
    for t in range(T):

        #if t == 20:
        #    sys.exit()
        
        #print "time: %d" %(t)
        # select user uid
        uid = randint(0,num_users-1)
        # pre-allocate list for k artists
        S = [ -1 for i in range(k) ]

        # select
        for i in range(k):
            S[i] = iba_e_greedy_select_artist(MAB[i], S, e, num_artists, k)

        relevant_set = False
        # Feedback
        for i in range(k):
            # get reward if user uid has listened to artist S[i]
            z = int(rel_mat[uid][S[i]])
            if z == 1:
                relevant_set = True
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 1.0)
            else:                
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 0.0)

        # measure performance
        # performance is measuredb by the
        # percentage of sets that contained at least one relevant
        # artist
        reward = 0.0
        if relevant_set:
            reward = 1.0
        else:
            reward = 0.0

        #print "Time: %d" %(t)    
        #print "Val: %d" %(val)
        
        if t != 0:
            val = set_avg[t-1]
            val_1 = ((t)/float(t+1)) * val
            val_2 = (1/float(t+1)) * reward
            new_val = val_1 + val_2
            set_avg[t] = new_val
        else:
            set_avg[t] = reward/(t+1)

    return set_avg


def RBA_e_Greedy( T, k, rel_mat, e, num_artists, num_users ):

    #num_artists = len(artists_id)
    #arm_rewards = [ 0.0 for i in range( num_artists ) ]

    MAB = [ [ 0.0 for i in range(num_artists) ] for j in range(k) ]
    MAB_histo = [ [ 0 for i in range(num_artists) ] for j in range(k) ]
    
    set_avg = [ 0.0 for i in range( T ) ]

    current_avg = 0
    sum_set = 0

    #print "Performing RBA e-greedy algo"   
    # perform e-greedy IBA
    for t in range(T):

        # select user uid
        uid = randint(0,num_users-1)
        # pre-allocate list for k artists
        S = [ -1 for i in range(k) ]

        # select 
        for i in range(k):
            S[i] = rba_e_greedy_select_artist(MAB[i], e, num_artists, k)

        relevant_set = False
        first_click = False
        # Feedback
        for i in range(k):
            # get reward if user uid has listened to artist S[i]
            z = int(rel_mat[uid][S[i]])
            if z == 1:
                if first_click == False:
                    relevant_set = True
                    first_click = True
                    # update the MAB reward vectors
                    MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 1.0)
                else:
                    # update the MAB reward vectors
                    MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 0.0)
                
            else:
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 0.0)
                

        # measure performance
        # performance is measured by the
        # percentage of sets that contained at least one relevant
        # artist
        reward = 0
        if relevant_set == True:
            reward = 1.0
        else:
            reward = 0.0

        #print "Time: %d" %(t)
        #print "Val: %d" %(val)

        if t != 0:
            val = set_avg[t-1]
            val_1 = ((t)/float(t+1)) * val
            val_2 = (1/float(t+1)) * reward
            new_val = val_1 + val_2
            set_avg[t] = new_val
        else:
            set_avg[t] = reward/(t+1)

    return set_avg


def IBA_UCB1( T, k, rel_mat, num_artists, num_users):

    #arm_rewards = [ 0.0 for i in range( num_artists ) ]
    MAB = [ [ 0.0 for i in range(num_artists) ] for j in range(k) ]
    MAB_histo = [ [ 0 for i in range(num_artists) ] for j in range(k) ]
    
    set_avg = [ 0.0 for i in range( T ) ]

    current_avg = 0
    sum_set = 0

    #print "Performing IBA UCB1 algo"   
    # perform e-greedy IBA
    for t in range(T):

        #print "Time: %d" % (t)

        # select user uid
        uid = randint(0,num_users-1)
        # pre-allocate list for k artists
        S = [ -1 for i in range(k) ]

        # select 
        for i in range(k):
            S[i] = iba_UCB1_selectArtist(MAB[i], MAB_histo[i], S, t, num_artists, k, False)

        relevant_set = False
        # Feedback
        for i in range(k):
            # get reward if user uid has listened to artist S[i]
            z = int(rel_mat[uid][S[i]])
            if z == 1:
                relevant_set = True
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 1.0)
            else:                
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 0.0)

        # measure performance
        # performance is measured by the
        # percentage of sets that contained at least one relevant
        # artist
        reward = 0
        if relevant_set == True:
            reward = 1.0
        else:
            reward = 0.0

        #print "Time: %d" %(t)    
        #print "Val: %d" %(val)

        if t != 0:
            val = set_avg[t-1]
            val_1 = ((t)/float(t+1)) * val
            val_2 = (1/float(t+1)) * reward
            new_val = val_1 + val_2
            set_avg[t] = new_val
        else:
            set_avg[t] = reward/(t+1)


    return set_avg

def RBA_UCB1( T, k, rel_mat, num_artists, num_users ):

    #num_artists = len(artists_id)
    #arm_rewards = [ 0.0 for i in range( num_artists ) ]

    MAB = [ [ 0.0 for i in range(num_artists) ] for j in range(k) ]
    MAB_histo = [ [ 0 for i in range(num_artists) ] for j in range(k) ]
    
    set_avg = [ 0.0 for i in range( T ) ]

    current_avg = 0
    sum_set = 0

    #print "Performing RBA UCB1 algo"   
    # perform e-greedy IBA
    for t in range(T):

        # select user uid
        uid = randint(0,num_users-1)
        # pre-allocate list for k artists
        S = [ -1 for i in range(k) ]

        # select 
        for i in range(k):
            S[i] = rba_UCB1_selectArtist(MAB[i], MAB_histo[i], S, t, num_artists, k)

        relevant_set = False
        first_click = False
        # Feedback
        for i in range(k):
            # get reward if user uid has listened to artist S[i]
            z = int(rel_mat[uid][S[i]])
            if z == 1:
                if first_click == False:
                    relevant_set = True
                    first_click = True
                    # update the MAB reward vectors
                    MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 1.0)
                else:
                    # update the MAB reward vectors
                    MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 0.0)
                
            else:
                # update the MAB reward vectors
                MAB[i], MAB_histo[i] = update(MAB[i],MAB_histo[i],S[i], 0.0)
                

        # measure performance
        # performance is measured by the
        # percentage of sets that contained at least one relevant
        # artist
        reward = 0
        if relevant_set == True:
            reward = 1.0
        else:
            reward = 0.0

        #print "Time: %d" %(t)
        #print "Val: %d" %(val)

        if t != 0:
            val = set_avg[t-1]
            val_1 = ((t)/float(t+1)) * val
            val_2 = (1/float(t+1)) * reward
            new_val = val_1 + val_2
            set_avg[t] = new_val
        else:
            set_avg[t] = reward/(t+1)

    return set_avg



if __name__ == "__main__":

    path = '/home/fdourado/UCLA/ee238/project/src/rel_matrix/rel_mat.csv'

    num_users = 25000
    
    index = 0
    rel_mat = []
    artists_id = []
    artists = []
    
    with open( path, 'r') as csvin:
        for row in csv.reader(csvin, delimiter = ','):
            if index == 0:
                # store list of artists
                artists = row[1:]
            elif index == 1:
                artists_id = row[1:]
            else:
                rel_mat.append(row[1:])
                
            index = index + 1
            

    # down sample number of users
    rel_mat = rel_mat[:num_users]
    num_artists = len(artists_id)
    #rel_mat = [[0 for i in range(num_artists)] for j in range(num_users)]


    #T = 50000 # total time
    T = 100000
    k = 3 # number of artists to show user. also number of MABs
    e = 0.01

    set_avg_1 = [ 0.0 for i in range(T)]
    set_avg_2 = [ 0.0 for i in range(T)]
    set_avg_3 = [ 0.0 for i in range(T)]
    set_avg_4 = [ 0.0 for i in range(T)]
    set_avg_5 = [ 0.0 for i in range(T)]

    # Number of simulations to run
    num_sims = 10
    print "IBA e-Greedy:"
    for i in range(num_sims):
        print i
        temp_vec = IBA_e_Greedy( T, k, rel_mat, e, num_artists, num_users)
        set_avg_1 = [ x + y for x,y in zip(temp_vec, set_avg_1) ]

    if num_sims>0:
        set_avg_1 = [ x/num_sims for x in set_avg_1 ]


    print "RBA e-Greedy:"
    for i in range(num_sims):
        print i
        temp_vec = RBA_e_Greedy( T, k, rel_mat, e, num_artists, num_users)
        set_avg_2 = [ x + y for x,y in zip(temp_vec, set_avg_2) ]

    if num_sims>0:
        set_avg_2 = [ x/num_sims for x in set_avg_2 ]

    print "IBA UCB1:"
    for i in range(num_sims):
        print i
        temp_vec = IBA_UCB1( T, k, rel_mat, num_artists, num_users)
        set_avg_3 = [ x + y for x,y in zip(temp_vec, set_avg_3) ]

    if num_sims>0:
        set_avg_3 = [ x/num_sims for x in set_avg_3 ]

    print "RBA UCB1:"
    for i in range(num_sims):
        print i
        temp_vec = RBA_UCB1( T, k, rel_mat, num_artists, num_users)
        set_avg_4 = [ x + y for x,y in zip(temp_vec, set_avg_4) ]

    if num_sims>0:
        set_avg_4 = [ x/num_sims for x in set_avg_4 ]

    print "IBA e-Greedy Modified:"
    for i in range(num_sims):
        print i
        temp_vec = IBA_e_Greedy_modified( T, k, rel_mat, e, num_artists, num_users)
        set_avg_5 = [ x + y for x,y in zip(temp_vec, set_avg_5) ]
    if num_sims>0:
        set_avg_5 = [ x/num_sims for x in set_avg_5 ]

    print "done!"

    tm = 1.0-(1.0/math.exp(1))
    theo_max = [tm for i in range(T)]

    t = np.arange(T)

    start = 100

    # Find IBA theoretical max
    artists_popularity = [0 for i in range(num_artists)]
    for i in range(num_artists):
        for j in range(num_users):
            artists_popularity[i] = artists_popularity[i] + int(rel_mat[j][i])

    sorted_artists = sorted(range(len(artists_popularity)), key=lambda i: artists_popularity[i])[-k:]

    print [artists[i] for i in sorted_artists]

    atleast_1 = 0;
    for i in range(num_users):
        a = 0
        for j in range(k):
            a = a + int(rel_mat[i][sorted_artists[j]])
        if a > 0:
            atleast_1 = atleast_1 + 1


    iba_max = atleast_1/float(num_users)

    iba_max_vec = [iba_max for i in range(T)]

    plt.semilogx(t[start:], set_avg_1[start:])
    plt.semilogx(t[start:], set_avg_2[start:])
    plt.semilogx(t[start:], set_avg_3[start:])
    plt.semilogx(t[start:], set_avg_4[start:])
    plt.semilogx(t[start:], set_avg_5[start:])
    plt.semilogx(t[start:], iba_max_vec[start:])
    plt.grid()


    plt.legend(['IBA E-Greedy', 'RBA E-Greedy', 'IBA UCB1', 'RBA UCB1', 'IBA E-Greedy Modified', 'Theoretical Max'], loc = 'upper right')
    #plt.legend(['IBA E-Greedy', 'RBA E-Greedy', 'IBA UCB1', 'Offline Theoretical Max'], loc = 'upper right')
    #plt.legend(['IBA UCB1', 'Offline Theoretical Max'], loc = 'upper right')
    #plt.legend(['IBA E-Greedy', 'IBA UCB1', 'Offline Theoretical Max'], loc = 'upper right')


    title = 'Num MABs: %d | Epsilon = %d%%' % (k,int(e*100))
    plt.xlabel('Time Steps')
    plt.ylabel('Fraction of Relevant Sets')
    plt.title(title)
    plt.axis([0, T, 0, 1])
    plt.show()
    
    
