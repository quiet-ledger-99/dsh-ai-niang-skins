import cv2,numpy as np,json,functools
D='/workspace/chatgpt-skin-bg/v5b_work/'
ts=json.load(open(D+'ts_1.5_3.0.json'));K=8;W,H=1920,1080;ALPHA=0.65
@functools.lru_cache(maxsize=8)
def load(i):
    s=cv2.imread(D+f'sr/{i:04d}.png').astype(np.float32)
    l=cv2.resize(cv2.imread(D+f'src/{i:04d}.png'),(W,H),interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    return ALPHA*s+(1-ALPHA)*l
def fr(t):
    i=int(np.floor(t));a=t-i
    return load(i) if a<1e-6 or i>=240 else (1-a)*load(i)+a*load(i+1)
L=len(ts)
def out_frame(j):  # j = output index 0..218
    k=j+K
    if k<L-K: return fr(ts[k])
    v=k-(L-K); t=(v+1)/(K+1);a=t*t*(3-2*t); return (1-a)*fr(ts[L-K+v])+a*fr(ts[v])
