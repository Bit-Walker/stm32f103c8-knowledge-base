"""Build auditable bounded expectations from the pinned knowledge-base snapshot.
This author-written helper reads local Markdown only and emits JSON to stdout.
"""
import pathlib,re,json,sys,hashlib
root=pathlib.Path(sys.argv[1]); tim='参数/TIM/硬件参数表.md'; dma='参数/DMA参数与HAL接口.md'; t=(root/tim).read_text();d=(root/dma).read_text();checks=[]
expected_hashes={tim:'276f896495ad8c4fe4157bf8a541f27017c952705dc2bfbf29ed3b6782a7a818',dma:'28f6e61d76c8c1ac8692a3cae1616689ccfc2bd67dba37da8c5b7e6570a86bd3'}
for name,digest in expected_hashes.items():
 if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
  raise ValueError('Baseline hash changed; review extraction before updating expected hash: '+name)
def c(p,v,source):
 path,section=source.split('#',1)
 checks.append({'path':'peripherals.'+p,'expected':v,'source':{'file':path,'section_label':section,'locator_kind':'human-readable section/formula label, not a URL anchor'}})
def field(p,r,f,start,width,src):
 c(f'{p}.registers.{r}.fields.{f}.bitOffset',start,src);c(f'{p}.registers.{r}.fields.{f}.bitWidth',width,src)
# Register maps parsed directly; CCMR input/output are same-address SVD views.
common=t.split('TIM1～TIM4 的公共寄存器：')[1].split('TIM1 的附加寄存器：')[0]
extra=t.split('TIM1 的附加寄存器：')[1].split('32位寄存器CPU')[0]
for pn,section in [('TIM1',common+extra),('TIM2',common)]:
 for offset,name,reset in re.findall(r'\| (0x[0-9A-Fa-f]+) \| (\w+) \| (0x[0-9A-Fa-f]+|0) \|',section):
  for rn in ([name+'_Input',name+'_Output'] if name.startswith('CCMR') else [name]):
   c(f'{pn}.registers.{rn}.addressOffset',int(offset,16),tim+'#寄存器地图与实例差异')
   c(f'{pn}.registers.{rn}.resetValue.value',int(reset,0),tim+'#寄存器地图与实例差异')
# Explicit bit position tables, independent from SVD.
for heading,reg,instances in [('CR1计数控制','CR1',['TIM1','TIM2']),('SMCR时钟与从模式','SMCR',['TIM1','TIM2']),('DIER共享请求位','DIER',['TIM1','TIM2']),('TIM1 BDTR','BDTR',['TIM1'])]:
 section=t.split('## '+heading+'\n')[1].split('\n## ')[0].strip().split('\n\n')[0]
 for bits,fn in re.findall(r'^\|(\d+(?::\d+)?)\|(\w+)\|',section,re.M):
  nums=list(map(int,bits.split(':')));start=nums[-1];width=nums[0]-start+1
  for pn in instances: field(pn,reg,fn,start,width,tim+'#'+heading)
for pn in ['TIM1','TIM2']:
 for rn in ['CNT','PSC','ARR','CCR1','CCR2','CCR3','CCR4']: field(pn,rn,rn,0,16,tim+'#共享计数与比较寄存器')
field('TIM1','RCR','REP',0,8,tim+'#共享计数与比较寄存器')
c('DMA1.baseAddress',0x40020000,dma+'#全部-dma1-寄存器')
for rn,offset in [('ISR',0),('IFCR',4)]+[(stem+str(i),base+20*(i-1)) for i in range(1,8) for stem,base in [('CCR',8),('CNDTR',12),('CPAR',16),('CMAR',20)]]:
 c(f'DMA1.registers.{rn}.addressOffset',offset,dma+'#1347-完整寄存器偏移地图')
 c(f'DMA1.registers.{rn}.resetValue.value',0,dma+'#全部-dma1-寄存器')
 c(f'DMA1.registers.{rn}.size.value',32,dma+'#全部-dma1-寄存器 [SVD size corroborates storage width, not ES096 access policy]')
for i in range(1,8):
 for j,fn in enumerate(['GIF','TCIF','HTIF','TEIF']):
  field('DMA1','ISR',fn+str(i),4*(i-1)+j,1,dma+'#1341-ISR')
  field('DMA1','IFCR','C'+fn+str(i),4*(i-1)+j,1,dma+'#1342-IFCR')
 for bits,fn in re.findall(r'^\|(\d+(?::\d+)?)\|(\w+)\|',d.split('### 13.4.3')[1].split('### 13.4.4')[0],re.M):
  nums=list(map(int,bits.split(':')));field('DMA1','CCR'+str(i),fn,nums[-1],nums[0]-nums[-1]+1,dma+'#1343-CCRx')
 for reg,fn,width in [('CNDTR','NDT',16),('CPAR','PA',32),('CMAR','MA',32)]: field('DMA1',reg+str(i),fn,0,width,dma+'#全部-dma1-寄存器')
# Probe for machine-readable semantics; absence must remain UNKNOWN.
c('DMA1.registers.IFCR.fields.CGIF1.modifiedWriteValues','oneToClear',dma+'#中断 (semantic probe)')
c('TIM2.registers.SR.fields.UIF.modifiedWriteValues','zeroToClear',tim+'#其余控制语义的归属 (semantic probe)')
c('TIM2.registers.CCR1.fields.CCR1.readAction','modifyExternal',tim+'#共享计数与比较寄存器 (semantic probe; conditional/side-effect target requires RM)')
if len(checks)!=654: raise ValueError('Expected exactly 654 assertions; review extraction')
if len({c['path'] for c in checks})!=654: raise ValueError('Duplicate assertion path')
print(json.dumps(checks,ensure_ascii=False,indent=2))
