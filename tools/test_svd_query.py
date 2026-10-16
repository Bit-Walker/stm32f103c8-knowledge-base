import unittest,tempfile,pathlib,subprocess,sys,json,os
import svd_query as s
class Tests(unittest.TestCase):
 def load(self,text,names=['P']):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'x.svd';p.write_bytes(text.encode());return s.model(p,names)
 def test_inheritance(self):
  m=self.load('<device><name>D</name><size>32</size><resetValue>0</resetValue><peripherals><peripheral><name>P</name><baseAddress>0x4000</baseAddress><registers><register><name>R</name><addressOffset>4</addressOffset><fields><field><name>F</name><bitRange>[7:4]</bitRange></field></fields></register></registers></peripheral></peripherals></device>')
  r=m['peripherals']['P']['registers']['R'];self.assertEqual(r['size']['value'],32);self.assertEqual(r['address'],0x4004);self.assertEqual(r['fields']['F']['bitWidth'],4);self.assertIsNone(r['readAction'])
 def test_no_dtd(self):
  with self.assertRaises(ValueError):self.load('<!DOCTYPE device [<!ENTITY x "x">]><device/>')
 def test_no_derived(self):
  with self.assertRaises(ValueError):self.load('<device><peripherals><peripheral derivedFrom="X"><name>P</name></peripheral></peripherals></device>')
 def test_unknown_is_not_match(self):
  self.assertEqual(s.checks({},[{'path':'x','expected':0}])['counts']['unknown'],1)
 def test_actual(self):
  path=pathlib.Path(os.environ.get('SVD_TEST_FILE',str(pathlib.Path(__file__).parent/'extracted/SVD/STM32F103xx.svd')))
  if not path.is_file(): self.skipTest('Optional vendor SVD absent; set SVD_TEST_FILE to test an acquired original')
  m=s.model(path,['TIM2']);r=m['peripherals']['TIM2']['registers']['CNT'];self.assertEqual(r['address'],0x40000024);self.assertEqual(r['fields']['CNT']['bitWidth'],16)
 def fixture(self,reg='',field=''):
  return '<device><size>16</size><peripherals><peripheral><name>P</name><registers><register><name>R</name>'+reg+'<fields><field><name>F</name>'+field+'</field></fields></register></registers></peripheral></peripherals></device>'
 def test_range_exceeds_size(self):
  with self.assertRaises(ValueError):self.load(self.fixture(field='<bitOffset>16</bitOffset><bitWidth>1</bitWidth>'))
 def test_conflicting_ranges(self):
  with self.assertRaises(ValueError):self.load(self.fixture(field='<bitOffset>0</bitOffset><bitWidth>1</bitWidth><bitRange>[3:2]</bitRange>'))
 def test_duplicate_property(self):
  with self.assertRaises(ValueError):self.load(self.fixture(reg='<resetValue>0</resetValue><resetValue>1</resetValue>'))
 def test_register_semantic_inheritance(self):
  m=self.load(self.fixture(reg='<readAction>clear</readAction><modifiedWriteValues>oneToClear</modifiedWriteValues>',field='<bitOffset>0</bitOffset><bitWidth>1</bitWidth>'))
  f=m['peripherals']['P']['registers']['R']['fields']['F'];self.assertEqual(f['readAction'],'clear');self.assertEqual(f['readActionSource'],'register:R');self.assertEqual(f['modifiedWriteValues'],'oneToClear')
 def test_unknown_cli_nonzero(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d);(p/'x.svd').write_text(self.fixture());(p/'c.json').write_text(json.dumps([{'path':'missing','expected':0}]))
   r=subprocess.run([sys.executable,str(pathlib.Path(s.__file__)),str(p/'x.svd'),'--check',str(p/'c.json')],capture_output=True)
   self.assertEqual(r.returncode,3)
 def test_field_requires_register(self):
  r=subprocess.run([sys.executable,str(pathlib.Path(s.__file__)),'absent.svd','--field','F'],capture_output=True);self.assertEqual(r.returncode,2);self.assertIn(b'--field requires --register',r.stderr)
 def test_missing_peripheral(self):
  self.assertEqual(self.load(self.fixture(),['missing'])['peripherals']['missing']['status'],'unknown')
 def test_multiple_enum_groups_rejected(self):
  with self.assertRaises(ValueError):self.load(self.fixture(field='<enumeratedValues/><enumeratedValues/>'))
 def test_register_write_constraint_rejected(self):
  with self.assertRaises(ValueError):self.load(self.fixture(reg='<writeConstraint><writeAsRead>true</writeAsRead></writeConstraint>'))
if __name__=='__main__':unittest.main()
