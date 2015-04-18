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
                features = [(hash(f)%N) for f in r[1].split()]
                label = 1
            #Saque los bigram, no tenia sentido dejarlos, se busca eficiencia y pocas dimensiones.
            yield label, id, features
def distance(v, w, N):
    """
    Calcula distancia entre dos vectores V y W, vectores dispersos que representan a otros 
    P y Q de dimension N.
    """
def cargarMatriz(archivo):
    m = []
    for i, (label, id, features) in enumerate( get_data_tsv(archivo) ):
        m.append((id, label, sorted(features)))
    return m

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
    print entrenamiento[0]
    print len(entrenamiento[0][2])
    # carga matriz con reviews para prueba. Label sobra, pero es mas facil que reescribir el metodo. Se reescribe label con el resultado buscado.
    prueba = cargarMatriz("testData.tsv") 