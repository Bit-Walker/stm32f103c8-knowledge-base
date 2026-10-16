#!/usr/bin/env python3
"""Offline read-only CMSIS-SVD query and explicit-claim checker (stdlib only).
No network, imports of vendor code, MMIO or file writes. Unknown is not a pass.
Supports explicit peripherals/registers/fields, inherited register defaults and
bitOffset/bitWidth, lsb/msb, bitRange. Rejects unsupported constructs in selected
peripherals rather than silently guessing. This is deliberately not a full SVD engine.
"""
import argparse, hashlib, json, pathlib, re, sys
import xml.etree.ElementTree as ET
LIMIT = 16 * 1024 * 1024

def number(s):
    if s is None: return None
    s = s.strip()
    if re.fullmatch(r'#[01]+', s): return int(s[1:], 2)
    if re.fullmatch(r'0[xX][0-9a-fA-F]+', s): return int(s, 16)
    if re.fullmatch(r'[0-9]+', s): return int(s, 10)
    raise ValueError('Unsupported numeric value: ' + s)

def safe_xml(path):
    with open(path, 'rb') as f: data = f.read(LIMIT + 1)
    if len(data) > LIMIT: raise ValueError('XML exceeds 16 MiB limit')
    # UTF-8-only source is intentional: prevents UTF-16/32 bypass of DTD guard.
    data.decode('utf-8-sig')
    if b'\0' in data or re.search(br'<!\s*(DOCTYPE|ENTITY)\b', data, re.I):
        raise ValueError('DTD/entities and non-UTF8 XML are forbidden')
    root = ET.fromstring(data)
    if root.tag != 'device': raise ValueError('Unsupported root/namespace')
    return root, hashlib.sha256(data).hexdigest()

SINGLETONS = set('name version size resetValue resetMask access baseAddress addressOffset bitOffset bitWidth lsb msb bitRange readAction modifiedWriteValues alternateRegister alternateGroup description registers fields writeConstraint enumeratedValues'.split())

def validate_singletons(node, recursive=True):
    for e in (node.iter() if recursive else [node]):
        for name in SINGLETONS:
            if len(e.findall(name)) > 1:
                raise ValueError('Duplicate supported property: ' + name)

def inherited(nodes, name, numeric=False):
    for node in nodes:
        v = node.findtext(name)
        if v is not None: return {'value': number(v) if numeric else v, 'source': node.tag + ':' + (node.findtext('name') or '')}
    return {'value': None, 'source': 'unknown'}

def unique(nodes):
    result = {}
    for n in nodes:
        name = n.findtext('name')
        if not name or name in result: raise ValueError('Missing or duplicate name')
        result[name] = n
    return result

