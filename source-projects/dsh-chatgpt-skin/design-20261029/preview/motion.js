/* Production motion source: image-backed deformation and eyelid in-betweens. */
(async()=>{
const W=1672,H=941,D=16,$=s=>document.querySelector(s),canvas=$('#scene');
const gl=canvas.getContext('webgl',{alpha:false,preserveDrawingBuffer:true,antialias:false});
if(!gl){$('#status').textContent='当前浏览器无法创建动画画布。';return;}
const vertex=`attribute vec2 a;varying vec2 uv;void main(){uv=a;gl_Position=vec4(a.x*2.-1.,1.-a.y*2.,0.,1.);}`;
const fragment=`precision highp float;varying vec2 uv;uniform float t;uniform sampler2D eye0,eye1,eye2,eye3,masks;const vec2 sz=vec2(1672.,941.);const float PI=3.14159265359;
float bell(vec2 p,vec2 c,vec2 r){vec2 d=(p-c)/r;return exp(-dot(d,d)*2.);}
float blink(float x,float start){float b=x-start;if(b<0.||b>.44)return 0.;if(b<.10)return smoothstep(0.,.10,b);if(b<.17)return 1.+smoothstep(.10,.17,b);if(b<.215)return 2.+smoothstep(.17,.215,b);if(b<.26)return 3.;if(b<.30)return 3.-smoothstep(.26,.30,b);if(b<.36)return 2.-smoothstep(.30,.36,b);return 1.-smoothstep(.36,.44,b);}
void main(){vec2 p=uv*sz;float q=t*2.*PI/16.;vec4 mask=texture2D(masks,uv);float body=mask.r;float hair=mask.g;float water=mask.b;
// Full-body outdoor composition with quiet, independent cloud movement.
vec2 shift=vec2(0.);float upper=1.-smoothstep(520.,805.,p.y);float breath=sin(q*3.);
shift.y+=body*upper*1.1*breath;shift.x+=body*upper*.5*sin(q*2.);
shift.x+=hair*(3.2*sin(q*2.+p.y*.007)+1.1*sin(q*3.-p.y*.004));shift.y+=hair*.9*sin(q*2.+p.x*.004);
float tassel=bell(p,vec2(686.,170.),vec2(10.,35.))+bell(p,vec2(664.,390.),vec2(20.,90.));shift.x+=tassel*2.5*sin(q*2.);
float tail=bell(p,vec2(370.,610.),vec2(90.,155.))*body;shift.x+=tail*2.1*sin(q);
float vine=bell(p,vec2(281.,167.),vec2(110.,250.))+bell(p,vec2(35.,420.),vec2(65.,390.));shift.x+=vine*3.6*sin(q*2.+p.y*.006);
shift.x+=water*(3.6*sin(q+p.y*.006)+1.1*sin(q*2.+p.x*.008));shift.y+=water*1.8*sin(q*2.+p.x*.004);
vec2 st=clamp((p+shift)/sz,vec2(.0005),vec2(.9995));vec4 col=texture2D(eye0,st);vec2 sp=st*sz;
float em=max(1.-smoothstep(.72,1.,length((sp-vec2(614.,159.))/vec2(21.,14.))),1.-smoothstep(.72,1.,length((sp-vec2(655.,146.))/vec2(21.,14.))));
float b=max(blink(t,4.15),blink(t,11.05));vec4 eyelid;if(b<1.)eyelid=mix(col,texture2D(eye1,st),b);else if(b<2.)eyelid=mix(texture2D(eye1,st),texture2D(eye2,st),b-1.);else eyelid=mix(texture2D(eye2,st),texture2D(eye3,st),b-2.);col=mix(col,eyelid,em);
float crystal=bell(p,vec2(1478.,253.),vec2(66.,90.));col.rgb+=crystal*.04*sin(q*3.)*vec3(.87,.71,1.);
float stars=bell(p,vec2(1110.,100.),vec2(360.,190.));col.rgb+=stars*.012*sin(q*2.+p.x*.025)*vec3(.7,.65,1.);
for(int i=0;i<8;i++){float f=float(i);float yy=mod(t/16.*1041.+f*139.,1041.)-50.;float xx=mod(45.+f*213.+34.*sin(q+f*1.91),1752.)-40.;vec2 d=p-vec2(xx,yy);float rot=q*2.+f;vec2 v=vec2(d.x*cos(rot)-d.y*sin(rot),d.x*sin(rot)+d.y*cos(rot));float petal=1.-smoothstep(.2,1.,length(v/vec2(3.9,1.6)));col.rgb=mix(col.rgb,vec3(.93,.84,.99),petal*(.13+.06*sin(q+f)));}
gl_FragColor=vec4(col.rgb,1.);}`;
function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;}
const pr=gl.createProgram();gl.attachShader(pr,shader(gl.VERTEX_SHADER,vertex));gl.attachShader(pr,shader(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(pr);if(!gl.getProgramParameter(pr,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(pr));gl.useProgram(pr);const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([0,0,1,0,0,1,0,1,1,0,1,1]),gl.STATIC_DRAW);const a=gl.getAttribLocation(pr,'a');gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,2,gl.FLOAT,false,0,0);gl.viewport(0,0,W,H);
const maskCanvas=document.createElement('canvas');maskCanvas.width=W;maskCanvas.height=H;const m=maskCanvas.getContext('2d');m.fillStyle='black';m.fillRect(0,0,W,H);m.globalCompositeOperation='lighter';
function path(d,color,blur=0){m.save();m.filter='blur('+blur+'px)';m.fillStyle=color;m.fill(new Path2D(d));m.restore();}
path('M573 40 L692 40 L747 181 L783 320 L837 447 L808 600 L1010 854 L885 919 L172 894 L64 811 L302 740 C287 656 315 577 363 514 L327 446 C378 349 467 279 543 217 C522 150 554 84 573 40 Z','rgb(255,0,0)',8);
path('M580 211 C518 233 417 259 363 336 L331 447 L406 475 C408 408 479 348 543 339 L600 268 Z','rgb(0,255,0)',10);
path('M704 171 C752 237 769 276 782 327 L786 496 L729 444 C748 354 711 312 687 257 Z','rgb(0,255,0)',10);
path('M818 274 L1672 279 L1672 941 L1621 941 L1453 809 L1265 702 L1066 643 L893 583 L853 509 Z','rgb(0,0,255)',20);
const sourceNames=['chatgpt-cloud-court-v2.png','chatgpt-cloud-blink-half.png','chatgpt-cloud-blink-almost.png','chatgpt-cloud-blink-closed.png'];
const images=await Promise.all(sourceNames.map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src='skin/chatgpt-silvercourt-dsh/assets/'+name;})));
[...images,maskCanvas].forEach((im,i)=>{const tx=gl.createTexture();gl.activeTexture(gl.TEXTURE0+i);gl.bindTexture(gl.TEXTURE_2D,tx);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,im);gl.uniform1i(gl.getUniformLocation(pr,i<4?'eye'+i:'masks'),i);});
const timeUniform=gl.getUniformLocation(pr,'t');let playing=true,position=0,last=performance.now(),speed=1,recording=false,recordStart=0,recorder;
function draw(t){gl.uniform1f(timeUniform,t);gl.drawArrays(gl.TRIANGLES,0,6);}
function tick(now){let dt=(now-last)/1000;last=now;if(recording){position=(now-recordStart)/1000;if(position>=D){position=0;recording=false;recorder.stop();}$('#status').textContent=recording?'正在导出 '+Math.min(100,Math.round(position/D*100))+'% · 请保持此页运行':'导出完成，可以保存成片。';}else if(playing)position=(position+Math.min(dt,.1)*speed)%D;draw(position);$('#timeline').value=position;$('#time').textContent=position.toFixed(2)+' s';requestAnimationFrame(tick);}
$('#play').onclick=()=>{playing=!playing;$('#play').textContent=playing?'暂停':'播放';};$('#timeline').oninput=e=>{position=Number(e.target.value);playing=false;$('#play').textContent='播放';};$('#slow').onclick=()=>{speed=speed===1?.22:1;if(speed!==1)position=4.0;playing=true;$('#play').textContent='暂停';$('#slow').textContent=speed===1?'眨眼慢放':'恢复原速';};

