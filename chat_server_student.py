"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
edited by Yuxin Zhang
"""

import time
import threading
import socket
import select
import sys
import string
import indexer
import json
import question_database as qd
import pickle as pkl
from chat_utils import *
import chat_group as grp

class Server:
    def __init__(self):
        self.current_remain =0
        self.question_dic =0
        self.answer_dic =0
        self.count_player=0
        self.player_list=[]
        self.count =0
        
        self.point = 0
        self.user = {"conqueror":[],"defendant":[]} #
        self.user_num = {"conqueror": 0,"defendant":0}   #create a dictionary counting the users for each role, they can only be equal to enter the game
        self.level = 1 
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        #initialize past chat indices
        self.indices={}
        # sonnet
        self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        self.sonnet = pkl.load(self.sonnet_f)
        self.sonnet_f.close()
        self.total_points = 0
        self.timerInfo = {
            "time": -1,
            "to": "",
            "remain": 0,
            "question": 0,
            "activate": False
        }
        threading._start_new_thread(self.timerThread, ())
    
    def game_rule(self):
        rule = "Welcome to the game 'Conquering Finance'.\n\
        In this game, you are automatically paired with a rival.\n\
        This game can allow six player to coorporate and play agaist each other at the same time at a maximum capacity\n\
        Your gaming result is alined with the that of your teammates(who choose the same role as you do.\n\
        This game sets the rounds and levels based on the number of pairs (ex: if there's four people, we have two rounds in each level with total two levels).\n\
        If you are the defendant, you would be asked one question at each level by your rival, and the round order is decided by your log_in game order\n\
        But don't worry if you answer the question wrong, with at least one teammate, you can always type in 'help' to resort to your friends\n\
        Of course, you can also type in 'skip' to directly jump to the next round.\n\n\n\
        How the points are counted:\n\
        1). if you answered the question directly assigned to you right, you earn 100 points for your team.\n\
        2). if at one round, you use one help choice and answer it right, you earn 50 points for your team, otherwise 25 points would be deducted\n\
        3). if at one round, you use two help choices to answer the question right, you earn 20 points for your team, otherwise 20 points would be deducted\n\
        4). if you type in skip, no points would be deducted or added.\n\n\
        Criteria for winning or losing:\n\
        1) if the conquerors get 75% out of the total points, they are defined as winners \n\
        2) if not, then the defendants wins \n\n\
        So make wise choices in choosing, answering, seeking for help!\n\
        Hope you enjoy yourself~!! "
        return rule
    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        #read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        #move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        #add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        #load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name]=pkl.load(open(name+'.idx','rb'))
                            except IOError: #chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps({"action":"login", "status":"ok"}))
                    else: #a client under this name has already logged in
                        mysend(sock, json.dumps({"action":"login", "status":"duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print ('wrong code received')
            else: #client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)
        

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        print(name, "LogOut")
        pkl.dump(self.indices[name], open(name + '.idx','wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

    def getTeamBySock(self, sock):
        name = self.logged_sock2name[sock]
        for team in range(len(self.player_list)):
            for player in range(len(self.player_list[team])):
                if self.player_list[team][player] == name:
                    return team, player
        return None, None

    def timerThread(self):
        while True:
            if self.timerInfo["activate"] and self.timerInfo["time"] > 0:
                self.timerInfo["time"] -= 1
                to_sock = self.logged_name2sock[self.timerInfo["to"]]
                if self.timerInfo["time"] <= 0:
                    self.timerInfo["activate"] = False
                    mysend(to_sock, json.dumps({"action": "wrong", "question": self.timerInfo["question"], "remain": self.timerInfo["remain"]}))
                else:
                    mysend(to_sock, json.dumps({"action": "timer", "time": self.timerInfo["time"]}))
            time.sleep(1)
    
    def stopTimer(self):
        self.resetTimer("", -1, 0, 0, False)

    def resetTimer(self, to, length, question, remain, activate=True):
        self.timerInfo["to"]       = to
        self.timerInfo["time"]     = length
        self.timerInfo["question"] = question
        self.timerInfo["remain"]   = remain
        self.timerInfo["activate"] = activate

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
#==============================================================================
# handle connect request this is implemented for you
#==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "start":
                

            # if msg["action"] == "connect":
            #     to_name = msg["target"]
            #     from_name = self.logged_sock2name[from_sock]
            #     if to_name == from_name:
            #         msg = json.dumps({"action":"connect", "status":"self"})
            #     # connect to the peer
            #     elif self.group.is_member(to_name):
            #         to_sock = self.logged_name2sock[to_name]
            #         self.group.connect(from_name, to_name)
            #         the_guys = self.group.list_me(from_name)
            #         msg = json.dumps({"action":"connect", "status":"success"})
            #         for g in the_guys[1:]:
            #             to_sock = self.logged_name2sock[g]
            #             mysend(to_sock, json.dumps({"action":"connect", "status":"request", "from":from_name}))
            #     else:
            #         msg = json.dumps({"action":"connect", "status":"no-user"})
                mysend(from_sock, json.dumps({"action":"start","status":"ok"}))
#==============================================================================
# handle messeage exchange: IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                # Finding the list of people to send to
                # and index message
                pass
                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]
                    pass
                    mysend(to_sock, "...Remember to index the messages before sending, or search won't work")

#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            # elif msg["action"] == "disconnect":
            #     from_name = self.logged_sock2name[from_sock]
            #     the_guys = self.group.list_me(from_name)
            #     self.group.disconnect(from_name)
            #     the_guys.remove(from_name)
            #     if len(the_guys) == 1:  # only one left
            #         g = the_guys.pop()
            #         to_sock = self.logged_name2sock[g]
            #         mysend(to_sock, json.dumps({"action":"disconnect"}))
        
            elif msg["action"] == "judging":
                print(self.logged_name2sock)
                
                self.count +=1
                print(self.count, self.user_num)
                rule = self.game_rule()
                
                if self.count == self.user_num["defendant"]+self.user_num["conqueror"]:
                    num_defendant =self.user_num["defendant"]
                    num_conqueror =self.user_num["conqueror"]
                    
                    if num_defendant == num_conqueror :
                        total_list_name =self.user["defendant"]+self.user["conqueror"]
                        print(total_list_name)
                        self.player_list =[self.user["defendant"],self.user["conqueror"]]
                        for k in total_list_name:
                            to_sock =self.logged_name2sock[k]
                            mysend(to_sock,json.dumps({"action":"next","status":"ok","message":rule}))
                        
                    elif num_defendant - num_conqueror == 1:
                        to_name = self.user["defendant"][-1:]
                        for i in to_name:
                            to_sock = self.logged_name2sock[i]
                            mysend(to_sock,json.dumps({"action":"next","status":"more_d"}))
                        self.user["defendant"] = self.user["defendant"][:num_defendant-1]
                        self.user_num ["defendant"]-=1
                        self.player_list =[self.user["defendant"],self.user["conqueror"]]
                        left_defendant = self.user["defendant"]
                        left_conqueror = self.user["conqueror"]
                        left = left_defendant + left_conqueror
                        for j in left:
                            to_sock = self.logged_name2sock[j]
                            mysend(to_sock,json.dumps({"action":"next","status":"ok","message":rule}))
                    elif num_defendant - num_conqueror == 2:
                        to_name = self.user["defendant"][-2:]
                        for q in to_name:
                            to_sock = self.logged_name2sock[q]
                            mysend(to_sock,json.dumps({"action":"next","status":"more_d"}))
                        self.user["defendant"] = self.user["defendant"][:num_defendant-2]
                        self.user_num ["defendant"]-=2
                        self.player_list =[self.user["defendant"],self.user["conqueror"]]
                        left_defendant = self.user["defendant"]
                        left_conqueror = self.user["conqueror"]
                        left = left_defendant + left_conqueror
                        for w in left:
                            to_sock = self.logged_name2sock[w]
                            mysend(to_sock,json.dumps({"action":"next","status":"ok","message":rule}))
                    elif num_conqueror - num_defendant == 1:
                        to_name = self.user["conqueror"][-1:]
                        for e in to_name:
                            to_sock = self.logged_name2sock[e]
                            mysend(to_sock,json.dumps({"action":"next","status":"more_c"}))
                        self.user["conqueror"] = self.user["conqueror"][:num_conqueror-1]
                        self.user_num ["conqueror"]-=1
                        self.player_list =[self.user["defendant"],self.user["conqueror"]]
                        left_defendant = self.user["defendant"]
                        left_conqueror = self.user["conqueror"]
                        left = left_defendant + left_conqueror
                        for r in left:
                            to_sock = self.logged_name2sock[r]
                            mysend(to_sock,json.dumps({"action":"next","status":"ok","message":rule}))
                    elif num_conqueror - num_defendant == 2:
                        to_name = self.user["conqueror"][-2:]
                        for t in to_name:
                            to_sock = self.logged_name2sock[t]
                            mysend(to_sock,json.dumps({"action":"next","status":"more_c"}))
                        self.user["conqueror"] = self.user["conqueror"][:num_conqueror-2]
                        self.user_num ["conqueror"]-=2
                        self.player_list =[self.user["defendant"],self.user["conqueror"]]
                        left_defendant = self.user["defendant"]
                        left_conqueror = self.user["conqueror"]
                        left = left_defendant + left_conqueror
                        for y in left:
                            to_sock = self.logged_name2sock[y]
                            mysend(to_sock,json.dumps({"action":"next","status":"ok","message":rule}))
                            
                    
                            
                        
                        
                        
                  
                            
            elif msg["action"] == "ingame":
                
                self.count_player +=1
                print("One More Player")
                
                if self.count_player  == self.user_num["defendant"] + self.user_num["conqueror"]:
                    
                    self.num_level = self.count_player // 2
                    self.num_round = self.count_player // 2
                    self.total_points = self.num_round **2 * 100
                    self.current_level = 1
                    self.current_round = 1
                    self.current_remain = self.num_level -1
                           
                    to_name = self.player_list[0][0]
                    to_sock = self.logged_name2sock[to_name]
                    time.sleep(3)
                    self.question_dic, self.answer_dic = qd.random_generation(self.current_level)
                    mysend(to_sock,json.dumps({"action":"choose_question","level":self.current_level,"round":self.current_round,"remain":self.current_remain,"question_dic":self.question_dic,"answer_dic" :self.answer_dic}))
                    # print("choose_question", self.question_dic)

            elif msg["action"]=="choose_question":
                
                current_team, current_player = self.getTeamBySock(from_sock)

                question_order = str(msg["message"]).strip()
                
                question = self.question_dic[int(question_order) ]
                to_name = self.player_list[1][current_player]
                to_sock = self.logged_name2sock[to_name]
                mysend(to_sock,json.dumps({"action":"answer_question","remain":self.current_remain,"question":question,"status":"", "level":self.current_level,"choice":question_order,"round":self.current_round,"chosen_question":msg["chosen_question"],"chosen_answers":msg["chosen_answers"]}))

                self.resetTimer(to_name, 30, question, len(self.player_list[0])-1)

            elif msg["action"] == "answer_question":
                
                current_team, current_player = self.getTeamBySock(from_sock)
                # remain = msg["remain"]
                answer = msg["message"].strip()
                
                
                true_answer = self.answer_dic[int(msg["choice"])]
                question = self.question_dic[int(msg["choice"])]

                if true_answer.strip().lower() == answer.strip().lower():
                    
                    to_name = self.player_list[1][current_player]
                    to_sock = self.logged_name2sock[to_name]
                    mysend(to_sock,json.dumps({"action":"ok","round":self.current_round,"level":self.current_level,"remain":self.current_remain,"identity":"conqueror"}))
                    to_name = self.player_list[0][current_player]
                    to_sock = self.logged_name2sock[to_name]
                    mysend(to_sock, json.dumps({"action":"ok","round":self.current_round,"level":self.current_level,"remain":self.current_remain,"identity":"defendant"}))
                    if (self.current_remain ==0 and self.num_round == 1) or (self.current_remain ==1 and self.num_round == 2) or (self.current_remain ==2 and self.num_round == 3):
                        self.point += 100
                    elif (self.current_remain == 0 and self.num_round ==2) or (self.current_remain == 1 and self.num_round ==3):
                        self.point += 50
                    elif self.current_remain == 0 and self.num_round ==3 :
                        self.point += 20
                    

                else:
                    to_name = self.player_list[1][current_player]
                    to_sock = self.logged_name2sock[to_name]
                    mysend(to_sock,json.dumps({"action":"wrong","question":question,"remain":self.current_remain}))
                    if (self.current_remain == 0 and self.num_round == 2) or (self.current_remain == 1 and self.num_round ==3):
                        self.point -= 25
                    elif self.current_remain == 0 and self.num_round ==3:
                        self.point -= 20

            elif msg["action"] == "help":
                
                question = msg["question"]
                
                current_team, current_player = self.getTeamBySock(from_sock)
                to_player = (current_player+1)% len(self.player_list[current_team])
                to_name = self.player_list[current_team][to_player]
                to_sock = self.logged_name2sock[to_name]
                choice =msg["choice"]
                self.current_remain -= 1
                if to_player != current_player and self.current_remain >=0:
                    mysend(to_sock,json.dumps({"action":"answer_question","question": question, "remain":self.current_remain,"level":self.current_level,"round":self.current_round,"choice":choice,"status":"help","chosen_question":msg["chosen_question"],"chosen_answers":msg["chosen_answers"]}))
                else:
                    mysend(to_sock,json.dumps({"action":"no more","remain":0}))
                
            elif msg["action"] == "skip" or msg["action"] == "success":
                self.current_remain =self.num_level -1
                self.current_round += 1
                
                if self.current_round > self.num_round:
                    self.current_level +=1
                    self.current_round = 1

                    if self.current_level > self.num_level:
                        
                        
                        percentage_complish =  "{} / {}".format(self.point,self.total_points)
                        p_c = self.point / self.total_points
                        
                        if p_c >= 0.75:
                            for j in self.player_list[0]:
                                to_sock = self.logged_name2sock[j]
                            
                            
                                mysend(to_sock,json.dumps({"action":"result","percent_point":percentage_complish,"result":"You lose!\n\
                                Remember to choose more tricky questions next time~!"}))
                            for h in self.player_list[-1]:
                                to_sock = self.logged_name2sock[h]
                            
                                
                                mysend(to_sock,json.dumps({"action":"result","percent_point":percentage_complish,\
                                "result":"Congratulations~!You successfully conquered Finance~!"}))
                        else:
                            for x in self.player_list[0]:
                                to_sock = self.logged_name2sock[x]
                                mysend(to_sock,json.dumps({"action":"result","percent_point":percentage_complish,\
                                "result":"You win! You successfully defended Finance~!"}))
                        
                            
                            for c in (self.player_list[1]):
                                to_sock = self.logged_name2sock[c]
                                    
                                mysend(to_sock,json.dumps({"action":"result","percent_point":percentage_complish,"result":"Sorry, you didn't conqueror Finance this time~\n\
                                Remember to spend 90 % your time studying~~ Try again next time~!"}))

                        # for i in total_player_list:
                        #     to_sock = self.logged_name2sock[i]
                        #     mysend(to_sock,json.dumps({"action":"end","point":self.point}))
                        
                    else:
                        to_name = self.player_list[0][0]
                        to_sock = self.logged_name2sock[to_name]
                        self.question_dic, self.answer_dic = qd.random_generation(self.current_level)
                        mysend(to_sock,json.dumps({"action":"choose_question","level":self.current_level,"round":self.current_round,"remain":self.current_remain,"question_dic":self.question_dic,"answer_dic" :self.answer_dic}))

                        
                
                else:
                    to_name = self.player_list[0][self.current_round - 1]
                    to_sock = self.logged_name2sock[to_name]
                    self.question_dic, self.answer_dic = qd.random_generation(self.current_level)
                    mysend(to_sock,json.dumps({"action":"choose_question","level":self.current_level,"round":self.current_round,"remain":self.current_remain,"question_dic":self.question_dic,"answer_dic" :self.answer_dic}))

                    
                    
                    
                    
                    
                


                          
                  
                 
                
#==============================================================================
#                 listing available peers: IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "list":
                pass
                msg = "needs to use self.group functions to work"
                mysend(from_sock, json.dumps({"action":"list", "results":msg}))
#==============================================================================
#             retrieve a sonnet : IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "poem":
                pass
                poem = "needs to use self.sonnet functions to work"
                print('here:\n', poem)
                mysend(from_sock, json.dumps({"action":"poem", "results":poem}))
#==============================================================================
#                 time
#==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps({"action":"time", "results":ctime}))
#==============================================================================
#                 search: : IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "search":
                pass # get search search_rslt
                search_rslt = "needs to use self.indices search to work"
                print('server side search: ' + search_rslt)
                mysend(from_sock, json.dumps({"action":"search", "results":search_rslt}))

#==============================================================================
#                 the "from" guy really, really has had enough
#==============================================================================
            elif msg ["action"] == "pick_side":
                side_choice = msg ["side"]
                from_name = self.logged_sock2name[from_sock]
                if side_choice == "c":
                    self.user_num["conqueror"] +=1
                    if self.user_num["conqueror"]>3 :
                        mysend(from_sock, json.dumps({"action":"pick_side","status":"max_c"}))
                    else:
                        mysend(from_sock, json.dumps({"action":"pick_side","status":"c"}))
                        self.user["conqueror"].append(from_name)

                elif side_choice == "d":
                    self.user_num["defendant"] +=1
                
                    
                    if self.user_num["defendant"]>3 :
                        mysend(from_sock, json.dumps({"action":"pick_side","status":"max_d"}))
                    else:
                        mysend(from_sock, json.dumps({"action":"pick_side","status":"d"}))
                        self.user["defendant"].append(from_name)
                        
                        
                

        else:
            #client died unexpectedly
            self.logout(from_sock)

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)

def main():
    server=Server()
    server.run()

main()
