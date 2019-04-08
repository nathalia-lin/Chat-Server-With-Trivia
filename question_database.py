import random
def list_choose(level):
    list_micro_q = [" what is microeconomics about?\n\
    A.Study of Business Environment\n\
    B.Study of financial position of the economy\n\
    C.Study of the Economy at Micro Level\n\
    D. None of the above","Slope of indifference curve indicates that:\n\
    A. Marginal Rate of Substitution of x for y\n\
    B. Prices of x and y\n\
    C. Slope of the budget line\n\
    D. Change in prices","While in perfect competition:\n\
    A. Firms are price taker\n\
    B. Buyers are independant\n\
    C. Input prices are given\n\
    D. the demand curve is flat","monopoly is a market where:\n\
    A.large number of buyer\n\
    B. Small number of buyer\n\
    C. A single firm controlling the market\n\
    D. Any of the above","Law of demand states that\n\
    A. With the increase in price Quantity increases\n\
    B. With the increase in price quantity decreases other things remaining the same.\n\
    C. Quantity does not change with any increase in price.\n\
    D. All of the above","Which of the following is not a factor of production?\n\
    A.labor\n\
    B.land\n\
    C.money\n\
    D.capital\n\
    E.All of these answers are factors of production.","points on the ppf are:\n\
    A. inefficient\n\
    B. normative\n\
    C. unattainable\n\
    D. efficient\n\
    E. none of these answers. ","Which of the following will not shift a country's production possibilities frontier ?outward\n\
    A. An advanced in technology\n\
    B. An increase in the labour force\n\
    C. An increase in the capital stock\n\
    D. A reduction in unemployment"]
    list_micro_a = ["C","A","A","C","B","E","D","A"]

    # dic_micro_q = {1:"\n1. what is microeconomics about?\n\
    #         A.Study of Business Environment\n\
    #         B.Study of financial position of the economy\n\
    #         C.Study of the Economy at Micro Level\n\
    #         D. None of the above",\
    #         2:"\n2. Slope of indifference curve indicates that:\n\
    #         A. Marginal Rate of Substitution of x for y\n\
    #         B. Prices of x and y\n\
    #         C. Slope of the budget line\n\
    #         D. Change in prices",\
    #         3:"\n3. While in perfect competition:\n\
    #         A. Firms are price taker\n\
    #         B. Buyers are independant\n\
    #         C. Input prices are given\n\
    #         D. the demand curve is flat",\
    #         4:"\n4. monopoly is a market where:\n\
    #         A.large number of buyer\n\
    #         B. Small number of buyer\n\
    #         C. A single firm controlling the market\n\
    #         D. Any of the above",\
    #         5:"\n5. Law of demand states that\n\
    #         A. With the increase in price Quantity increases\n\
    #         B. With the increase in price quantity decreases other things remaining the same.\n\
    #         C. Quantity does not change with any increase in price.\n\
    #         D. All of the above",\
    #     }
    
    list_fof_q =[ "a bond has a current yield of 9 %, and a yield to maturity of 10%. is the bond selling above or below par value?\n\
     A. Above\n\
     B. Below\n\
     C. Par value\n\
     D. Not enough information",\
     "Consider a 10-year, coupon paying bond with a coupon rate 4% and a yield-to-maturity of 5%. What is the annual HPR over the life pf the bond if all the coupon payment are reinvested at a rate of 4.5%?\n\
     A. Greater than 5 %\n\
     B. Greater than 4.5 % but less than 5%\n\
     C. Greater than 4%, but less than 4.5%\n\
     D. Can’t tell from the information given.",\
     "As the yield increase, the duration of a risk-free, coupon paying bond will:\n\
     A. Increase\n\
     B. Stay the same\n\
     C. Decrease\n\
     D. Not enough information to tell",\
    "The buyer of a put and seller of a call:\n\
     A. must disagrees about whether the price of the underlying is expected to go up or down\n\
     B. both have rights and not obligations\n\
     C. both profit if the price of the underlying falls\n\
     D. both b and c are correct\n\
     E.None of the above",\
     " The standard deviation of a two-asset portfolio is a linear function of the assets’ weigh when:\n\
     A. the assets have a correlation coefficient less than zero\n\
     B. the assets have a correlation coefficient equal to zero\n\
     C. the assets have a correlation coefficient greater than zero\n\
     D. the assets have a correlation coefficient equal to one\n\
     E. the assets have a correlation coefficient less than one.",\
     "This type of risk is avoidable through proper diversification\n\
     A. porfolio risk\n\
     B. systematic risk\n\
     C. unsystematic risk\n\
     D. total risk",\
     "An aggressive common stock would have beta: \n\
     A. equal to zero\n\
     B. greater than one\n\
     C. equal to one\n\
     D. less than one",\
     "A line that describes the relationship between an individual security's returns and returns on the market portfolio:\n\
     A. characteristic line\n\
     B. security market line\n\
     C. capital market line\n\
     D. beta"]
    list_fof_a = ["B","B","C","C","D","C","B","B"]

    list_cf_q = ["Projected cash flow is typically defined to be \n\
    A. the best case expected cash flow\n\
    B. an average of the possible cash flows from the various scenarios\n\
    C. the largest possible cash flow\n\
    D. the cash flow that results in the lowest NPV but still allows the project to be accepted\n\
    E. the least likely cash flow",\
    "Positive net present value projects : \n\
    A. tend to be rare in a highly competitive market\n\
    B. will likely have a source of value that is difficult to determine\n\
    C. tend to be rare in a highly monopolistic market\n\
    D. will typically occur in international markets, but not domestic markets\n\
    E. are common for firms in old, well established industries",\
    "Which of the following is not a reason why companies are not always entirely clear on their dividend policy?\n\
    A. For fear of giving away sensitive information.\n\
    B. In order to maintain a managerial advantage over shareholders.\n\
    C. Because they do not know how much is available for dividends.\n\
    D. Companies have different abilities to communicate.",\
    "What does pecking order theory say? (The < or = sign represents company preference here.\n\
    A. Internal capital < debt < external equity.\n\
    B. Internal capital = debt = external equity.\n\
    C. Internal capital > debt > external equity.\n\
    D. External equity > debt < internal capital.",\
    "In a simple perfect capital market, what happens if dividends are brought forward?\n\
    A. Share price goes up.\n\
    B. It is impossible to know.\n\
    C. Share price goes down.\n\
    D. Share price remains the same.",\
    "The traditional approach towards the valuation of a company assumes:\n\
    A. that the overall capitalization rate holds constant with changes in financial leverage.\n\
    B. that there is an optimum capital structure.\n\
    C. that total risk is not altered by changes in the capital structure.\n\
    D. that markets are perfect.",\
    "Which of the following is an argument for the relevance of dividends?\n\
    A.Informational content.\n\
    B. Reduction of uncertainty.\n\
    C. Some investors' preference for current income.\n\
    D. All of the above.",\
    "The 'information effect' refers to the notion that:\n\
    A. a corporation's actions may convey information about its future prospects.\n\
    B. management is reluctant to provide financial information that is not required by law.\n\
    C. agents incur costs in trying to obtain information.\n\
    D. the financial manager should attempt to manage sensitive information about the firm."]
    list_cf_a = ["B","B","C","C","C","D","D","A"]
    if level == 1:#microeconomics
        return list_micro_q,  list_micro_a
    elif level ==2: #when all conquerors jointly ansewered thequestions in level 2
        return list_fof_q, list_fof_a
    elif level ==3: #after the frist two round is passed by the conqueror
        return list_cf_q, list_cf_a



def random_generation(level):
        choice_list =[1,2,3,4,5,6,7,8]
        chosen =[]
        for i in range(4):
            position = random.randint(0,len(choice_list)-1)
            chosen.append(choice_list[position])
            choice_list=choice_list[:position]+choice_list[position+1:]
            
        question_list,answer_list = list_choose(level)
        q_dic = {1:"",2:"",3:"",4:""}
        a_dic = {1:"",2:"",3:"",4:""}
        counting = 1
        
        for i in chosen:
            index = i-1
            question_chosen = "\n{}. ".format(counting)+question_list[index]
            q_dic[counting] = question_chosen
            a_dic[counting] =answer_list[index]
            counting +=1
        return q_dic, a_dic



        

        
        

