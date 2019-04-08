"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import question_database as qd
import threading
import time
import SuperTyper

class ClientSM:
    def __init__(self, s):
        self.test = 0
        self.ghost = True
        self.question_set = 0
        self.answer_set =0 
        self.question = ''
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s   # size of the message (?)
        self.current_level = 0
        self.current_round = 0
        self.current_remain = 0
        self.msgStackLock = False
        self.msgStack = []
        threading._start_new_thread(self.recvMsg, ())
        self.choice = 0
        self.q_order = -1
        self.remainTime = None
        self.chosen_answer_list =[]
        self.current_question_chosen =""
        

    def recvMsg(self):
        while True:
            if self.msgStackLock:
                rev = myrecv(self.s)
                if rev:
                    self.msgStack.append(rev)
            time.sleep(0.01)

    def getMsg(self):
        if len(self.msgStack):
            return self.msgStack.pop(0)
        else:
            return None

    def getRemainTime(self):
        if self.remainTime == None:
            return None
        return self.remainTime * 100 // 30

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''

        if self.state == S_LOGGEDIN:
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == 'g':
                    mysend(self.s, json.dumps({"action":"start"}))
                    start = json.loads(myrecv(self.s))
                    if start["status"] == "ok":
                        self.state = S_START
                        self.out_msg += "Next let's pick sides! \nType in 'c' for conqueror \nType in 'd' for defendant \n "
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"][1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"][1:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.state = S_CHATTING
                    self.out_msg = "You are connected with: " + peer_msg["from"]

        # if we have time, we can work on printing number of conqueror and defendants
        elif self.state == S_START:
            if len(my_msg) > 0:
                mysend(self.s, json.dumps({"action":"pick_side", "side":my_msg}))
                response = json.loads(myrecv(self.s))

                if response["status"] == 'c':
                    self.state = S_PENDING
                    self.out_msg += 'You have been successfully logged in as a conqueror'
                elif response["status"] == 'd':
                    self.state = S_PENDING
                    self.out_msg += 'You have been successfully logged in as a defendant'
                elif response["status"] == 'max_c':
                    self.state = S_LOGGEDIN
                    self.out_msg+= "Sorry, there are already 3 conquerors in the game. \nYou can try logging in as a defendant"
                elif response["status"] == 'max_d':
                    self.state = S_LOGGEDIN
                    self.out_msg += "Sorry, there are already 3 defendants in the game. \nYou can try logging in as a conqueror"
                else:
                    self.out_msg += "Please type in 'c' or 'd'"

        elif self.state == S_PENDING:
            
            if my_msg == 'next':
                self.state = S_JUDGING
                self.out_msg += "Matching... Please wait"
                mysend(self.s, json.dumps({"action":"judging"}))

        elif self.state == S_JUDGING:       
                # while nxt != True:
            
            if len(peer_msg):
                
                response = json.loads(peer_msg)

                if response["status"] == "ok":  
                    
                    game_rule = response["message"]
                    self.out_msg += game_rule
                    self.state = S_INGAME
                
                elif response["status"] == "more_c":  # when the number of players are uneven
                        
                    self.out_msg += 'There were more conquerors than defendants, so you were automatically removed from the game'
                    self.state = S_LOGGEDIN
                    # mysend(self.s,json.dumps({"action":"next"}))
                    #     response = json.loads(myrecv(self.s))
                    #     # else:
                        #     self.out_msg += "There were more conquerors than defendants, so {} was automatically removed".format(response["pop"])
                elif response["status"] == "more_d":
                        # if response["pop"] == self.me:
                    self.out_msg += 'There were more defendants than conquerors, so you were automatically removed from the game'
                    self.state = S_LOGGEDIN
                        # mysend(self.s,json.dumps({"action":"next"}))
                            # nxt = True
                        # else:
                        #     self.out_msg += "There were more conquerors than defendants, so {} was automatically removed".format(response["pop"])


        elif self.state == S_INGAME:

            if not self.msgStackLock:
                self.msgStackLock = True
                self.ghost = False
                mysend(self.s, json.dumps({"action":"ingame"}))
                self.st = SuperTyper.SuperTyper()
                self.st.getTime = self.getRemainTime
                threading._start_new_thread(self.st.run, ())
            
            peer_msg = self.getMsg()
            if self.st:
                my_msg = self.st.fetchMessage()

            if peer_msg:
                response = json.loads(peer_msg)
                if response["action"] == "choose_question":
                    self.current_level  = response["level"]
                    self.current_round  = response["round"]
                    self.current_remain = response["remain"]
                    self.question_set   = response["question_dic"]
                    self.answer_set     = response["answer_dic"]
                    self.q_order = 0

                    question_list=[]
                    for i in self.question_set.values():
                        question_list.append(i)
                    
                    question_answer_list = []
                    for l in question_list[self.q_order].split("\n"):
                        if l.strip():
                            question_answer_list.append(l.strip())
                    
                    self.current_question_chosen = question_answer_list[0].strip()
                    self.chosen_answer_list = question_answer_list[1:]
                    
                    self.st.setQuestion("Please choose a question from the dataset to defend yourself (Type `n` to Switch To Next Question, `y` to Choose): ", self.current_level, self.current_remain, self.current_question_chosen, self.chosen_answer_list )

                elif response["action"] == "answer_question":
                    self.current_level  = response["level"]
                    self.current_round  =  response["round"]
                    self.question       = response["question"]
                    self.current_remain = response["remain"]
                    self.choice         = response["choice"]
                    self.current_question_chosen = response["chosen_question"]
                    self.chosen_answer_list = response["chosen_answers"]
                    
                    if response["status"] == "help":
                        self.st.setQuestion("Your friend is in need of your help~~!",self.current_level, self.current_remain,"",[])
                    
                        time.sleep(2)
                    self.st.setQuestion("This is the question for you, please choose the answer by typing in (A/B/C/D/E) ", self.current_level, self.current_remain, self.current_question_chosen, self.chosen_answer_list)
                elif response["action"] == "result":
                    result= response["result"]
                    percent = response["percent_point"]
                    self.st.setQuestion("",self.current_level, self.current_remain,"",["Game over!! Here's your game report:","In total the conquerors' team get {}".format(percent),"Based on the rule for 'Conquering Finance':","{}".format(result),""])


                elif response["action"] == "ok" and response["identity"] == "conqueror":
                    rounds =response["round"]
                    level =response["level"]
                    self.current_remain =response["remain"]
                    self.st.setQuestion("Congratulations! You got this question right~",self.current_level, self.current_remain,"",[])
                    mysend(self.s,json.dumps({"action":"success","level":self.current_level,"round":self.current_round,"remain":self.current_remain}))
                elif response["action"] == "ok" and response["identity"] == "defendant":
                    rounds =response["round"]
                    level =response["level"]
                    self.current_remain =response["remain"]
                    self.st.setQuestion("opps~~ It seems the conqueror got the question right~ ",self.current_level, self.current_remain,"",[])
                    
                    # mysend(self.s,json.dumps({"action":"success","level":level,"round":rounds,"remain":self.current_remain}))
                elif response["action"] == "wrong":
                    self.question = response["question"]
                    self._current_remain =response["remain"]
                    self.st.setQuestion("Unforturnately you answer this question wrongly, type in 'help' to get help from your friends, or type 'skip' to get to the next round",self.current_level, self.current_remain,"",[])
   
                    
                elif response["action"] == "no more":
                    self.current_remain =response["remain"]
                    self.st.setQuestion("Sorry you have no more friends to help so the system automatically gets you into the next round/level",self.current_level, self.current_remain,"",[])
                    
                    mysend(self.s, json.dumps({"action":"skip","remain":self.current_remain}))
                # elif response["action"] == "end":
                #     self.out_msg = "Game over, the conqueror team gets {} points".format(response["point"])
                elif response["action"] == "timer":
                    self.remainTime = int(response["time"])
            if my_msg:
                if self.q_order >= 0:
                    if my_msg.strip().lower() == "n":
                        self.q_order += 1
                        self.q_order %= len(self.question_set)
                    
                        question_list = []
                        for i in self.question_set.values():
                            question_list.append(i)
                        
                        question_answer_list = []
                        for l in question_list[self.q_order].split("\n"):
                            if l.strip():
                                question_answer_list.append(l.strip())

                        self.current_question_chosen = question_answer_list[0]
                        self.chosen_answer_list = question_answer_list[1:]
                        
                        self.st.setQuestion("Please choose a question from the dataset to defend yourself (Type (N/n) to Switch To Next Question, (Y/y) to Choose): ", self.current_level, self.current_remain, self.current_question_chosen, self.chosen_answer_list )
                    elif my_msg.strip().lower() == "y":
                        self.q_order += 1
                        
                        question_list = []
                        for i in self.question_set.values():
                            question_list.append(i)
                        
                        question_answer_list = []
                        for l in question_list[self.q_order-1].split("\n"):
                            if l.strip():
                                question_answer_list.append(l.strip())

                        self.current_question_chosen = question_answer_list[0]
                        self.chosen_answer_list = question_answer_list[1:]
                        
                        
                            
                        mysend(self.s,json.dumps({"action":"choose_question","message":self.q_order,"level":self.current_level,"round":self.current_round,"remain":self.current_remain,"chosen_question":self.current_question_chosen,"chosen_answers":self.chosen_answer_list}))
                        self.q_order = -1
                elif my_msg.upper() in ["A","B","C","D","E"]:
                    self.remainTime = None
                    mysend(self.s,json.dumps({"action":"answer_question","level":self.current_level,"round":self.current_round,"message":my_msg,"remain":self.current_remain,"choice":self.choice}))
                elif my_msg== "help" or my_msg =="skip":
                    self.remainTime = None
                    mysend(self.s,json.dumps({"action":my_msg,"question":self.question,"remain":self.current_remain,"choice":self.choice,"chosen_question":self.current_question_chosen,"chosen_answers":self.chosen_answer_list}))
                    
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            elif len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                print(self.peer, "self.peer")
                #receiving messages
                if peer_msg["action"] == "disconnect":
                    self.out_msg += "You are the only one left in the group." 
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "exchange":
                    self.peer = peer_msg["message"]
                    self.out_msg += peer_msg["from"] + ': ' + peer_msg["message"]
                elif peer_msg["action"] == "connect":
                    self.out_msg += "You are chatting with " + peer_msg["from"]

        
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