def model(path, names):
    root, digest = safe_xml(path)
    validate_singletons(root, False)
    peripherals = unique(root.findall('./peripherals/peripheral'))
    out = {'svd_sha256': digest, 'device': root.findtext('name'), 'version': root.findtext('version'), 'peripherals': {}}
    for name in names:
        if name not in peripherals:
            out['peripherals'][name] = {'status':'unknown', 'reason':'peripheral absent', 'registers':{}}
            continue
        p = peripherals[name]
        validate_singletons(p)
        if any('derivedFrom' in e.attrib or e.tag in ('dim','cluster') for e in p.iter()):
            raise ValueError('Unsupported derivedFrom/dim/cluster in selected peripheral ' + name)
        po = {'baseAddress': number(p.findtext('baseAddress')), 'registers': {}}
        for rn, r in unique(p.findall('./registers/register')).items():
            if r.find('writeConstraint') is not None: raise ValueError('Register writeConstraint unsupported; no effective constraint inference')
            ro = {key: inherited([r,p,root],key,key!='access') for key in ('size','resetValue','resetMask','access')}
            ro.update(name=rn,addressOffset=number(r.findtext('addressOffset')),fields={},description=r.findtext('description'))
            ro['address'] = None if po['baseAddress'] is None or ro['addressOffset'] is None else po['baseAddress'] + ro['addressOffset']
            for key in ('readAction','modifiedWriteValues','alternateRegister','alternateGroup'):
                ro[key] = r.findtext(key) # absent explicitly remains unknown
            for fn,f in unique(r.findall('./fields/field')).items():
                forms = [f.find('bitOffset') is not None or f.find('bitWidth') is not None,
                         f.find('lsb') is not None or f.find('msb') is not None,
                         f.find('bitRange') is not None]
                if sum(forms) > 1: raise ValueError('Multiple field range representations')
                if (f.find('bitOffset') is None) != (f.find('bitWidth') is None): raise ValueError('Incomplete bitOffset/bitWidth')
                if (f.find('lsb') is None) != (f.find('msb') is None): raise ValueError('Incomplete lsb/msb')
                start,width=number(f.findtext('bitOffset')),number(f.findtext('bitWidth'))
                if start is None and f.findtext('lsb') is not None:
                    start=number(f.findtext('lsb')); end=number(f.findtext('msb')); width=None if end is None else end-start+1
                if start is None and f.findtext('bitRange') is not None:
                    m=re.fullmatch(r'\[(\d+):(\d+)\]', f.findtext('bitRange'))
                    if not m: raise ValueError('Unsupported bitRange')
                    start=int(m[2]);width=int(m[1])-start+1
                if start is not None and (start<0 or width is None or width<1 or start+width>1024): raise ValueError('Invalid field width')
                if start is not None and ro['size']['value'] is not None and start+width > ro['size']['value']: raise ValueError('Field exceeds register size')
                fo={'bitOffset':start,'bitWidth':width,'access':inherited([f,r,p,root],'access'), 'description':f.findtext('description')}
                for key in ('readAction','modifiedWriteValues','writeConstraint','enumeratedValues'):
                    if key in ('readAction','modifiedWriteValues'):
                        prop=inherited([f,r],key)
                        fo[key]=prop['value'];fo[key+'Source']=prop['source']
                    else:
                        e=f.find(key);fo[key]=None if e is None else ET.tostring(e,encoding='unicode')
                ro['fields'][fn]=fo
            po['registers'][rn]=ro
        out['peripherals'][name]=po
    return out

def checks(data, expected):
    rows=[]
    for c in expected:
        value=data
        for key in c['path'].split('.'):
            value=value.get(key) if isinstance(value,dict) else None
        status='unknown' if value is None else ('match' if value==c['expected'] else 'mismatch')
        rows.append(dict(c,actual=value,status=status))
    return {'counts':{s:sum(x['status']==s for x in rows) for s in ('match','mismatch','unknown')},'checks':rows}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('svd',type=pathlib.Path);ap.add_argument('--peripherals',nargs='+',default=['DMA1','TIM1','TIM2'])
    ap.add_argument('--register');ap.add_argument('--field');ap.add_argument('--check',type=pathlib.Path)
    args=ap.parse_args()
    if args.field and not args.register: ap.error('--field requires --register')
    if args.check and (args.register or args.field): ap.error('--check cannot be combined with --register/--field')
    data=model(args.svd,args.peripherals)
    if args.check: result=checks(data,json.loads(args.check.read_text(encoding='utf-8')))
    elif args.register:
        result={}
        for pn,p in data['peripherals'].items():
            r=p['registers'].get(args.register)
            value=r.get('fields',{}).get(args.field) if args.field and r else r
            result[pn]=value if value is not None else {'status':'unknown','reason':'selected register or field absent'}
    else: result=data
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return (1 if result['counts']['mismatch'] else 3 if result['counts']['unknown'] else 0) if args.check else 0
if __name__=='__main__':
    try: sys.exit(main())
    except (ValueError,OSError,ET.ParseError) as e: print(str(e),file=sys.stderr);sys.exit(2)
