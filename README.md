# ChatbotUni

## Integrantes

Integrante | Correo
------------ | -------------
Rosa Irene Limachi Paucar | <rlimachip@uni.pe>
Carlos Gabriel Felix Romo | <cfelixr@uni.pe>
Cristhian Elian Cruz Coro | <cecruzc@uni.pe>
Juan Carlos Cotrina Muñoz | <juan.cotrina.m@uni.pe>
Freider Wilmer Achic Cuenca | <fachicc@uni.pe>

## Datos usados para el entrenamiento

* ESLORA: Corpus para el estudio del español oral <http://eslora.usc.es>, versión 2.0 de septiembre de 2020, ISSN: 2444-1430.

* DAILYD  :  Un  conjunto  de  datos  de  dialogo  de multiples. 

* METALW : Un conjunto de datos de di ́alogos mul-tidominio para la rapida adaptacion de modelos deconversaci ́on.

* Traducción directa de DAILYD y METALW.

<https://github.com/CHANEL-JSALT-2020/dataset>

* TranslateAlignRetrieve:  Un  conjunto  de  datos  que pertenece  a  un  proyecto  en  la  cual  se  aplica  el metodo  TAR  (Translate-Align-Retrieve)  diseñado  eimplementado  para  la  traduccion  automatica  del Stanford  Question  Answering  Dataset  (SQuAD)  al español.  Consiste  en  un  objeto  JSON  que  contiene preguntas y respuestas de cultura general.

<https://raw.githubusercontent.com/ccasimiro88/TranslateAlignRetrieve/master/SQuAD-es-v2.0/dev-v2.0-es_small.json>

## Para correr la aplicacion en local

* (FLASK) En ./Aplicacion/backend/

Crear venv. Instalar dependencias.

`pip install -r requirements.txt`

Iniciar backend.

`flask run`

* (REACT) En ./Aplicacion/frontend/

Instalar dependencias.

`npm install`

Iniciar frontend.

`npm start`

## Descargar el checkpoint etapa 04, y ubicarlo en ./Aplicacion/backend/static/

* MERGE_HEAD

<https://drive.google.com/drive/folders/1Xv_lK_sReD_T4N-65tRv7nXuHgXBgf8n?usp=sharing>

## Referencias 

* Pytorch - CHATBOT TUTORIAL. Author: Matthew Inkawhich

<https://pytorch.org/tutorials/beginner/chatbot_tutorial.html>

* Proyecto TranslateAlignRetrieve.

<https://github.com/ccasimiro88/TranslateAlignRetrieve>