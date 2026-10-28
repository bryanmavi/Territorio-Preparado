import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import numpy as np
from fastapi.testclient import TestClient
from servidor.ia import app as module
from servidor.ia.engines import mask_to_geojson, Unavailable

class AIIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = patch.object(module, 'DB', Path(self.temp.name)/'messages.sqlite')
        self.db.start()
        self.client = TestClient(module.app)
    def tearDown(self):
        self.client.close()
        self.db.stop()
        self.temp.cleanup()
    def test_original_persisted_and_websocket_event(self):
        predicted={'scores':[{'label':'LABEL_0','score':.9}], 'priority':'human_review'}
        with patch.object(module.sos,'predict',return_value=predicted), self.client.websocket_connect('/api/v1/messages/ws') as ws:
            result=self.client.post('/api/v1/analyze-text',json={'text':'We need water','language':'en'})
            self.assertEqual(result.status_code,200)
            self.assertEqual(ws.receive_json()['id'],result.json()['id'])
        self.assertEqual(self.client.get('/api/v1/messages').json()[0]['original_text'],'We need water')
    def test_spanish_translation_failure_does_not_store(self):
        with patch.dict(os.environ,{'DEEPL_AUTH_KEY':'', 'TP_TRANSLATION_MODEL':'/missing/tp-model'}):
            self.assertEqual(self.client.post('/api/v1/analyze-text',json={'text':'Necesito ayuda','language':'es'}).status_code,503)
        self.assertEqual(self.client.get('/api/v1/messages').json(),[])
    def test_spanish_original_survives_local_translation(self):
        with patch.object(module, 'english', return_value=('We need water', True)), patch.object(module.sos, 'predict', return_value={'priority':'human_review','scores':[]}):
            result=self.client.post('/api/v1/analyze-text',json={'text':'Necesitamos agua','language':'es'})
        self.assertEqual(result.status_code,200)
        self.assertEqual(result.json()['original_text'],'Necesitamos agua')
        self.assertEqual(result.json()['analyzed_text'],'We need water')
    def test_damage_upload_adapter(self):
        files={'pre':('pre.png',b'pre','image/png'),'post':('post.png',b'post','image/png')}
        output={'type':'FeatureCollection','features':[]}
        with patch.object(module.damage,'predict',return_value=output) as engine:
            result=self.client.post('/api/v1/analyze-damage',files=files,data={'bounds':'[-77,3,-76,4]'})
            self.assertEqual(result.status_code,200)
            engine.assert_called_once_with(b'pre',b'post',[-77,3,-76,4])
    def test_cross_origin_rejected(self):
        self.assertEqual(self.client.post('/api/v1/analyze-text',headers={'Origin':'https://unrelated.example'},json={'text':'Help','language':'en'}).status_code,403)
    def test_missing_model_no_fake_inference(self):
        with patch.object(module.sos,'predict',side_effect=Unavailable('missing weights')):
            self.assertEqual(self.client.post('/api/v1/analyze-text',json={'text':'Help me','language':'en'}).status_code,503)
    def test_validation(self):
        for body in [{'text':'   ','language':'en'}, {'text':'help','language':'fr'}]:
            self.assertEqual(self.client.post('/api/v1/analyze-text',json=body).status_code,422)
        files={'pre':('pre.png',b'bad','image/png'),'post':('post.png',b'bad','image/png')}
        self.assertEqual(self.client.post('/api/v1/analyze-damage',files=files,data={'bounds':'[1,2,0,3]'}).status_code,422)
    def test_georeference_and_classes(self):
        output=mask_to_geojson(np.array([[0,1],[3,4]],dtype='uint8'),[-77,3,-76,4])
        self.assertEqual(len(output['features']),3)
        destroyed=next(f for f in output['features'] if f['properties']['damage_class']==4)
        ring=destroyed['geometry']['coordinates'][0]
        self.assertIn((-76.5,3.5),ring)
        self.assertIn((-76.,3.),ring)
    def test_reject_unknown_mask_classes(self):
        with self.assertRaises(Unavailable):mask_to_geojson(np.array([[8]]),[-77,3,-76,4])
    def test_static_ui(self):
        self.assertEqual(self.client.get('/disaster-ai.html').status_code,200)
        self.assertEqual(self.client.post('/api/demo/reconcile').json()['unique_people'],104)

if __name__=='__main__':unittest.main()
