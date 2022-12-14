# -*- coding: utf-8 -*-

"""
  Python ile IoThook REST Api Testi

  Kod çalıştırıldığında APIKEY ile doğrulama gerçekleştirilir.
  Cihaz api_key ile ilgili veriler IoThook a post edilir.

  Bu ornek IotHook servisine veri almak/gondermek icin baslangic seviyesinde
  testlerin yapilmasini amaclamaktadir.

  20 Eylul 2017
  Güncelleme : 19 Agustos 2019
  Güncelleme : 21 Ekim 2021
  Sahin MERSIN

  Daha fazlasi icin

  http://www.iothook.com
  ve
  https://github.com/electrocoder/iotHook

  sitelerine gidiniz.

  Sorular ve destek talepleri icin
  https://github.com/electrocoder/iotHook/issues
  sayfasindan veya Meşe Bilişim den yardım alabilirsiniz.

  Yayin : http://mesebilisim.com

  Licensed under the Apache License, Version 2.0 (the "License").
  You may not use this file except in compliance with the License.
  A copy of the License is located at

  http://www.apache.org/licenses/
"""

import json
import pprint
import random
import time

import requests

headers = {'Content-type': 'application/json'}

url = 'http://localhost:8000/api/datas/'

for i in range(100):
    data = {
        'api_key': '7bf59e593a524c16bbdca0465c4b19194ad797c5',
        'field_1': random.randint(1, 10),
        'field_2': round(random.uniform(0.0,10.0), 2),
    }

    data_json = json.dumps(data)

    response = requests.post(url, data=data_json, headers=headers)
    pprint.pprint(response.json())
    time.sleep(5)