// MediaRecorder omits Duration; write it into the small Segment Info header.
async function addDuration(blob,seconds){
 const b=new Uint8Array(await blob.arrayBuffer());
 function el(at){let n=1;while(!(b[at]&(1<<(8-n))))n++;let id=0;for(let j=0;j<n;j++)id=id*256+b[at+j];at+=n;let k=1;while(!(b[at]&(1<<(8-k))))k++;let size=b[at]&((1<<(8-k))-1);for(let j=1;j<k;j++)size=size*256+b[at+j];return {id,size,data:at+k,k};}
 const ebml=el(0),segment=el(ebml.data+ebml.size);let at=segment.data,info=el(at);while(info.id!==0x1549a966){at=info.data+info.size;info=el(at);}
 const extra=new Uint8Array(11);extra.set([0x44,0x89,0x88]);new DataView(extra.buffer).setFloat64(3,seconds*1000,false);
 const header=b.slice(at,info.data);let value=info.size+extra.length;for(let j=header.length-1;j>=header.length-info.k;j--){header[j]=value%256;value=Math.floor(value/256);}header[header.length-info.k]|=1<<(8-info.k);
 return new Blob([b.slice(0,at),header,b.slice(info.data,info.data+info.size),extra,b.slice(info.data+info.size)],{type:blob.type});
}

$('#export').onclick=()=>{const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(x=>MediaRecorder.isTypeSupported(x));const chunks=[];const stream=canvas.captureStream(30);recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:6500000});recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recorder.onstop=async()=>{const blob=await addDuration(new Blob(chunks,{type:mime}),D);$('#download').href=URL.createObjectURL(blob);$('#download').hidden=false;$('#export').disabled=false;stream.getTracks().forEach(t=>t.stop());$('#status').textContent='导出完成 · '+(blob.size/1048576).toFixed(1)+' MiB · 30 fps · 无声循环';};$('#export').disabled=true;position=0;draw(0);recordStart=performance.now();recording=true;recorder.start(500);};
$('#status').textContent='动态原片就绪 · 16 秒循环 · 4 个眼睛状态 / 连续过渡';requestAnimationFrame(tick);
})().catch(err=>{document.querySelector('#status').textContent='制作失败：'+err.message;});
