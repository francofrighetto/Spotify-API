import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import spotipy.util as util
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv("../.env"))

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')


token = util.prompt_for_user_token(
    username=username,
    scope='playlist-modify-public', 
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=os.getenv('REDIRECT_URL')
)

sp = spotipy.Spotify(auth=token)


playlist_link = os.getenv('URL_PRUEBA')
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

vec=[]
dic={}


# guardo en el vector el nombre de cancion y cantante
# en el diccionario guardo las uri de las canciones
for track in sp.playlist_tracks(playlist_URI)["items"]: 
    #Track name
    track_uri = track["track"]["uri"]
    track_name = track["track"]["name"]
        
    #Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]

    
    vec.append(track_name +" "+ artist_name)
    dic[track_name +" "+ artist_name]=track_uri


# defino a la busqueda binaria
def busqueda_binaria(lista, x):

    izq = 0 # izq guarda el índice inicio del segmento
    der = len(lista) -1 # der guarda el índice fin del segmento

    # un segmento es vacío cuando izq > der:
    while izq <= der or izq==1:
        # el punto medio del segmento
        medio = int((izq+der)/2)

       # print("DEBUG:", "izq:", izq, "der:", der, "medio:", medio)

        # si el medio es igual al valor buscado, lo devuelve
        if lista[medio] == x:
            return medio

        # si el valor del punto medio es mayor que x, sigue buscando
        # en el segmento de la izquierda: [izq, medio-1], descartando la
        # derecha
        elif lista[medio] > x:
            der = medio-1

        # sino, sigue buscando en el segmento de la derecha:
        # [medio+1, der], descartando la izquierda
        else:
            izq = medio+1
        # si no salió del ciclo, vuelve a iterar con el nuevo segmento

    # salió del ciclo de manera no exitosa: el valor no fue encontrado
    return -1

# paso el vec a vec2 para poder ordenarlo y aplicar busqueda binaria (debe estar ordenado)
# vec = vector original como aparece en spotify
# vec2 = vec ordenado alfabeticamente
vec2=[]
for i in range(len(vec)):
    vec2.append(vec[i])

vec2.sort()
vec3=[]

# si la busqueda binaria me devuelve un valor que no es el de la posicion, significa que esa cancion ya esta antes,
# osea esta repetido. Guarda los repetidos vec3
for i in range(len(vec2)):
    if i!=busqueda_binaria(vec2,vec2[i]):
        vec3.append(vec2[i])

if len(vec3)>0:
    print("Canciones que estan repetidas")
    for i in range(len(vec3)):
        print("*  "+vec3[i])
    verificador_borrar = input("¿Quiere borrarlas a todas? (s/n): ")

    if verificador_borrar == "s":
        # itera sobre vec3 que es donde estan los repetidos
        # en cada iteracion busca donde esta la cancion en la lista original
        # luego se borra de la lista esa cancion y tambien la borro de vec para que siga consistente las posiciones
        # siempre borra la cancion repetida que este mas arriba
        for i in range(len(vec3)):
            borrar=[]
            # borrar tiene la uri y la posicion en la lista
            # ejemplo de como se ve el parametro borrar
            # [{“uri”:”4iV5W9uYEdYUVa79Axb7Rh”, “positions”:[2]}, {“uri”:”1301WleyT98MSxVHPZCA6M”, “positions”:[7]}]
            borrar.append({"uri":dic[vec3[i]],"positions":[vec.index(vec3[i])]})
            vec.remove(vec3[i])
            # llama a la funcion que lo borra
            sp.playlist_remove_specific_occurrences_of_items(playlist_URI,borrar)
