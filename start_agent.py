# A Sample Carrom Agent to get you started. The logic for parsing a state
# is built in
from math import sqrt, sin, cos, tan
from thread import *
import time
import socket
import sys
import argparse
import random
import ast
import numpy as np

pockets = [(44.1, 44.1), (755.9, 44.1), (755.9, 755.9), (44.1, 755.9)]
count=0

# Parse arguments

parser = argparse.ArgumentParser()

parser.add_argument('-np', '--num-players', dest="num_players", type=int,
                    default=1,
                    help='1 Player or 2 Player')
parser.add_argument('-p', '--port', dest="port", type=int,
                    default=12121,
                    help='port')
parser.add_argument('-rs', '--random-seed', dest="rng", type=int,
                    default=0,
                    help='Random Seed')
parser.add_argument('-c', '--color', dest="color", type=str,
                    default="Black",
                    help='Legal color to pocket')
args = parser.parse_args()


host = '127.0.0.1'
port = args.port
num_players = args.num_players
random.seed(args.rng)  # Important
color = args.color

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))


# Given a message from the server, parses it and returns state and action


def parse_state_message(msg):
    s = msg.split(";REWARD")
    s[0] = s[0].replace("Vec2d", "")
    reward = float(s[1])
    state = ast.literal_eval(s[0])
    return state, reward

#distance between two points
def dist(p1, p2):
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def agent_1player(state):

    flag = 1
    # print state
    try:
        state, reward = parse_state_message(state)  # Get the state and reward
    except:
        pass

  
    coin_radius = 15.01
    striker_radius = 20.6
    
    coins = state['Black_Locations'] + state['White_Locations'] + state['Red_Location']
    redcoin = state['Red_Location']
   
    
    coin_count=[0,0,0,0,0,0]
    
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
  
    final_list = []
    final_list.append(list1)
    final_list.append(list2)
    final_list.append(list3)
    final_list.append(list4)
    final_list.append(list5)
    final_list.append(list6)


    for coin in coins:
	#Left-Bottom Pocket
    	if coin[0]<=400 and coin[1]<=165:
		coin_count[0] = coin_count[0]+1
		final_list[0].append(coin)
        elif coin[0]>=400 and coin[1]<=165:
		#Right-Bottom pocket
		coin_count[1] = coin_count[1]+1
		final_list[1].append(coin)
	elif coin[0]<=165 and coin[1]>=165:
		#Left-Top pocket
		coin_count[2] = coin_count[2]+1
		final_list[2].append(coin)
	elif coin[0]>=800-165 and coin[1]>=165:
		#Right-Top pocket
		coin_count[3] = coin_count[3]+1
		final_list[3].append(coin)
	elif coin[0]<=400 and coin[1]>=165:
		#Left-Top NOT Pocket
		coin_count[4] = coin_count[4]+1
		final_list[4].append(coin)
	else:
		#Right-Top NOT Pocket
		coin_count[5] = coin_count[5]+1
		final_list[5].append(coin)


    yx = zip(coin_count, final_list)
    yx.sort()
    himu = [x for y, x in yx]

    list_to_be_considered = himu[5] + himu[4] + himu[3] + himu[2] + himu[1] + himu[0] 

   
    force = 1.0

    for coin in list_to_be_considered:
	#Left-Bottom Pocket
    	if coin[0]<=400 and coin[1]<=165:
		angle = (np.arctan2(coin[1]-155,coin[0]-600)*180)/np.pi	
		if angle <= -135:
    			angle = 360+angle
		a = str(0.75) + ',' + str(angle) + ',' + str(force)
		break
        elif coin[0]>=400 and coin[1]<=165:
		#Right-Bottom pocket
		angle = (np.arctan2(coin[1]-155,coin[0]-200)*180)/np.pi	
		if angle <= -135:
    			angle = 360+angle
		a = str(0.25) + ',' + str(angle) + ',' + str(force)
		break
	elif coin[0]<=165 and coin[1]>=165:
		#Left-Top pocket
		angle = (np.arctan2(coin[1]-155,coin[0]-170)*180)/np.pi	
		if angle <= -135:
    			angle = 360+angle
		a = str(0) + ',' + str(angle) + ',' + str(force)
		break
	elif coin[0]>=800-165 and coin[1]>=165:
		#Right-Top pocket
		angle = (np.arctan2(coin[1]-155,coin[0]-800+170)*180)/np.pi	
		if angle <= -135:
    			angle = 360+angle
		a = str(1) + ',' + str(angle) + ',' + str(force)
		break
		
	else:
		if redcoin:
			angle = (np.arctan2(redcoin[0][1]-155,redcoin[0][0]-400)*180)/np.pi
			#Left-Top NOT Pocket
		elif coin[0]<=400 and coin[1]>=165:
			angle = (np.arctan2(coin[1]-155,coin[0]-400)*180)/np.pi
			#Right-Top NOT Pocket
		else:
			angle = (np.arctan2(coin[1]-155,coin[0]-400)*180)/np.pi
	    
		if angle <= -135:
			angle = 360+angle
	    
		a = str(0.5) + ',' + str(angle) + ',' + str(force)
		break
		

    try:
        s.send(a)
    except Exception as e:
        print "Error in sending:",  a, " : ", e
        print "Closing connection"
        flag = 0

    return flag


