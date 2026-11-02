/* Editable 2.5D animation. Artwork is fixed; eyelids are separately drawn frames. */
(async () => {
  const $ = s => document.querySelector(s), canvas = $('#scene');
  const cfg = await (await fetch('motion-config.json')).json();
  const W = 1672, H = 941, D = 16;
  const gl = canvas.getContext('webgl', {alpha:false, antialias:false, preserveDrawingBuffer:true});
  if (!gl) throw new Error('无法创建动画画布');
  const vertex = `attribute vec2 a;varying vec2 uv;void main(){uv=a;gl_Position=vec4(a.x*2.-1.,1.-a.y*2.,0.,1.);}`;
  const fragment = `precision highp float;
  varying vec2 uv;uniform float t,theme;uniform sampler2D eye0,eye1,eye2,masks;
  uniform vec2 ec0,ec1,er;const vec2 sz=vec2(1672.,941.);const float PI=3.14159265359;
  float bell(vec2 p,vec2 c,vec2 r){vec2 d=(p-c)/r;return exp(-dot(d,d)*2.);}
  float blink(float x,float start){float z=x-start;if(z<0.||z>.38)return 0.;
    if(z<.08)return smoothstep(0.,.08,z);if(z<.14)return 1.+smoothstep(.08,.14,z);
    if(z<.21)return 2.;if(z<.28)return 2.-smoothstep(.21,.28,z);return 1.-smoothstep(.28,.38,z);}
  void main(){
    vec2 p=uv*sz;float q=t*2.*PI/16.;vec4 m=texture2D(masks,uv);
    float body=m.r,hair=m.g,world=m.b*(1.-body);vec2 sh=vec2(0.);
    // Different frequencies and phase delays prevent the whole picture reversing together.
    float breath=sin(q*4.);sh.y+=body*(1.-smoothstep(650.,930.,p.y))*2.1*breath;
    sh.x+=body*.7*sin(q*2.+.6);
    sh.x+=hair*(6.1*sin(q*2.-p.y*.006)+1.6*sin(q*3.+p.y*.008));
    sh.y+=hair*1.4*sin(q*2.+p.x*.006);
    if(theme>.5){
      float hem=bell(p,vec2(1150.,820.),vec2(430.,190.))*body;
      sh.y+=hem*3.7*sin(q*2.-p.x*.005);sh.x+=hem*2.2*sin(q*3.+p.y*.008);
      float curtain=bell(p,vec2(1460.,110.),vec2(260.,210.))*(1.-body);
      sh.x+=curtain*5.8*sin(q*2.+p.y*.005);sh.y+=curtain*2.4*sin(q*3.+p.x*.004);
      sh.x+=world*(7.8*sin(q+p.y*.005)+3.2*sin(q*2.+p.x*.004));
      sh.y+=world*2.1*sin(q*2.+p.x*.004);
    }else{
      float tail=bell(p,vec2(330.,490.),vec2(160.,230.))*body;
      sh.x+=tail*4.7*sin(q*2.);sh.y+=tail*2.5*sin(q*2.+.8);
      sh.x+=world*(3.8*sin(p.y*.035-q*3.)+1.6*sin(q*2.+p.x*.008));
      sh.y+=world*1.2*sin(q*3.+p.x*.006);
      float hang=bell(p,vec2(1291.,160.),vec2(45.,170.))+bell(p,vec2(430.,154.),vec2(38.,150.));
      sh.x+=hang*2.7*sin(q*2.)*smoothstep(0.,240.,p.y);
    }
    vec2 st=clamp((p+sh)/sz,vec2(.0005),vec2(.9995));vec2 sp=st*sz;
    vec4 col=texture2D(eye0,st);
    float em=max(1.-smoothstep(.72,1.,length((sp-ec0)/er)),1.-smoothstep(.72,1.,length((sp-ec1)/er)));
    float b=max(blink(t,3.4),blink(t,10.6));
    vec4 lid=b<1.?mix(col,texture2D(eye1,st),b):mix(texture2D(eye1,st),texture2D(eye2,st),b-1.);
    col=mix(col,lid,em);
    if(theme>.5){
      float flame=bell(p,vec2(1540.,639.),vec2(95.,175.))+bell(p,vec2(1610.,570.),vec2(45.,130.));
      float pulse=.052*sin(q*7.)+.029*sin(q*11.+.7)+.014*sin(q*17.);
      col.rgb+=flame*pulse*vec3(1.,.53,.20);
      float moon=bell(p,vec2(280.,135.),vec2(240.,230.))*(1.-body);
      col.rgb+=moon*.015*sin(q*2.)*vec3(1.,.24,.25);
      float mist=world*bell(p,vec2(1190.,440.),vec2(430.,180.));
      col.rgb+=mist*.019*(sin(p.x*.009-q*2.)+sin(p.x*.015+q*3.))*vec3(.75,.78,1.);
    }else{
      float light=world*smoothstep(.3,.8,dot(col.rgb,vec3(.21,.72,.07)));
      col.rgb+=light*.026*sin(p.y*.075-q*4.+sin(p.x*.012+q))*vec3(.5,.8,1.);
      float lamp=bell(p,vec2(1545.,540.),vec2(115.,140.));
      col.rgb+=lamp*.024*sin(q*5.)*vec3(1.,.8,.47);
      for(int i=0;i<13;i++){
        float f=float(i);vec2 bp=vec2(mod(400.+f*117.+19.*sin(q+f),1320.),mod(980.-t*58.+f*97.,1020.)-40.);
        float rad=2.4+mod(f,3.);float d=length(p-bp);float ring=(1.-smoothstep(.4,1.3,abs(d-rad)));
        col.rgb=mix(col.rgb,vec3(.85,.96,1.),ring*.15*(1.-body));
      }
    }
    // Sparse particles leave the face and reading area calm.
    for(int i=0;i<7;i++){
      float f=float(i);float xx=mod(1740.-t*27.+f*263.,1752.)-40.;float yy=110.+mod(f*139.,770.)+25.*sin(q+f);
      vec2 d=p-vec2(xx,yy);float a=q*2.+f;vec2 v=vec2(d.x*cos(a)-d.y*sin(a),d.x*sin(a)+d.y*cos(a));
      float petal=1.-smoothstep(.25,1.,length(v/vec2(theme>.5?7.:2.5,theme>.5?3.:2.5)));
      vec3 ink=theme>.5?vec3(.56,.07,.14):vec3(.88,.97,1.);
      col.rgb=mix(col.rgb,ink,petal*.35*(1.-body*.8));
    }
    gl_FragColor=vec4(col.rgb,1.);
  }`;
  function shader(type,src){const s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;}
  const program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,vertex));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);gl.useProgram(program);
  const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([0,0,1,0,0,1,0,1,1,0,1,1]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(program,'a');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);gl.viewport(0,0,W,H);
  const mc=document.createElement('canvas');mc.width=W;mc.height=H;const m=mc.getContext('2d');m.fillStyle='black';m.fillRect(0,0,W,H);m.globalCompositeOperation='lighter';
  for(const path of cfg.masks){m.save();m.filter='blur('+path.blur+'px)';m.fillStyle=path.color;m.fill(new Path2D(path.d));m.restore();}
  const images=await Promise.all(cfg.frames.map(src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error('图片未加载 '+src));im.src=src;})));
  [...images,mc].forEach((im,i)=>{const tex=gl.createTexture();gl.activeTexture(gl.TEXTURE0+i);gl.bindTexture(gl.TEXTURE_2D,tex);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,im);gl.uniform1i(gl.getUniformLocation(program,i<3?'eye'+i:'masks'),i);});
  gl.uniform1f(gl.getUniformLocation(program,'theme'),cfg.theme==='grok'?1:0);
  gl.uniform2fv(gl.getUniformLocation(program,'ec0'),cfg.eyes[0]);gl.uniform2fv(gl.getUniformLocation(program,'ec1'),cfg.eyes[1]);gl.uniform2fv(gl.getUniformLocation(program,'er'),cfg.eyeRadius);
  const tu=gl.getUniformLocation(program,'t');let position=0,last=performance.now(),playing=!matchMedia('(prefers-reduced-motion:reduce)').matches,speed=1,recording=false,start=0,recorder;
  function draw(t){gl.uniform1f(tu,t);gl.drawArrays(gl.TRIANGLES,0,6);}
  function tick(now){const dt=Math.min((now-last)/1000,.1);last=now;if(recording){position=(now-start)/1000;if(position>=D){recording=false;position=0;recorder.stop();}}else if(playing&&!document.hidden)position=(position+dt*speed)%D;
    if(!document.hidden||recording)draw(position);$('#timeline').value=position;$('#time').textContent=position.toFixed(2)+' s';requestAnimationFrame(tick);}
  $('#play').onclick=()=>{playing=!playing;$('#play').textContent=playing?'暂停':'播放';};
  $('#timeline').oninput=e=>{position=Number(e.target.value);playing=false;$('#play').textContent='播放';draw(position);};
  $('#slow').onclick=()=>{position=3.25;speed=speed===1?.2:1;playing=true;$('#slow').textContent=speed===1?'眨眼慢放':'恢复原速';};
  $('#export').onclick=()=>{
    const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8'].find(x=>MediaRecorder.isTypeSupported(x));
    const stream=canvas.captureStream(30),chunks=[];recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:14000000});
    recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
    recorder.onstop=async()=>{const blob=new Blob(chunks,{type:mime});const response=await fetch('/export/'+cfg.theme,{method:'POST',headers:{'Content-Type':mime},body:blob});stream.getTracks().forEach(tr=>tr.stop());$('#export').disabled=false;$('#status').textContent=response.ok?'视频已保存 · 16 秒 / 30 fps / 无声':'导出保存失败';};
    position=0;draw(0);start=performance.now();recording=true;$('#export').disabled=true;$('#status').textContent='正在导出 16 秒循环，请保持预览页可见';recorder.start(500);
  };
  $('#status').textContent=cfg.label+' · 16 秒循环 / 三段眼睛画面与连续过渡';requestAnimationFrame(tick);
})().catch(e=>{document.querySelector('#status').textContent=e.message;});
