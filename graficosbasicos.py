import matplotlib.pyplot as plt

#Grupos de dados que serão mostrados nos gráficos
x1 = [1,3,5,7,9]
y1 = [2,3,7,1,0]
z1 = [120, 150, 200, 80, 50]
x2 = [2,4,6,8,10]
y2 = [5,1,3,7,4]

#Legendas
titulo = "Gráfico de Barras"
eixox = "Eixo X"
eixoy = "Eixo Y"
plt.title(titulo)
plt.xlabel(eixox)
plt.ylabel(eixoy)

#Gráfico de linhas
def grafico_linhas(x,y):
    plt.plot(x, y)

#Gráfico de colunas
def grafico_colunas(x,y,x2,y2):
    plt.bar(x,y, label = "Grupo 1")
    plt.bar(x2,y2, label = "Grupo 2")
    plt.legend()

#Gráfico de dispersão ligado por linhas
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
def grafico_dispersao(x,y,z):
    plt.scatter(x, y, label="Meus pontos", color="k", marker="*", s=z)
    plt.plot(x, y, color="k", linestyle=":")

#Salvar figuras
def salvar_figura(nomearq):
    plt.savefig(nomearq, dpi=300)

#grafico_linhas(x1,y1)
#grafico_colunas(x1,y1,x2,y2)
grafico_dispersao(x1,y1,z1)
#plt.show()

nomearquivo = "teste.png"
salvar_figura(nomearquivo)