def agent_2player(state, color):

    flag = 1

    # Can be ignored for now
    #a = str(random.random()) + ',' + \
    #    str(random.randrange(-45, 225)) + ',' + str(random.random())

    # print state
    try:
        state, reward = parse_state_message(state)  # Get the state and reward
    except:
        pass

    coin_radius = 15.01
    striker_radius = 20.6
    #If passed color is white then my color will be white
    if color == [169, 121, 47]:
    	rival_coins = state["Black_Locations"]  
    	my_coins = state['White_Locations'] 
    else:
	rival_coins = state['White_Locations'] 
    	my_coins = state["Black_Locations"]  

    diff = [0,0,0,0,0,0,0,0]
    my_coin_count = [0,0,0,0,0,0,0,0]
    rival_count = [0,0,0,0,0,0,0,0]

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    list8 = []
    final_list = []
    final_list.append(list1)
    final_list.append(list2)
    final_list.append(list3)
    final_list.append(list4)
    final_list.append(list5)
    final_list.append(list6)
    final_list.append(list7)
    final_list.append(list8)
    extra = []


    for coin in my_coins:
	if coin[0]<145 and coin[1]<400 and coin[1]-coin[0]>0:
		final_list[0].append(coin)
                my_coin_count[0] = my_coin_count[0]+1
	elif coin[0]>800-145 and coin[1]<400 and coin[1]+coin[0]-800>0:
		final_list[1].append(coin)
		my_coin_count[1] = my_coin_count[1]+1
	elif coin[1]+coin[0]-800>0 and coin[0]<=400:
		final_list[2].append(coin)
		my_coin_count[2] = my_coin_count[2]+1
	elif coin[1]-coin[0]>0 and coin[0]>=400:
		final_list[3].append(coin)	
		my_coin_count[3] = my_coin_count[3]+1	
    	elif coin[0]<=400 and coin[1]<=145 and coin[1]-coin[0]<0:
		final_list[4].append(coin)
		my_coin_count[4] = my_coin_count[4]+1
        elif coin[0]>=400 and coin[1]<=145 and coin[1]+coin[0]-800<0:
		final_list[5].append(coin)
		my_coin_count[5] = my_coin_count[5]+1
	elif coin[1]+coin[0]-800<0:
		final_list[6].append(coin)
		my_coin_count[6] = my_coin_count[6]+1
	elif coin[1]-coin[0]<0:
		final_list[7].append(coin)
		my_coin_count[7] = my_coin_count[7]+1
	else:
                extra.append(coin)



    for coin in rival_coins:
	if coin[0]<145 and coin[1]<400 and coin[1]-coin[0]>0:
		rival_count[0] = rival_count[0]+1
    
	elif coin[0]>800-145 and coin[1]<400 and coin[1]+coin[0]-800>0:
		rival_count[1] = rival_count[1]+1

	elif coin[1]+coin[0]-800>0 and coin[0]<=400:
		rival_count[2] = rival_count[2]+1

	elif coin[1]-coin[0]>0 and coin[0]>=400:
		rival_count[3] = rival_count[3]+1		

    	elif coin[0]<=400 and coin[1]<=145 and coin[1]-coin[0]<0:
		rival_count[4] = rival_count[4]+1
		
        elif coin[0]>=400 and coin[1]<=145 and coin[1]+coin[0]-800<0:
		rival_count[5] = rival_count[5]+1

	elif coin[1]+coin[0]-800<0:
		rival_count[6] = rival_count[6]+1

	elif coin[1]-coin[0]<0:
		rival_count[7] = rival_count[7]+1
	
    for i in range(0,8):
	diff[i] = rival_count[i] - my_coin_count[i]

    # minimum rival coins should be present in the area of my coin

    yx = zip(diff, final_list)
    yx.sort()
    himu = [x for y, x in yx]
    list_to_be_considered = himu[0] + himu[1] + himu[2] + himu[3] + himu[4] + himu[5] + himu[6] +himu[7] + extra


    #print list_to_be_considered
    if len(list_to_be_considered)>=3:
    	coins = list_to_be_considered + state['Red_Location']
    else:
	coins = state['Red_Location'] + list_to_be_considered


    for coin in coins:
	if coin[0]<145 and coin[1]<400 and coin[1]-coin[0]>0:
		#Working fine
		#reverse shot for pocket 1 ... coin should be lying above the line 2

		x_on_top_wall = (755.9-44.1)*((coin[0]-44.1)/(coin[1]-44.1))+44.1
		tan_theta = (755.9 - coin[1])/(x_on_top_wall-coin[0]) # tan_theta = a/b
		b = (coin[1]-145)/tan_theta 
		#print "x_on_top_wall ",x_on_top_wall
		position = x_on_top_wall + x_on_top_wall - coin[0] + b
		angle = (np.arctan2(755.9-145,x_on_top_wall-position)*180)/np.pi # y = baseline+striker radius
		#print "angle",angle
		if angle<=-135:
			angle = angle+360
		final_pos = (position-145)/490.0
		if final_pos<0.0 or final_pos > 1:
                	angle = (np.arctan2(coin[1]-165,coin[0]-400)*180)/np.pi

	    		if angle <= -135:
	    			angle = 360+angle
	    
	    		a = str(0.5) + ',' + str(angle) + ',' + str(0.5)
		else:
			a = str(final_pos) + ',' + str(angle) + ',' + str(1.0)
		break
	elif coin[0]>800-145 and coin[1]<400 and coin[1]+coin[0]-800>0:
		#reverse shot for pocket 2 ... coin should be lying above the line 1
		#print coin[0]

		x_on_top_wall = (755.9-44.1)*((coin[0]-755.9)/(coin[1]-44.1))+755.9 
		tan_theta = (755.9-coin[1])/(coin[0]-x_on_top_wall) # tan_theta = a/b
		b = (coin[1]-145)/tan_theta

		#print "x_on_top_wall ",x_on_top_wall
		position = x_on_top_wall - ( coin[0] - x_on_top_wall ) - b
		angle = (np.arctan2(755.9-145,x_on_top_wall-position)*180)/np.pi # y = baseline+striker radius
		#print "angle",angle
		if angle<=-135:
			angle = angle+360
		final_pos = (position-155)/490.0
		if final_pos<0.0 or final_pos > 1:
                	angle = (np.arctan2(coin[1]-165,coin[0]-400)*180)/np.pi

	    		if angle <= -135:
	    			angle = 360+angle
	    
	    		a = str(0.5) + ',' + str(angle) + ',' + str(0.5)
		else:
			a = str(final_pos) + ',' + str(angle) + ',' + str(1.0)
		break
		#Working fine
	elif coin[1]+coin[0]-800>0 and coin[0]<=400:
		#LEFT Region
		
		position = coin[0]+15 # coin x position + coin radius + lesser than striker radius
		
		angle = (np.arctan2(coin[1]-145,position-400)*180)/np.pi
		if angle <= -135:
	    		angle = 360+angle

		a = str(0.5) + ',' + str(angle) + ',' + str(0.6)
		break
		#Workng fine
	elif coin[1]-coin[0]>0 and coin[0]>=400:
		#RIGHT Region
		
		position = coin[0]-15 # coin x position -( coin radius + lesser than striker radius)
		
		angle = (np.arctan2(coin[1]-145,position-400)*180)/np.pi
		if angle <= -135:
	    		angle = 360+angle

		a = str(0.5) + ',' + str(angle) + ',' + str(0.6)
		break
	#Left-Bottom Pocket
        #pocket 2 and the coin should lie on same side of line 1
	#44.1-755.9 < 0
    	elif coin[0]<=400 and coin[1]<=145 and coin[1]-coin[0]<0:
		
		angle = (np.arctan2(coin[1]-145,coin[0]-600)*180)/np.pi
		if angle <= -135:
    			angle = 360+angle
		a = str(0.75) + ',' + str(angle) + ',' + str(0.3)
		break
        #pocket 1 and the coin should lie on same side of line 1
	#1*44.1+1*44.1-800 < 0
        elif coin[0]>=400 and coin[1]<=145 and coin[1]+coin[0]-800<0:
		#Right-Bottom pocket
		
		angle = (np.arctan2(coin[1]-145,coin[0]-200)*180)/np.pi
		if angle <= -135:
    			angle = 360+angle
		a = str(0.25) + ',' + str(angle) + ',' + str(0.3)
		break

	elif coin[1]+coin[0]-800<0:
		#Left-Top pocket
		angle_p_c = (np.arctan2(coin[1]-755.9,coin[0]-44.1)*180)/np.pi
		
		angle = 200
		position = 1
		
		for x in range(155,800-155,2): 
			#step size is radius of the coin
			angle_c_s = (np.arctan2(coin[1]-(145+20.6),coin[0]-x)*180)/np.pi # y = baseline+striker radius
			temp = angle_c_s
			
			
			mini = 180.0
			#print "diff",abs(angle_c_s-angle_p_c)
			if(abs(angle_c_s-angle_p_c) < mini and angle_c_s>=-45):
				mini = abs(angle_c_s-angle_p_c)
				#print "mini",mini
				angle = temp
				position = x
		
		if angle <= -135:
    			angle = 360+angle

		final_pos = (position-155)/490.0
		if final_pos<0.0 or final_pos > 1:
                	angle = (np.arctan2(coin[1]-165,coin[0]-400)*180)/np.pi

	    		if angle <= -135:
	    			angle = 360+angle
	    
	    		a = str(0.5) + ',' + str(angle) + ',' + str(0.25)
		else:
			a = str(final_pos) + ',' + str(angle) + ',' + str(0.5)
		break
	elif coin[1]-coin[0]<0:
		#Right-Top pocket
		angle_p_c = (np.arctan2(coin[1]-755.9,coin[0]-755.9)*180)/np.pi
		
		angle = 200
		position = 1
		
		for x in range(155,800-155,2): 
			#step size is radius of the coin
			angle_c_s = (np.arctan2(coin[1]-(145+20.6),coin[0]-x)*180)/np.pi # y = baseline+striker radius
			temp = angle_c_s
			
			
			mini = 180.0
			#print "diff",abs(angle_c_s-angle_p_c)
			if(abs(angle_c_s-angle_p_c) < mini and angle_c_s>=-45):
				mini = abs(angle_c_s-angle_p_c)
				#print "mini",mini
				angle = temp
				position = x
		
		if angle <= -135:
    			angle = 360+angle

		final_pos = (position-155)/490.0
		if final_pos<0.0 or final_pos > 1:
                	angle = (np.arctan2(coin[1]-165,coin[0]-400)*180)/np.pi

	    		if angle <= -135:
	    			angle = 360+angle
	    
	    		a = str(0.5) + ',' + str(angle) + ',' + str(0.25)
		else:
			a = str(final_pos) + ',' + str(angle) + ',' + str(0.5)
		break
	
	else:
	 
	    angle = (np.arctan2(coin[1]-165,coin[0]-400)*180)/np.pi
	    
	    if angle <= -135:
	    	angle = 360+angle
	    
	    a = str(0.5) + ',' + str(angle) + ',' + str(0.5)
	    break



    try:
        s.send(a)
    except Exception as e:
        print "Error in sending:",  a, " : ", e
        print "Closing connection"
        flag = 0

    return flag


while 1:
    state = s.recv(1024)  # Receive state from server
    if num_players == 1:
        if agent_1player(state) == 0:
            break
    elif num_players == 2:
        if agent_2player(state, color) == 0:
            break
s.close()
