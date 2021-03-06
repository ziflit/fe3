import re

#Constantes N y K: N es la cantidad de dimensiones, K la cantidad de NN a considerar.
N = 550
K = 5

def clean(s):
    """
        Limpia el string s.
        Devuelve mas palabras que las que reporta wordcount. Revisar
    """
    return " ".join(re.findall(r'\w+', s,flags = re.UNICODE | re.LOCALE)).lower()


def get_data_tsv(loc_dataset):
    #Devuelve de a 1 linea.
    for e, line in enumerate(open(loc_dataset,"rb")):
        if e > 0:
            r = line.strip().split("\t")
            id = r[0]
            
            #Limpia la review, pero si es una de test falla, he ahi el try.
            try:
                r[2] = clean(r[2])
            except:
                r[1] = clean(r[1])
            features = []
            if len(r) == 3: #train set
                for word in r[2].split(): 
                    posicion = hash(word)%N
                    if posicion not in features:
                        features.append(posicion)
                label = int(r[1])
            else: #test set
				for word in r[1].split(): 
					posicion = hash(word)%N
					if posicion not in features:
						features.append(posicion)
                        
				label = 1
            #Saque los bigram, no tenia sentido dejarlos, se busca eficiencia y pocas dimensiones.
            yield label, id, features


def distancia(v, w):            
    """
    Calcula distancia entre dos vectores V y W, vectores dispersos que representan a otros 
    P y Q de dimension N.
    """
    i = j = k = suma = 0

    while (i < N):
        p = q = 0
        if ( ( j < len(v) ) and ( v[j] == i) ):
            p = 1
            j+=1
        if ( ( k < len(w) ) and ( w[k] == i) ):
            q = 1
            k+=1
        suma += (p - q) ** 2
        i+=1

    return suma


#Para el sort
def getKey(item):
    return item[0]    


def calcularVecinos(matrizEntrenamiento, reviewPrueba):
    vecinos = [(N+1, 1)] * K
    for tuplaEntrenamiento in matrizEntrenamiento:
        v = tuplaEntrenamiento[2]
        distanciaEntreVectores = distancia(v, reviewPrueba)
        if ( distanciaEntreVectores < vecinos[K-1][0]): 
            vecinos[K-1] = (distanciaEntreVectores, tuplaEntrenamiento[1] )
            vecinos = sorted(vecinos, key=getKey)
    return vecinos       

def calcularProbabilidadPositiva(vecinos):
    """
    Dado un vector de vecinos decide la probabilidad de que sea positiva calculando de la forma
    vecinosPositivos / vecinosTotales
    """
    vecinosTotales = K
    vecinosPositivos = 0.0
    for vec in vecinos:
        if ( vec[1] == 1): vecinosPositivos +=1
    return (vecinosPositivos * 1.0) / (vecinosTotales * 1.0)
    

def cargarMatriz(archivo):
    m = []
    for i, (label, id, features) in enumerate( get_data_tsv(archivo) ):
        m.append((id, label, sorted(features)))
    return m


def outputToCSV(entrenamiento, prueba):
    """
    Genera el output de kaggle
    de la forma:
    id  sentiment
    """
    with open("resultadofe3.csv", "wb") as outfile:
        outfile.write('"id","sentiment"'+"\n")
        for p in prueba:
            vecinos = calcularVecinos(entrenamiento, p[2])
            probabilidad = calcularProbabilidadPositiva(vecinos)
            outfile.write("%s,%s\n"%(p[0],probabilidad))
if __name__ == "__main__":
    """
        dimensiones tomadas: 550 en un principio (TODO: Ajustar el numero.)
       -Tomo el archivo:
           -por cada review entreno un vector de features de dim N, N entre (100, 1000). 
           -Tengo una matriz de N x 25000 donde cada columna corresponde a un review
                y sus filas son las palabras que se "activaron".
       -Tomo el archivo de pruebas y por cada review que tengo
    """
    entrenamiento = cargarMatriz("labeledTrainData.tsv") # matriz con reviews de entrenamiento.
    # print entrenamiento[0]
    # print len(entrenamiento[0][2])
    # carga matriz con reviews para prueba. Label sobra, pero es mas facil que reescribir el metodo. Se reescribe label con el resultado buscado.
    prueba = cargarMatriz("testData.tsv") 
    # print prueba[0]
    # print len(prueba[0][2])

    outputToCSV(entrenamiento,prueba)