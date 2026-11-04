import sys, os, base64, struct, numpy as np
def read_stl(p):
    b = open(p, 'rb').read(); n = struct.unpack('<I', b[80:84])[0]
    d = np.frombuffer(b[84:84 + n * 50], dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
    return d['v'].reshape(-1, 3).astype(np.float32)
out, label, dest = sys.argv[1], sys.argv[2], sys.argv[3]
cols = {'white': '#f2efe8', 'green': '#2f9a5c', 'gold': '#d9a43a', 'red': '#d0262e'}
parts = []
for i, c in enumerate(['white', 'green', 'gold', 'red'], 1):
    v = read_stl(os.path.join(out, 'stadium_%s_%d_%s.stl' % (label, i, c)))
    parts.append('{c:"%s",d:"%s"}' % (cols[c], base64.b64encode(v.tobytes()).decode()))
three = open('/home/user/epp-stadium-presentation/vendor/three.min.js').read()
html = '''<!doctype html><meta charset="utf-8"><title>Stadium keepsake preview</title>
<style>html,body{margin:0;height:100%;background:#0d1a17;overflow:hidden}canvas{display:block}#h{position:fixed;left:14px;bottom:12px;color:#9fb5ad;font:13px system-ui}</style>
<div id="h">Drag to turn · scroll to zoom</div>
<script>''' + three + '''</script><script>
const P=[''' + ','.join(parts) + '''];
const T=THREE, R=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});R.setPixelRatio(Math.min(devicePixelRatio,2));R.setSize(innerWidth,innerHeight);
R.outputColorSpace=T.SRGBColorSpace;document.body.appendChild(R.domElement);
const S=new T.Scene();S.background=new T.Color(0x0d1a17);
const C=new T.PerspectiveCamera(30,innerWidth/innerHeight,1,5000);
S.add(new T.HemisphereLight(0xffffff,0x334433,1.1));const L=new T.DirectionalLight(0xffffff,1.6);L.position.set(-120,-260,300);S.add(L);
const L2=new T.DirectionalLight(0xffffff,.5);L2.position.set(200,150,120);S.add(L2);
const G=new T.Group();S.add(G);let box=new T.Box3();
for(const p of P){const b=Uint8Array.from(atob(p.d),c=>c.charCodeAt(0));const g=new T.BufferGeometry();g.setAttribute('position',new T.BufferAttribute(new Float32Array(b.buffer),3));g.computeVertexNormals();
 const m=new T.Mesh(g,new T.MeshStandardMaterial({color:p.c,roughness:.62,metalness:p.c=='#d9a43a'?.35:0,flatShading:true}));G.add(m);g.computeBoundingBox();box.union(g.boundingBox);}
const ctr=box.getCenter(new T.Vector3()), sz=box.getSize(new T.Vector3()).length();
G.position.sub(ctr);let az=+(new URLSearchParams(location.search).get('az')||-0.35),el=+(new URLSearchParams(location.search).get('el')||0.62),dist=sz*(+(new URLSearchParams(location.search).get('d')||1.45));
const Q=new URLSearchParams(location.search),AIM=new T.Vector3(+(Q.get('tx')||0),+(Q.get('ty')||0),+(Q.get('tz')||0));function place(){C.position.set(AIM.x+Math.sin(az)*Math.cos(el)*dist,AIM.y-Math.cos(az)*Math.cos(el)*dist,AIM.z+Math.sin(el)*dist);C.up.set(0,0,1);C.lookAt(AIM);}
let drag=null;addEventListener('pointerdown',e=>drag=[e.clientX,e.clientY]);addEventListener('pointerup',()=>drag=null);
addEventListener('pointermove',e=>{if(!drag)return;az-=(e.clientX-drag[0])*.008;el=Math.max(.05,Math.min(1.5,el+(e.clientY-drag[1])*.006));drag=[e.clientX,e.clientY];});
addEventListener('wheel',e=>{dist*=1+Math.sign(e.deltaY)*.08});addEventListener('resize',()=>{R.setSize(innerWidth,innerHeight);C.aspect=innerWidth/innerHeight;C.updateProjectionMatrix();});
(function f(){place();R.render(S,C);requestAnimationFrame(f)})();window.READY=1;
</script>'''
open(dest, 'w').write(html); print(dest, os.path.getsize(dest) // 1024, 'KB')
