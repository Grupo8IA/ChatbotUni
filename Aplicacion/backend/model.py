import torch
import re
import unicodedata
from io import open

MAX_LENGTH = 10 # Cantidad de palabras máxima por cada sentencia

class Voc:
    def __init__(self, name):
        self.name = name
        self.trimmed = False
        self.word2index = {"PAD": PAD_token , "SOS":SOS_token , "EOS":EOS_token }
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3  # Los 3 tokens inicializados SOS, EOS, PAD

    def agregarSentencia(self, sentence):
        for word in sentence.split(' '):
            self.agregarPalabra(word)

    def agregarPalabra(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    def indiceDeSentencia(self, sentencia):
        return [self.word2index[word] for word in sentencia.split(' ')] + [EOS_token]

    def sentenciaDeIndice(self, indice):
        return [self.index2word[idx] for idx in indice]

    # Remueve las palabras que se repiten menos de una cierta cantidad de veces
    def trim(self, min_count):
        if self.trimmed:
            return
        self.trimmed = True

        keep_words = []

        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        print('keep_words {} / {} = {:.4f}'.format(
            len(keep_words), len(self.word2index), len(keep_words) / len(self.word2index)
        ))

        # Reinicializamos los diccionarios
        self.word2index = {"PAD":PAD_token , "SOS":SOS_token , "EOS":EOS_token }
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3 # Los 3 tokens inicializados SOS, EOS, PAD

        for word in keep_words:
            self.agregarPalabra(word)

# Función que normalizará cada sentencia
def unicodeToAscii(s):
    return ''.join(
        # c for c in unicodedata.normalize('NFD', s) # Normalizará y eliminará las tildes y la ñ
        c for c in unicodedata.normalize('NFC', s) # Normalizará y mantiene las tildes y la ñ
        if unicodedata.category(c) != 'Mn'
    )

# Normalizamos cada sentencia
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip()) # Normalizamos y pasamos todas las letras a minúsculas
    # Pasamos cada sentencia a minúsculas, removemos los espacios y carácteres que no son letras excluyendo los números
    s = re.sub(r"([.¡!¿?])", r" \1", s)  # Mantenemos los signos interrogación y exclamación de apertura y cierre
    s = re.sub(r"[^A-zÁ-ú.¡!¿?0-9]+", r" ", s) # Mantenemos las tildes y números
    # s = re.sub(r"\¿", r"¿ ", s) # Agregamos un espacio a los signos de interrogación para que se cuente como una palabra
    # s = re.sub(r"\?", r" ?", s) # Agregamos un espacio a los signos de interrogación para que se cuente como una palabra
    # s = re.sub(r"\¡", r"¡ ", s) # Agregamos un espacio a los signos de exclamación para que se cuente como una palabra
    # s = re.sub(r"\!", r" !", s) # Agregamos un espacio a los signos de exclamación para que se cuente como una palabra
    # s = re.sub(r"\s+", r" ", s).strip() # Eliminamos los espacios demás
    # s = re.sub(r"\.", r"", s).strip() # Eliminamos los puntos

    # s = re.sub(r"[^A-z.¡!¿?0-9]+", r" ", s) # Elimina tildes
    s = re.sub(r"\.", r"", s)
    s = re.sub(r"\¿\s+", r"¿", s) # Elimina espacios alrededor del signo de interrogación
    s = re.sub(r"\s+\?", r"?", s) # Elimina espacios alrededor del signo de interrogación
    s = re.sub(r"\¡\s", r"¡", s) # Elimina espacios alrededor del signo de exclamación
    s = re.sub(r"\!\s", r"!", s) # Elimina espacios alrededor del signo de exclamación
    s = re.sub(r"\s+", r" ", s).strip() # Elimina los espacios demás
    return s


# Leemos las lineas del archivo y devolvemos los pares y un objeto Voc
def readVocs(datafile, corpus_name):
    print("Leyendo líneas...")
    # Leemos el archivo y devuelve una lista de líneas
    lines = open(datafile, encoding='utf-8').\
        read().strip().split('\n')
    # Dividimos cada linea en pares, normaliza normalizando cada sentencia
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]
    voc = Voc(corpus_name)
    # Devuelve el objeto vocabulario y los pares
    return voc, pairs

# Retorna True si ambas sentencias en el par tienen una cantidad de palabras menores que MAX_LENGTH
def filtrarPar(p):
    # Las sentencias de entrada, necesitamos un espacio para el token SOS
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGTH

