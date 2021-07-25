import json
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import pandas as pd
from sklearn import preprocessing
from sklearn import cluster
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors

conn= psycopg2.connect(database="delati", user="modulo4", password="modulo4", host="128.199.1.222", port="5432")
cursor=conn.cursor()
sql="select distinct o.htitulo_cat, o.htitulo from webscraping w inner join oferta o on (w.id_webscraping=o.id_webscraping) where o.id_estado is null order by 1,2 limit 500;"

def load_data():
    cursor.execute(sql)
    result=cursor.fetchall()
    return result

def init():
    data = load_data()
    json_result = json.dumps(data)
    return json_result


df = pd.read_sql(sql, con = conn)
#print(df)
#df.shape
#DBSCAN_data_scaler = StandardScaler().fit(data)
#data = DBSCAN_data_scaler.transform(data)


dups = df.groupby(['htitulo_cat']).count()
#print(dups)
dups.shape

def transform_data():
    label_encoder = preprocessing.LabelEncoder()
    transformed_data = df.apply(label_encoder.fit_transform)
    #print(transformed_data)
    X=transformed_data.iloc[:,[0,1]].values
    #print(X)
    return X

def transform():
    label_encoder = preprocessing.LabelEncoder()
    transformed_data = df.apply(label_encoder.fit_transform)
    #print(transformed_data)
    X=transformed_data.iloc[:,[0,1]].values
    #print(X)
    b=[]
    for item in X:
        b.append(str(item))
        print(b)
    
    result = json.dumps(b)
    return result

def metodo_codo():
    z=transform_data()
    # Usamos vecinos más cercanos para calcular la distancia entre puntos.
    # calcular distancias 
    neigh=NearestNeighbors(n_neighbors=2)
    distance=neigh.fit(z)
    # índices y valores de distancia
    distances,indices=distance.kneighbors(z)
    # Ahora ordenando el orden creciente de distancia
    sorting_distances=np.sort(distances,axis=0)
    # distancias ordenadas
    sorted_distances=sorting_distances[:,1]
    return json.dumps(list(sorted_distances))

#grafico entre distancia vs épsilon
#plt.plot(sorted_distances)
#plt.xlabel('Distancia')
#plt.ylabel('Epsilon')
#plt.show()

def dbscan_model():
    # inicializamos DBSCAN
    clustering_model=DBSCAN(eps=4,min_samples=4)
    # ajustamos el modelo a transform_data
    clustering_model.fit(transform_data())
    #print(clustering_model)
    # prediccion por DBSCAN
    predicted_labels=clustering_model.labels_
    #print(predicted_labels)
    dat = []
    for it in predicted_labels:
        dat.append(int(it))

    res = json.dumps(dat)

    cluster=pd.read_json(res)

    absisa=[]
    ordenada=[]
    for item in transform_data():
        absisa.append(int(item[0]))
        ordenada.append(int(item[1]))
        #  b.append(" ".join(str(item)))

    resA = json.dumps(absisa)
    resO = json.dumps(ordenada)

    a=pd.read_json(resA)
    o = pd.read_json(resO)

    df['cluster']=cluster
    df['absisas']=a
    df['ordenadas']=o

    R = df.to_json(orient="records")
    return R
# visualzing clusters
#plt.scatter(X[:,0], X[:,1],c=predicted_labels, cmap='Paired')
#plt.xlabel('Categoria')
#plt.ylabel('Datos')
#plt.title("DBSCAN")
#plt.show()

