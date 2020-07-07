"""
Exemplo do problema de atribuicao de trafego entre DC e PTT
Caso generico
Autor: Rodrigo de Souza Couto - GTA/PEE/COPPE/UFRJ
Nota: Exemplo baseado no codigo disponivel em https://github.com/coin-or/pulp
"""

#FALAR NA AULA QUE EH SEMPRE BOM OLHAR O LP RESULTANTE COM UM EXEMPLO PEQUENO

from pulp import *

##Parametros
#DCs
dcList = ["DC_1","DC_2"]

#PTTs
pttList = ["PTT_1","PTT_2","PTT_3"]

#Capacidade dos PTTs
capPtts = {"PTT_1": 10000, "PTT_2": 15000, "PTT_3": 21000}

#Trafego dos DCs
trafegoDCs = {"DC_1":16000,"DC_2":12000}

#Custos - Cada linha eh um DC e cada coluna eh um PTT
matrizCustos = [[100,150,225],[125,100,225]]

#Transformando a lista de custos em dicionario custos["DC_i"]["PTT_j"]
custos = makeDict([dcList,pttList],matrizCustos,0)

#Definindo o problema de minimizacao de custos entre DCs e PTTs
prob = LpProblem("DCs_e_PTTs_generico",LpMinimize)

#Definindo as variaveis
variaveisX = LpVariable.dicts("X",(dcList,pttList),0,None,LpContinuous)

#Criando tuplas (DC_i,PTT_j)
tuplasDCPTT = [(dc,ptt) for dc in dcList for ptt in pttList]

#Declarando a funcao objetivo
prob += lpSum([variaveisX[dc][ptt]*custos[dc][ptt] for (dc,ptt) in tuplasDCPTT]), "Custo"

#Declarando restricoes dos PTTs
for ptt in pttList:
    prob += lpSum([variaveisX[dc][ptt] for dc in dcList]) <= capPtts[ptt], "Capacidade_%s"%ptt

#Declarando restricoes dos DCs
for dc in dcList:
    prob += lpSum([variaveisX[dc][ptt] for ptt in pttList]) == trafegoDCs[dc], "Trafego_%s"%dc

#Escrevendo o arquivo
prob.writeLP("DC_PTT_generico.lp")

#Resolvendo o problema
prob.solve(CPLEX())
#prob.solve()

#Mostrando o estado da solucao
print("Status:", LpStatus[prob.status])

#Imprimindo as variaveis do problema
for v in prob.variables():
    print(v.name, "=", v.varValue)

#Imprimindo a funcao objetivo
print("O custo total da infraestrutura eh= ", value(prob.objective))

