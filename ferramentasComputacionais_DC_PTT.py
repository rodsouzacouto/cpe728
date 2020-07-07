"""
Exemplo do problema de atribuicao de trafego entre DC e PTT
Caso particular para 2 DCs e 3 PTTs
Autor: Rodrigo de Souza Couto - GTA/PEE/COPPE/UFRJ
Nota: Exemplo baseado no codigo disponivel em https://github.com/coin-or/pulp
"""
from pulp import *

##Parametros
#Custo DC i -> PTT j
c_1_1 = 100
c_1_2 = 150
c_1_3 = 225
c_2_1 = 125
c_2_2 = 100
c_2_3 = 225
#Capacidade do PTT
b_1 = 10000
b_2 = 15000
b_3 = 21000
#Trafego do DC
d_1 = 16000
d_2 = 12000

#Definindo o problema de minimizacao de custos entre DCs e PTTs
prob = LpProblem("2_DCs_e_3_PTTs",LpMinimize)

#Definindo as variaveis
x_1_1=LpVariable("X_DC_1_PTT_1",0,None,LpInteger)
x_1_2=LpVariable("X_DC_1_PTT_2",0,None,LpInteger)
x_1_3=LpVariable("X_DC_1_PTT_3",0,None,LpInteger)
x_2_1=LpVariable("X_DC_2_PTT_1",0,None,LpInteger)
x_2_2=LpVariable("X_DC_2_PTT_2",0,None,LpInteger)
x_2_3=LpVariable("X_DC_2_PTT_3",0,None,LpInteger)

#Declarando a funcao objetivo
prob += c_1_1*x_1_1 + c_1_2*x_1_2 + c_1_3*x_1_3 + c_2_1*x_2_1 + c_2_2*x_2_2 + c_2_3*x_2_3 ,"Custo"

#Declarando restricoes dos PTTs
prob += x_1_1 + x_2_1 <= b_1, "Capacidade_PTT_1"
prob += x_1_2 + x_2_2 <= b_2, "Capacidade_PTT_2"
prob += x_1_3 + x_2_3 <= b_3, "Capacidade_PTT_3"

#Declarando restricoes dos DCs
prob += x_1_1 + x_1_2 + x_1_3 == d_1, "Trafego_DC_1"
prob += x_2_1 + x_2_2 + x_2_3 == d_2, "Trafego_DC_2"

#Escrevendo o arquivo
prob.writeLP("DC_PTT.lp")

#Resolvendo o problema
#prob.solve(CPLEX())
prob.solve()

#Mostrando o estado da solucao
print("Status:", LpStatus[prob.status])

#Imprimindo as variaveis do problema
for v in prob.variables():
    print(v.name, "=", v.varValue)

#Imprimindo a funcao objetivo
print("O custo total da infraestrutura eh= ", value(prob.objective))
