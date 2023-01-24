import matplotlib.pyplot as plt

#Estudo de Caso 1: Crescimento da População Brasileira de 1980-2016
#DataSus

dados = open ("populacao_brasileira.csv").readlines()
x = []
y = []

for i in range(len(dados)):
    if i !=0 :
        linha = dados[i].split(";")
        x.append(int(linha[0]))
        y.append(int(linha[1]))

plt.plot(x, y, color="k", linestyle = "--")
plt.bar(x, y, color="#e5e5e5")
plt.title("Crescimento da População Brasileira de 1980-2016")
plt.xlabel("Ano")
plt.ylabel("População x100.000.000")
plt.show()

plt.savefig("populacaobrasileira.png", dpi=300)