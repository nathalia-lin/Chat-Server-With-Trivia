def dic_choose(level):
    dic_micro_q = {1:"1. what is microeconomics about?\nA.Study of Business Environment\nB.Study of financial position of the economy\nC.Study of the Economy at Micro Leve\nD. None of the above",\
     2:"2. Slope of indifference curve indicates that:\nA. Marginal Rate of Substitution of x for y\nB. Prices of x and y\nC. Slope of the budget line\nD. Change in prices",\
     3:"3. While in perfect competition:\nA. Firms are price taker\nB. Buyers are independant\nC. Input prices are given\nD. the demand curve is flat",\
     4:"4. monopoly is a market where:\nA.large number of buyer\nB. Small number of buyer\nC. A single firm controlling the market\nD. Any of the above",\
     5:"5. Law of demand states that\nA. With the increase in price Quantity increases\nB. With the increase in price quantity decreases other things remaining the same.\nC. Quantity does not change with any increase in price.\nD. All of the above"}
    dic_micro_a = {1:"C",2:"A",3:"A",4:"C",4:"B"}

    dic_fof_q = {1:"1. a bond has a current yield of 9 %, and a yield to maturity of 10%. is the bond selling above or below par value?\n\
     A. Above\n\
     B. Below\n\
     C. Par value\n\
     D. Not enough information",\
     2:"2. Consider a 10-year, coupon paying bond with a coupon rate 4% and a yield-to-maturity of 5%. What is the annual HPR over the life pf the bond if all the coupon payment are reinvested at a rate of 4.5%?\n\
     A. Greater than 5 %\n\
     B. Greater than 4.5 % but less than 5%\n\
     C. Greater than 4%, but less than 4.5%\n\
     D. Can’t tell from the information given.",\
     3: "3. As the yield increase, the duration of a risk-free, coupon paying bond will:\n\
     A. Increase\n\
     B. Stay the same\n\
     C. Decrease\n\
     D. Not enough information to tell",\
     4: "4. The buyer of a put and seller of a call:\n\
     A. must disagrees about whether the price of the underlying is expected to go up or down\n\
     B. both have rights and not obligations\n\
     C. both profit if the price of the underlying falls\n\
     D. both b and c are correct\n\
     E.None of the above",\
     5:"5. The standard deviation of a two-asset portfolio is a linear function of the assets’ weigh when:\n\
     A. the assets have a correlation coefficient less than zero\n\
     B. the assets have a correlation coefficient equal to zero\n\
     C. the assets have a correlation coefficient greater than zero\n\
     D. the assets have a correlation coefficient equal to one\n\
     E. the assets have a correlation coefficient less than one."}
    dic_fof_a = {1:"B",2:"B",3:"C",4:"C",5:"D"}

    dic_cf_q = {1:"1. Projected cash flow is typically defined to be \n\
     A. the best case expected cash flow\n\
     B. an average of the possible cash flows from the various scenarios\n\
     C. the largest possible cash flow\n\
     D. the cash flow that results in the lowest NPV but still allows the project to be accepted\n\
     E. the least likely cash flow",\
     2:"2. Positive net present value projects : \n\
     A. tend to be rare in a highly competitive market\n\
     B. will likely have a source of value that is difficult to determine\n\
     C. tend to be rare in a highly monopolistic market\n\
     D. will typically occur in international markets, but not domestic markets\n\
     E. are common for firms in old, well established industries",\
     3:"3. Which of the following is not a reason why companies are not always entirely clear on their dividend policy?\n\
     A. For fear of giving away sensitive information.\n\
     B. In order to maintain a managerial advantage over shareholders.\n\
     C. Because they do not know how much is available for dividends.\n\
     D. Companies have different abilities to communicate.",\
     4: "4.What does pecking order theory say? (The < or = sign represents company preference here.\n\
     A. Internal capital < debt < external equity.\n\
     B. Internal capital = debt = external equity.\n\
     C. Internal capital > debt > external equity.\n\
     D. External equity > debt < internal capital.",\
     5: "5. In a simple perfect capital market, what happens if dividends are brought forward?\n\
     A. Share price goes up.\n\
     B. It is impossible to know.\n\
     C. Share price goes down.\n\
     D. Share price remains the same."}
    dic_cf_a = {1:"B",2:"B",3:"C",4:"C",5:"C"}
    
    if level == 1:#microeconomics
        return dic_micro_q,  dic_micro_a
    elif level ==2: #when all conquerors jointly ansewered thequestions in level 2
        return dic_fof_q, dic_fof_a
    elif level ==3: #after the frist two round is passed by the conqueror
        return dic_cf_q, dic_cf_a
        

        
        

