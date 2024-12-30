# -*- coding: utf-8 -*-
"""
Created on Tue May 23 08:21:59 2023

@author: davboter
"""

import sys
sys.path.append(r'C:\Users\rcDMZConfig\Desktop\RUNT\RUNT')


from functions import *
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException,TimeoutException, WebDriverException
from urllib3.exceptions import MaxRetryError, NewConnectionError
import matplotlib.pyplot as plt
import time
import warnings
import logging
import win32com.client as win32
import pandas as pd
import tensorflow

warnings.filterwarnings("ignore")

# Configurar el logger
logging.basicConfig(filename=r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Automatizacion Runt\Historico\consulta_runt.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def Validacion_atributos_runt(atributo,xpath):
    # Placa
    intentos = 0
    placa = None

    while intentos < 3:
        try:
            atributo = driver.find_element('xpath', xpath)
            break  # Si se encuentra el elemento, salir del ciclo interno
        except NoSuchElementException:
            intentos += 1
            if intentos == 3:
                print("No se pudo encontrar el elemento después de 3 intentos.")
                break  # Si se alcanza el máximo de intentos, salir del ciclo interno
            else:
                time.sleep(3)  # Esperar 3 segundos antes de realizar el siguiente intento

    if atributo is not None:
        data.append(atributo.text)
    else:
        print(f'No se encontro el elemento: {placa}, reiniciando la busqueda.')
        captcha_fallo = True


placas = pd.read_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\placas.xlsx") 

placas = list(placas['placa'])
nit = '890903938'                   # Adicionar al archivo donde se encuentran las constantes

for placa in placas:
    df_existente = pd.read_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\runt.xlsx") 
    df_existente_error = pd.read_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\error.xlsx")
    captcha_fallo = True
    while captcha_fallo == True:
        try:
            data = []
            data_2 = []
            # Driver para iniciar WebScraping
            options = Options() 
            DRIVER_PATH = r"C:\WebScraping\chromedriver.exe"
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument("headless")
            options.add_argument("disable-gpu")
            options.add_argument("no-sandbox")
            options.add_argument("--incognito")
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            driver.get('https://www.runt.com.co/consultaCiudadana/#/consultaVehiculo')


            start_time = time.time()
            logging.info(f'Inicio de la consulta para la placa {placa}')
            print(f'Ha iniciado la busqueda para la placa: {placa}')

                
            time.sleep(8)

            # Ingresar placa
            searchbox = driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/div/div/form/div[1]/div[1]/input')
            searchbox.send_keys(placa)

            # Combo Box
            ddelement= Select(driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/div/div/form/div[4]/div/select'))
            ddelement.select_by_index(3)

            # Ingresar nit
            searchbox = driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/div/div/form/div[5]/div[1]/input')
            searchbox.send_keys(nit)

            # Captcha
            captcha = driver.find_element("xpath",'//*[@id="imgCaptcha"]')
            captcha.screenshot("captcha.png")

            # Limpieza
            img = plt.imread("captcha.png")
            imagen=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            image = cv2.normalize(imagen, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)
            # Binarizacion
            thresh=cv2.inRange(image,50,255);
            # Matriz de transformacion
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,4))
            # Dilatacion de pixeles blancos
            imagenes = cv2.dilate(thresh, kernel,iterations=1)
            # Prediccion
            text_captcha = prediction(imagenes)[0]

            time.sleep(2)
        
            # Enviamos la prediccion del captcha
            sendcaptcha = driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/div/div/form/div[8]/div[1]/div[2]/input')
            sendcaptcha.send_keys(text_captcha.strip())
            sendcaptcha.send_keys(Keys.ENTER)
            
            # Esperamos a que cargue la pagina
            time.sleep(1)
            
            # Limpieza mensaje
            
            captcha_fallo = driver.find_element(By.ID,'dlgConsulta').text.strip()
            captcha_fallo = captcha_fallo.replace('Resultado Consulta','')
            captcha_fallo = captcha_fallo.replace('Aceptar','')
            captcha_fallo = captcha_fallo.replace('×','')
            captcha_fallo = captcha_fallo.replace('\n','')

            if captcha_fallo == 'Por favor verifique el valor ingresado en los campos resaltados en rojo.':
                captcha_fallo = True
                logging.error(f'La consulta para la placa {placa} ha fallado: Por favor verifique el valor ingresado en los campos resaltados en rojo.')
                driver.quit()
            elif captcha_fallo == 'La imagen no coincide con el valor ingresado, por favor verifiquela e intente nuevamente.':
                captcha_fallo = True
                logging.error(f'La consulta para la placa {placa} ha fallado: La imagen no coincide con el valor ingresado, por favor verifiquela e intente nuevamente.')
                driver.quit()
            elif captcha_fallo == 'Señor Usuario, para el vehículo consultado no hay información registrada en el sistema RUNT.':
                data_2.append([placa,nit,captcha_fallo])
                df = pd.DataFrame(data_2)
                df_total = pd.concat([df_existente_error, df], ignore_index=True)
                df_total.to_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\error.xlsx",index=False)
                captcha_fallo = False
                logging.error(f'La consulta para la placa {placa} ha fallado: Señor Usuario, para el vehículo consultado no hay información registrada en el sistema RUNT.')
                driver.quit()
            elif captcha_fallo == 'Los datos registrados no corresponden con los propietarios activos para el vehículo consultado.':
                data_2.append([placa,nit,captcha_fallo])
                df = pd.DataFrame(data_2)
                df_total = pd.concat([df_existente_error, df], ignore_index=True)
                df_total.to_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\error.xlsx",index=False)
                captcha_fallo = False
                logging.info(f'Los datos registrados para la placa {placa} no corresponden con los propietarios activos para el vehículo consultado.')
                driver.quit()
            else:
                print('El captcha se envio correctamente')
                time.sleep(3)

                # Extraccion de los atributos generales del vehiculo.

                Validacion_atributos_runt('placa',placa_xpath)
                Validacion_atributos_runt('tipo_combustible',tipo_combustible_xpath)
                Validacion_atributos_runt('marca',marca_xpath)
                Validacion_atributos_runt('modelo',modelo_xpath)
                Validacion_atributos_runt('chasis',chasis_xpath)
                Validacion_atributos_runt('cilindraje',cilindraje_xpath)
                Validacion_atributos_runt('linea',linea_xpath)
                Validacion_atributos_runt('color',color_xpath)
                Validacion_atributos_runt('motor',motor_xpath)
                Validacion_atributos_runt('vin',vin_xpath)
                Validacion_atributos_runt('fecha_matricula',fecha_matricula_xpath)
                Validacion_atributos_runt('autoridad',autoridad_xpath)
                Validacion_atributos_runt('nro_licencia',nro_licencia_xpath)
                Validacion_atributos_runt('tipo_servicio',tipo_servicio_xpath)
                Validacion_atributos_runt('estado_vehiculo',estado_vehiculo_xpath)
                Validacion_atributos_runt('clase_vehiculo',clase_vehiculo_xpath)
                Validacion_atributos_runt('numero_serie',numero_serie_xpath)
                Validacion_atributos_runt('tipo_carroceria',tipo_carroceria_xpath)
                Validacion_atributos_runt('regrabacion_motor',regrabacion_motor_xpath)
                Validacion_atributos_runt('nro_regrabacion_motor',nro_regrabacion_motor_xpath)
                Validacion_atributos_runt('regrabacion_chasis',regrabacion_chasis_xpath)
                Validacion_atributos_runt('nro_regrabacion_chasis',nro_regrabacion_chasis_xpath)
                Validacion_atributos_runt('regrabacion_serie',regrabacion_serie_xpath)
                Validacion_atributos_runt('nro_regrabacion_serie',nro_regrabacion_serie_xpath)
                Validacion_atributos_runt('regrabacion_vin',regrabacion_vin_xpath)
                Validacion_atributos_runt('nro_regrabacion_vin',nro_regrabacion_vin_xpath)
                
                # Extraccion de datos técnicos
                elemento_objetivo = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]')
                driver.execute_script("arguments[0].scrollIntoView();", elemento_objetivo)      

                time.sleep(1)   

                driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]').click() 

                time.sleep(1)

                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]')
                                                            
                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        pass
                except NoSuchElementException:
                    data.append('')

                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]/div/div/div/div[2]/div[1]/div[2]')
                                                            
                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        pass
                except NoSuchElementException:
                    data.append('')

                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]/div/div/div/div[2]/div[2]/div[4]')

                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        data.append('')
                except NoSuchElementException:
                    data.append('')
      
                # Extraccion del soat
                elemento_objetivo = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[5]/div[1]')
                driver.execute_script("arguments[0].scrollIntoView();", elemento_objetivo)

                time.sleep(1)

                driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[5]/div[1]').click()

                time.sleep(1)

                for tr in driver.find_element(By.ID,'pnlPolizaSoatNacional').find_elements(By.XPATH,'.//tr'):
                    row = [item.text for item in tr.find_elements(By.XPATH,'.//td')]
                    if len(row) > 0:
                        data.append(row)
                        break
                

                driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[7]/div[1]/h4/a').click()

                time.sleep(1)

                found_data = []  # Variable para almacenar los datos encontrados en la primera fila

                for tr in driver.find_element(By.ID,'pnlRevisionTecnicoMecanicaNacional').find_elements(By.XPATH,'.//tr'):
                    row = [item.text for item in tr.find_elements(By.XPATH,'.//td')]
                    if len(row) > 0:
                        row.pop()
                        found_data = row  # Almacenar los datos en la variable found_data
                        break

                if not found_data:
                    found_data = ['NO SE ENCONTRO INFORMACION REGISTRADA EN EL RUNT']

                # Añadir found_data a la lista de datos
                data.append(found_data)

                 # Extraccion del blindaje
                elemento_objetivo = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[1]')
                driver.execute_script("arguments[0].scrollIntoView();", elemento_objetivo)

                time.sleep(1)
                driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[1]').click()
                time.sleep(1)
                
                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[2]/div/div/div/div[1]/div[2]')
                                                            
                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        pass
                except NoSuchElementException:
                    data.append('')

                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[2]/div/div/div/div[1]/div[4]')

                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        data.append('')
                except NoSuchElementException:
                    data.append('')


                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[2]/div/div/div/div[2]/div[2]')

                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        data.append('')
                except NoSuchElementException:
                    data.append('')
                
                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[2]/div/div/div/div[2]/div[4]')

                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        data.append('')
                except NoSuchElementException:
                    data.append('')

                try:

                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[2]/div/div/div/div[3]/div[1]/div[2]')

                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        data.append('')
                except NoSuchElementException:
                    data.append('')

                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[2]/div/div/div/div[3]/div[1]/div[4]')

                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        data.append('')
                except NoSuchElementException:
                    data.append('')

                try:
                    atributo = driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[10]/div[2]/div/div/div/div[3]/div[2]/div[2]')
    
                    if atributo is not None:
                        data.append(atributo.text)
                    else:
                        data.append('')
                except NoSuchElementException:
                    data.append('')

                #Extracción solicitudes de traspaso
                elemento_objetivo = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[9]/div[1]')
                driver.execute_script("arguments[0].scrollIntoView();", elemento_objetivo)

                time.sleep(1)

                driver.find_element('xpath','/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[9]/div[1]').click()

                time.sleep(1)

                traspaso_data = []  # Variable para almacenar los datos de traspaso

                for tr in driver.find_element(By.ID, 'pnlInformacionSolicitud').find_elements(By.XPATH, './/tr'):
                    row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                    if len(row) > 0 and 'traspaso' in ' '.join(row).lower():
                        traspaso_data = row
                        break


                # Verificar si hay información de traspaso
                if traspaso_data:
                    data.append(traspaso_data)
                else:
                    data.append(['SIN SOLICITUDES DE TRASPASO REGISTRADAS EN EL RUNT'])

                time.sleep(1)

   
                df = transform_to_df(data)
                df_total = pd.concat([df_existente, df], ignore_index=True)


                df_total.to_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\runt.xlsx", index=False)

                # La busqueda de esta placa finalizo correctamente
                captcha_fallo = False
                driver.quit()
                elapsed_time = time.time() - start_time
                logging.info(f'Finalizo la busqueda para la placa {placa}')
                logging.info(f'Tiempo transcurrido: {elapsed_time} segundos')
                print(f"Tiempo transcurrido: {elapsed_time} segundos")
        except (NoSuchElementException, ElementNotInteractableException, MaxRetryError, NewConnectionError,AssertionError,ValueError,TimeoutException, WebDriverException) as e:
                # Se produjo un error, reiniciar el ciclo while
                logging.info(f'Se ha producido una excepción: {str(e)}')
                print(f"Se produjo un error: {str(e)}")
                print("Reiniciando la búsqueda...")
                captcha_fallo = True
                driver.quit()

    df_final = pd.read_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\runt.xlsx")
