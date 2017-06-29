import csv
import sys
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt

def write_first_line( f, artist_list ):
    
    f.write("ARTIST NAME,")
    num_artists = len(artist_list)
    for c in range(num_artists):
        if c == (num_artists-1):
            f.write( "%s\n" % (artist_list[c]) )
        else:                
            f.write( "%s," % (artist_list[c]) )

    f.write("USER # \ ARTIST #,")        
    for c in range(num_artists):
        if c == (num_artists-1):
            f.write( "%d\n" % (c) )
        else:                
            f.write( "%d," % (c) )


if __name__ == "__main__":

    # usersha1-artmbid-artname-plays.tsv
    # usersha1-profile.tsv

    #path = 'lastfm-dataset-360K/usersha1-profile.tsv'
    path = 'lastfm-dataset-360K/usersha1-artmbid-artname-plays.tsv'
    #out_path = 'lastfm-dataset-360K/rel_mat.csv'
    out_path = 'src/rel_matrix/'
    # build up an artist vector
    csv.field_size_limit(sys.maxsize)

    #number of top artists to select
    N = 100
    
    #artists = set([])
    artists = dict([])
    users = dict([])
    user_index = 0
    artist_index = 0
    print "Building Artist and User histo vector"

    with open( path, 'r') as tsvin:
        for row in csv.reader(tsvin, delimiter = '\t'):

            if row[2] in artists:
                artists[row[2]] = artists[row[2]] + 1
            else:
                artists[row[2]] = 1
                
            if row[0] not in users:
                users[row[0]] = user_index
                user_index = user_index + 1
                
    num_artists = len(artists)
    num_users = len(users)

    
    
    #print "Print top 100 artists and number of users who played them"

    #sorted_artists = [ k for k in artists ]
    sorted_artists = sorted(artists, key=artists.__getitem__, reverse = True)
    #sorted_plays = sorted(artists.values(), reverse = True)

    # slice the list
    sorted_artists = sorted_artists[0:N]
    #sorted_plays = sorted_plays[0:N]

    # randomize sorted artists
    shuffle( sorted_artists )

    #for i in range(N):
    #    print "Artists: %s | #Users: %d" % (sorted_artists[i], sorted_plays[i] )
    
    print "Build the relevance vectors"

    num_artists = N

    #print num_users
    #print num_artists
    
    rel_mat = np.zeros( (num_users, num_artists) )
    rel_mat = np.array(rel_mat)
    rel_mat = np.int8(rel_mat)
    
    f_users = set([])
    user_index = -1
    with open( path, 'r') as tsvin:
        for row in csv.reader(tsvin, delimiter = '\t'):
            if row[0] not in f_users:
                f_users.add(row[0])
                user_index+=1

            if row[2] in sorted_artists:
                rel_mat[user_index, sorted_artists.index(row[2])] = 1
            

    if len(f_users) != num_users:
        print "Number of users error!"

    num_users = len(f_users)
    print "Save relevance vector to file!"
    print "Creating File"
    # assign a new file name
    fname = "rel_mat.csv"
    f = open( out_path + fname, 'w')
    write_first_line(f, sorted_artists)

    for r in range(num_users):
        f.write("%d," % (r))
        for c in range(num_artists):
            if c == (num_artists-1):
                f.write("%d\n" % rel_mat[r,c])
            else:
                f.write("%d," % rel_mat[r,c])

    print "Done!"
