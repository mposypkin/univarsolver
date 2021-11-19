import math
import sympy as sym
import pandas as pd
import interval as ival
import uvarprob as uvpr
import bnb as bnb
import sub as sub
import ivalprocessor as ivproc
import gridsearch as gs

# from sortedcontainers import SortedList
from sortedcontainers import SortedKeyList


def read_problems(fname):
    data = pd.read_csv(fname, index_col = 'name', comment = '#')
    return data

# problems = read_problems("problems.csv")
problems = read_problems("/tmp/shek.csv")
print(problems)
name = 'shekel_1'
prob = uvpr.UniVarProblem(name, problems.loc[name,'objective'], problems.loc[name,'a'], problems.loc[name,'b'], problems.loc[name,'min_f'], problems.loc[name,'mins_x'].strip('][').split(', '))
print(prob)

dp = ivproc.IntervalProcessor(prob.min_f, prob.mins_x[0], prob, 0.0001)

sl = SortedKeyList(key = lambda s : s.level)
sub = sub.Sub(0, 0, ival.Interval([prob.a, prob.b]))
dp.compute_bounds(sub)
sl.add(sub)
print(sl)
cnt = 1000
print("steps performed: ", bnb.bnb(sl, cnt, dp))
print("Record value = ", dp.rec_v, " at ", dp.rec_x);
print(sl)

true_min = gs.grid_search(prob.objective, prob.a, prob.b, 1e-3)
print("Grid search:", true_min)
prob.mins_x = [true_min[0]]
prob.min_f = true_min[1]
print("problem = ", prob)
print("type = ", type(problems.loc[name,'mins_x']))
print("type = ", type(prob.mins_x))
problems.loc[name,'mins_x'] =  str([round(true_min[0], 5), 1.])
problems.loc[name,'min_f'] = round(true_min[1], 5)
problems.to_csv('/tmp/prob.csv')

# while len(sl) > 0:
#     print(sl.pop())
