import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd

from pathlib import Path
from collections import Counter

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class CTCLayer(layers.Layer):
    def __init__(self, name=None):
        super().__init__(name=name)
        self.loss_fn = keras.backend.ctc_batch_cost


runt = keras.models.load_model(r'C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\runt.h5',custom_objects={'CTCLayer': CTCLayer})

characters = ['2', '3', '4', '5', '6', '7', '8', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'm', 'n', 'p', 'r', 'w', 'x', 'y']

# Mapear caracteres a números enteros
char_to_num = layers.StringLookup(
    vocabulary=list(characters), mask_token=None
)

# Mapear enteros a los caracteres originales
num_to_char = layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
)

def encode_single_sample2(img):
    # Desired image dimensions
    img_width = 204
    img_height = 53
    # 2. Decode and convert to grayscale
    img = np.reshape(img,(53, 204,1))
    # 3. Convert to float32 in [0, 1] range
    img = tf.image.convert_image_dtype(img, tf.float32)
    # 4. Resize to the desired size
    img = tf.image.resize(img, [img_height, img_width])
    # 5. Transpose the image because we want the time
    # dimension to correspond to the width of the image.
    img = tf.transpose(img, perm=[1, 0, 2])
    return {"image": img}

def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:, :5]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text

prediction_model = keras.models.Model(runt.get_layer(name="image").input, runt.get_layer(name="dense2").output)

def prediction(img):
    pred_dataset=encode_single_sample2(img)
    batch_imagenes = pred_dataset["image"]

    size_img=1
    batch_imagenes = np.reshape(batch_imagenes,(size_img,204, 53, 1))

    prediccion = prediction_model.predict(batch_imagenes)
    pred_texts_vv = decode_batch_predictions(prediccion)

    return pred_texts_vv

def transform_to_df(lista):
    columns = ['placa','tipo_combustible','marca','modelo','chasis','cilindraje','linea','color','motor','vin','fecha_matricula','autoridad','nro_licencia',
               'tipo_servicio','estado_vehiculo','clase_vehiculo','numero_serie','tipo_carroceria','regrabacion_motor',
               'nro_regrabacion_motor','regrabacion_chasis','nro_regrabacion_chasis','regrabacion_serie','nro_regrabacion_serie',
               'regrabacion_vin','nro_regrabacion_vin','capacidad_pasajeros','capacidad_carga','capacidad_pasajeros_sentados',
               'soat','tecnomecanica','blindado','nivel_blindaje','fecha_blindaje','fecha_desblindaje','numero_resolucion',
               'fecha_expedicion','tipo_autorizacion','solicitudes']
    df = pd.DataFrame([lista],columns = columns)
    
    return df

################################### PATHS ##############################################################

placa_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div/div[1]/div[2]'
marca_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[1]/div[2]'
modelo_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[2]/div[2]'
chasis_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[4]/div[2]'
cilindraje_xpath ='/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[5]/div[2]'
linea_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[1]/div[4]'
color_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[2]/div[4]'
motor_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[3]/div[4]'
vin_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[4]/div[4]'
fecha_matricula_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[6]/div[4]'
autoridad_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[7]/div[2]'
tipo_combustible_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[6]/div[2]'
nro_licencia_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div/div[2]/div[2]'
tipo_servicio_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div/div[3]/div[2]'
estado_vehiculo_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div/div[2]/div[4]'
clase_vehiculo_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div/div[3]/div[4]'
numero_serie_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[3]/div[2]'
tipo_carroceria_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[5]/div[4]'
regrabacion_motor_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[9]/div[2]'
nro_regrabacion_motor_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[9]/div[4]'
regrabacion_chasis_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[10]/div[2]'
nro_regrabacion_chasis_xpath ='/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[10]/div[4]'
regrabacion_serie_xpath ='/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[11]/div[2]'
nro_regrabacion_serie_xpath ='/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[11]/div[4]'
regrabacion_vin_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[12]/div[2]'
nro_regrabacion_vin_xpath = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[6]/div[2]/div/div/div/div[12]/div[4]'

################################### PATHS ##############################################################