# Filtra los pares usando la función filtrarPar
def filtrarPares(pairs):
    return [pair for pair in pairs if filtrarPar(pair)]

# Usando las funciones definidas arriba generamos el diccionario que mapea de palabras a índices
# devolverá el objeto voc y la lista de pares
def loadPrepareData(corpus_name, datafile, save_dir):
    print("Empieza la preparación de la data ...")
    voc, pairs = readVocs(datafile, corpus_name)
    print("Se leyó {!s} pares de sentencias".format(len(pairs)))
    pairs = filtrarPares(pairs)
    print("Filtrado {!s} pares de sentencias".format(len(pairs)))
    print("Contando las palabras...")

    for pair in pairs:
        # Agregamos cada sentencia al objeto Voc para hacer el mapeo
        voc.agregarSentencia(pair[0])
        voc.agregarSentencia(pair[1])
        
    print("Cantidad total de palabras:", voc.num_words)
    
    
    return voc, pairs

class Encoder(torch.nn.Module):
  def __init__(self, longitud_entrada, longitud_embedding=200, longitud_oculta=200, n_capas=2):
    super().__init__()
    # Inicializacion de la longitud del estado oculto
    self.longitud_oculta = longitud_oculta
    # Inicializacion del embedding
    self.embedding = torch.nn.Embedding(longitud_entrada, longitud_embedding)
    # Inicializacion de la red GRU
    self.gru = torch.nn.GRU(longitud_embedding, longitud_oculta, num_layers=n_capas, batch_first=True)

  # Definicion del forward, retorna la salida y el estado oculto
  def forward(self, oraciones_entrada):
    embedded = self.embedding(oraciones_entrada)
    salidas, oculta = self.gru(embedded)
    return salidas, oculta

class AtencionDecoder(torch.nn.Module):
  def __init__(self, longitud_entrada, longitud_embedding=200, longitud_oculta=200, n_layers=2, longitud_maxima=MAX_LENGTH):
    super().__init__()
    # Inicializacion del embedding
    self.embedding = torch.nn.Embedding(longitud_entrada, longitud_embedding)
    # Inicializacion de la red GRU
    self.gru = torch.nn.GRU(longitud_embedding, longitud_oculta, num_layers=n_layers, batch_first=True)
    # Define una transformacion lineal para la salida del decoder
    self.out = torch.nn.Linear(longitud_oculta, longitud_entrada)

    # Define la transformacion lineal para el calculo del vector de atencion
    self.atencion = torch.nn.Linear(longitud_oculta + longitud_embedding, longitud_maxima)
    # Define la transformacion lineal para combinar el vector de atencion con el estado oculto del encoder
    self.combinar_atencion = torch.nn.Linear(longitud_oculta * 2, longitud_oculta)

  # Definicion del forward, retorna la salida, el estado oculto, y los pesos del vector de pesos de atencion
  def forward(self, palabras_entrada, oculta, salidas_encoder):
    embedded = self.embedding(palabras_entrada)
    pesos_atencion = torch.nn.functional.softmax(self.atencion(torch.cat((embedded.squeeze(1), oculta[0]), 1)))
    atencion_aplicada = torch.bmm(pesos_atencion.unsqueeze(1), salidas_encoder)
    # Concatena el embedding con el vector de atencion
    salida = torch.cat((embedded.squeeze(1), atencion_aplicada.squeeze(1)), 1)
    salida = self.combinar_atencion(salida)
    salida = torch.nn.functional.relu(salida)
    salida, oculta = self.gru(salida.unsqueeze(1), oculta)
    salida = self.out(salida.squeeze(1))
    return salida, oculta, pesos_atencion

def main():
    save_dir = "./"
    datafile = "../../Data/all30.txt"
    corpus_name = "dataf_s2s"
    voc, pairs = loadPrepareData(corpus_name, datafile, save_dir)

    # Imprimimos una muestra de la data para verificar su estructura
    print("\npares:")

    for pair in pairs[:10]:
        print(pair)

    encoder = Encoder(longitud_entrada=voc.num_words)
    decoder = AtencionDecoder(longitud_entrada=voc.num_words)
    checkpoint = torch.load('checkpoint-512BS-30ML-18EP.pt')
    encoder.load_state_dict(checkpoint['encoder'])
    decoder.load_state_dict(checkpoint['decoder'])


    pass

if __name__ == '__main__':
    main()