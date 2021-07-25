
# Preprocesamiento de la data
### Proceso de preprocesamiento

En estos cuadernos describimos los procesos que hemos seguido para limpiar y procesar la data para obtener texto con el formato que necesitamos para entrenar nuestro modelo.

Para la preparación de la data de entrenamiento necesitamos obtener pares de oraciones por ejemplo una frase en inglés y una frase en español que representa su tradución nos serviría para entrenar un chatbot que traduce frases del inglés al español.

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)

En la imágen anterior se muestra una data antes de ser procesada, ésta data serviría para hacer un traductor del inglés al español.

Como nuestro objetivo es hacer un chatbot nosotros necesitamos pares de oraciones con una pregunta y respuesta, con pregunta nos referimos al usuario activo en la conversación y la respuesta es la manera en que esperamos que se responda a la conversación.

El proceso completo para procesar los datos para el modelo de entrenamiento es:

* Leer el archivo de texto y limpiarlo, el objetivo es que queden solo líneas de pares de oraciones.
* Dividir cada línea en pares de oraciones y guardarlo en otro archivo, cada par deben estar separados por un tab (\t) y añadir al final un salto de línea (\n).

https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html

Al final del procesamiento obtendremos un archivo de líneas de texto donde cada línea tiene el siguiente formato: **sentencia 1\tsentencia 2\n**


