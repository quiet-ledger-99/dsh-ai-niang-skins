import subprocess,sys
from common import *
import blink
C={109:0.5,110:1.0,111:1.0,112:0.55,113:0.2}
N=(L-2*K)+K
out=sys.argv[1]
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','24','-i','-',
 '-c:v','libx264','-preset','slow','-crf','11','-pix_fmt','yuv420p','-profile:v','high','-tune','animation','-x264-params','keyint=infinite:scenecut=0:ipratio=1.0:pbratio=1.0:aq-mode=3','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-an',out],stdin=subprocess.PIPE)
for j in range(N):
    im=out_frame(j)
    if j in C: im=blink.apply(im,C[j])
    p.stdin.write(np.clip(im+0.5,0,255).astype(np.uint8).tobytes())
p.stdin.close();p.wait();print('done',p.returncode,N)
