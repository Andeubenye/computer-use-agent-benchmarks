"""Losslessly unwrap JPEG payloads; retain every original server response unchanged."""
import hashlib,json
from pathlib import Path
from common import OUT,save
records=[]
for p in (OUT/'runs/sai').glob('*/screenshots/*.jpg'):
 if '.recovered.' in p.name:continue
 data=p.read_bytes();offset=data.find(bytes.fromhex('ffd8ff'))
 if 0<offset<128 and data.endswith(bytes.fromhex('ffd9')):
  derived=p.with_name(p.stem+'.recovered.jpg');derived.write_bytes(data[offset:])
  records.append({'original':str(p.relative_to(OUT)),'original_sha256':hashlib.sha256(data).hexdigest(),'jpeg_start_offset':offset,'derived':str(derived.relative_to(OUT)),'derived_sha256':hashlib.sha256(data[offset:]).hexdigest(),'pixels_modified':False})
save(OUT/'audit/sai-image-unwrapping.json',{'reason':'Screenshot endpoint returned 15 non-JPEG prefix bytes before an intact JPEG stream. Original responses remain unchanged. Derived images omit only the prefix.','images':records})
print('Unwrapped',len(records),'JPEG payloads; originals preserved.')
