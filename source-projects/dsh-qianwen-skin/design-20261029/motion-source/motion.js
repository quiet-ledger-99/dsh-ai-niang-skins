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
// Mesh-like inverse displacement keeps lettering and DSH controls outside the film.
vec2 shift=vec2(0.);float upper=1.-smoothstep(640.,865.,p.y);float breath=sin(q*3.);shift.y+=body*upper*2.7*breath;shift.x+=body*upper*.9*sin(q*2.);
float head=bell(p,vec2(1175.,260.),vec2(330.,330.))*body;float angle=.0018*sin(q*2.);shift+=head*vec2(-(p.y-480.)*angle,(p.x-1190.)*angle);
shift.x+=hair*(5.2*sin(q*2.+p.y*.007)+1.6*sin(q*3.-p.y*.004));shift.y+=hair*1.7*sin(q*2.+p.x*.004);
float tassel=bell(p,vec2(922.,364.),vec2(19.,69.));shift.x+=tassel*5.2*sin(q*2.)*smoothstep(285.,390.,p.y);
float braid=bell(p,vec2(1330.,620.),vec2(69.,235.))*body;shift.x+=braid*1.9*sin(q*2.+.8);
float willow=bell(p,vec2(87.,194.),vec2(220.,305.));shift.x+=willow*(4.4*sin(q*2.+p.y*.006)+1.8*sin(q*3.-p.x*.009))*smoothstep(0.,220.,p.y);shift.y+=willow*1.1*sin(q*2.);
float hanging=bell(p,vec2(820.,180.),vec2(17.,52.))+bell(p,vec2(1435.,162.),vec2(14.,90.));shift.x+=hanging*3.4*sin(q*2.)*smoothstep(90.,215.,p.y);
shift.x+=water*(2.7*sin(p.y*.18-q*4.)+1.2*sin(p.y*.071+q*3.));shift.y+=water*.45*sin(q*3.+p.x*.012);
float curtain=bell(p,vec2(1624.,100.),vec2(80.,175.));shift.x+=curtain*2.5*sin(q*2.+p.y*.008);
vec2 st=clamp((p+shift)/sz,vec2(.0005),vec2(.9995));vec4 col=texture2D(eye0,st);vec2 sp=st*sz;
float em=max(1.-smoothstep(.72,1.,length((sp-vec2(1105.,327.))/vec2(48.,32.))),1.-smoothstep(.72,1.,length((sp-vec2(1221.,283.))/vec2(48.,32.))));
float b=max(blink(t,4.15),blink(t,11.05));vec4 eyelid;if(b<1.)eyelid=mix(col,texture2D(eye1,st),b);else if(b<2.)eyelid=mix(texture2D(eye1,st),texture2D(eye2,st),b-1.);else eyelid=mix(texture2D(eye2,st),texture2D(eye3,st),b-2.);col=mix(col,eyelid,em);
float luma=dot(col.rgb,vec3(.2126,.7152,.0722));float shimmer=water*(.055*sin(p.y*.37-q*4.)+.025*sin(p.y*.12+q*3.))*smoothstep(.25,.7,luma);col.rgb+=vec3(.74,.84,1.)*shimmer;
float lantern=bell(p,vec2(1642.,370.),vec2(125.,185.));float lampPulse=.045*sin(q*4.)+.018*sin(q*7.);col.rgb+=lantern*lampPulse*vec3(1.,.63,.27);
float halo=bell(p,vec2(762.,211.),vec2(110.,110.));col.rgb+=halo*.012*sin(q*2.)*vec3(.78,.86,1.);
// A few drifting petals, with positions and opacity continuous across the loop.
for(int i=0;i<7;i++){float f=float(i);float yy=mod(t/16.*1021.+f*151.,1021.)-40.;float xx=mod(67.+f*239.+52.*sin(q+f*1.91),1752.)-40.;vec2 d=p-vec2(xx,yy);float rot=q*2.+f;vec2 v=vec2(d.x*cos(rot)-d.y*sin(rot),d.x*sin(rot)+d.y*cos(rot));float petal=1.-smoothstep(.25,1.,length(v/vec2(4.4+mod(f,2.),1.9)));float opacity=(.17+.12*sin(q+f))*petal;col.rgb=mix(col.rgb,vec3(.81,.87,.98),opacity);}
gl_FragColor=vec4(col.rgb,1.);}`;
function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;}
const pr=gl.createProgram();gl.attachShader(pr,shader(gl.VERTEX_SHADER,vertex));gl.attachShader(pr,shader(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(pr);if(!gl.getProgramParameter(pr,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(pr));gl.useProgram(pr);const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([0,0,1,0,0,1,0,1,1,0,1,1]),gl.STATIC_DRAW);const a=gl.getAttribLocation(pr,'a');gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,2,gl.FLOAT,false,0,0);gl.viewport(0,0,W,H);
const maskCanvas=document.createElement('canvas');maskCanvas.width=W;maskCanvas.height=H;const m=maskCanvas.getContext('2d');m.fillStyle='black';m.fillRect(0,0,W,H);m.globalCompositeOperation='lighter';
function path(d,color,blur=0){m.save();m.filter='blur('+blur+'px)';m.fillStyle=color;m.fill(new Path2D(d));m.restore();}
path('M976 0 L1235 0 C1335 42 1374 184 1357 287 C1384 356 1420 416 1480 455 C1550 515 1648 543 1665 634 C1685 695 1615 739 1580 770 L1650 855 L1430 884 L816 852 L599 830 C585 792 644 760 695 744 C737 718 765 705 791 657 C823 597 838 550 875 502 C911 469 941 430 964 375 C936 341 934 285 912 248 C901 223 905 184 930 159 C934 96 950 32 976 0 Z','rgb(255,0,0)',8);
path('M1018 365 C958 432 902 480 854 579 C838 648 788 689 745 724 C699 753 633 767 606 814 L670 817 C753 781 814 734 851 668 C889 589 955 550 987 495 Z','rgb(0,255,0)',12);
path('M1330 330 C1384 391 1426 452 1496 479 C1581 523 1660 577 1664 647 C1679 708 1600 750 1550 766 L1480 740 C1555 718 1574 658 1535 612 C1486 572 1426 537 1394 488 C1364 444 1340 390 1330 330 Z','rgb(0,255,0)',12);
path('M0 508 C170 511 284 514 465 513 L787 502 L800 628 L643 651 L469 674 C392 624 296 601 191 601 L0 562 Z','rgb(0,0,255)',8);
const sourceNames=['qianwen-moon-study.png','qianwen-blink-half.png','qianwen-blink-almost.png','qianwen-blink.png'];
const images=await Promise.all(sourceNames.map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src='skin/qianwen-moonporcelain-dsh/assets/'+name;})));
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
