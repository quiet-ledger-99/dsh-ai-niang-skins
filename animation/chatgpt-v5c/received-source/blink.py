# v5c 眨眼：每只眼只用"这只眼、这一帧自己的"原画素材
#  - 眼区用这只眼周围的皮肤 inpaint 盖掉（开眼睫毛/虹膜/下睑线全盖）
#  - 闭眼线 = 这只眼原上睫毛按列抽出的浓度剖面，沿闭眼弧重新摆放、厚度压到 ~60%（外眼角睫毛团原地保留）
import numpy as np, cv2
LUM=np.array([.15,.55,.3],np.float32)   # BGR
def bez(P,n=400):
    P=np.asarray(P,np.float32); t=np.linspace(0,1,n)[:,None]
    return (1-t)**2*P[0]+2*(1-t)*t*P[1]+t**2*P[2]
def cy(P,xs):
    q=bez(P); return np.interp(xs,q[:,0],q[:,1])
EYES=dict(
 L=dict(box=(698,154,740,186),
   mask=[(709,166),(712,162.3),(718,161.3),(726,161.3),(731.5,163.5),(733,168),(732,174),(729,178.5),(722,179),(715,178.5),(711,176),(709,173)],
   lash=[(708,166),(712,163),(718,162.5),(726,163),(730,165),(732,168),(729,168.5),(722,167.5),(716,167.5),(712,168),(711,173),(708,173.5)],
   open=[(709,169.5),(719,163.6),(731,167)], shut=[(709,170.5),(719,177.6),(731,172.2)],
   xr=(709,731)),
 R=dict(box=(750,148,796,178),
   mask=[(756.5,161.5),(760,157),(766,154.3),(774,154.3),(782,155),(788.5,158.5),(788,163),(784,167),(778,171),(770,172),(762,171.5),(756.5,168.5),(756,164)],
   lash=[(757,162.5),(760,158),(766,156),(774,156),(782,157),(788,159.5),(787,162),(782,163),(781,167),(778,167),(778,162.5),(770,162),(763,162.5),(759,164.5)],
   open=[(758,163),(772,157.6),(787,160.5)], shut=[(758,164.8),(772,170.4),(787,164.2)],
   xr=(758,787)),
)
def poly_mask(pts,x0,y0,shape,ss=4):
    h,w=shape; m=np.zeros((h*ss,w*ss),np.uint8)
    p=np.round((np.array(pts,np.float32)-[x0-0.5,y0-0.5])*ss).astype(np.int32)
    cv2.fillPoly(m,[p],255); return cv2.resize(m,(w,h),interpolation=cv2.INTER_AREA).astype(np.float32)/255
def fill_cols(P,Mb,skin):
    ph,pw=P.shape[:2]; clean=P.copy()
    tops=np.full(pw,np.nan); bots=np.full(pw,np.nan)
    A=np.zeros((pw,3),np.float32); B=np.zeros((pw,3),np.float32); ok_a=np.zeros(pw,bool); ok_b=np.zeros(pw,bool)
    for x in range(pw):
        r=np.where(Mb[:,x])[0]
        if len(r)==0: continue
        t,b=r.min(),r.max(); tops[x]=t; bots[x]=b
        ra=[y for y in range(max(0,t-4),t) if skin[y,x]]; rb=[y for y in range(b+1,min(ph,b+5)) if skin[y,x]]
        if ra: A[x]=np.median(P[ra,x],0); ok_a[x]=True
        if rb: B[x]=np.median(P[rb,x],0); ok_b[x]=True
    xs=np.arange(pw); cols=~np.isnan(tops)
    for arr,ok in ((A,ok_a),(B,ok_b)):
        if ok.sum()==0: continue
        for ch in range(3): arr[:,ch]=np.interp(xs,xs[ok],arr[ok,ch])
    # 平滑横向
    A=cv2.GaussianBlur(A[None],(0,0),1.5,sigmaY=0.01)[0] if pw>3 else A
    B=cv2.GaussianBlur(B[None],(0,0),1.5,sigmaY=0.01)[0] if pw>3 else B
    for x in xs[cols]:
        t,b=int(tops[x]),int(bots[x])
        for y in range(t,b+1):
            w=min(1.0,(y-t+1)/3.5); w=w*w*(3-2*w); clean[y,x]=A[x]*(1-w)+B[x]*w
    return clean
def blink_eye(img,e,c,thin=0.72):
    """img float BGR 0..255 (modified copy returned for box); c in 0..1"""
    x0,y0,x1,y1=e['box']; P=img[y0:y1,x0:x1]/255.; ph,pw=P.shape[:2]
    M=poly_mask(e['mask'],x0,y0,(ph,pw))
    Mb=(M>0.02).astype(np.uint8)
    g=P@LUM
    # clean skin: 只用 mask 外、亮的、偏暖的像素
    skin=(g>0.80)&(P[...,2]>P[...,0]-0.005)&(cv2.dilate(Mb,np.ones((3,3),np.uint8))==0)
    clean=fill_cols(P,Mb,skin)
    gc=clean@LUM
    # 原上睫毛浓度 alpha
    LM=poly_mask(e['lash'],x0,y0,(ph,pw))
    blue=np.clip(((P[...,0]-P[...,2])-0.01)/0.06,0,1)
    core=np.percentile(g[LM>0.5],8)
    a=np.clip((gc-g)/np.maximum(gc-core,0.15),0,1)*(1-blue)*LM
    a=np.clip((a-0.06)/0.94,0,1)
    acol=a>0.7
    lashc=np.median(P[acol],0) if acol.sum()>3 else P[LM>0.5].min(0)
    colr=np.clip((P-(1-a[...,None])*clean)/np.maximum(a[...,None],0.3),0,1)
    w=np.clip((a-0.3)/0.5,0,1)[...,None]; colr=colr*w+lashc*(1-w)
    xs=np.arange(x0,x1,dtype=np.float32)
    xa,xb=e['xr']; inx=(xs>=xa)&(xs<=xb)
    yo=np.where(inx,cy(e['open'],xs),0); ys=np.where(inx,cy(e['shut'],xs),0)
    # 眼角处权重渐变（外眼角睫毛团原地不动）
    yc=yo+(ys-yo)*c
    s=1-(1-thin)*c          # 厚度缩放
    Y=np.arange(ph,dtype=np.float32)[:,None]+y0
    # 采样：新位置 y -> 原位置 yo + (y-yc)/s
    srcY=(yo[None,:]+(Y-yc[None,:])/s)-y0
    X=np.tile(np.arange(pw,dtype=np.float32)[None,:],(ph,1))
    srcY=np.where(inx[None,:],srcY,Y-y0).astype(np.float32)
    a2=cv2.remap(a,X,srcY,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
    c2=cv2.remap(colr,X,srcY,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    # 底：移动后睫毛中心线以上 = 干净皮肤；以下 = 原图（露出的虹膜下半）；快闭死全部干净
    above=np.clip(yc[None,:]+1.0-Y,0,1)
    k=float(np.clip((c-0.6)/0.35,0,1)); k=k*k*(3-2*k)
    A=np.clip(above+(1-above)*k,0,1)*M
    A=np.where(inx[None,:],A,M*k) if False else A
    base=P*(1-A[...,None])+clean*A[...,None]
    out=base*(1-a2[...,None])+c2*a2[...,None]
    # 只在 mask（略外扩）内生效，外面逐像素不变
    Mo=np.clip(cv2.GaussianBlur(cv2.dilate(Mb,np.ones((3,3),np.uint8)).astype(np.float32),(0,0),0.6)*1.2,0,1)
    if c<=0: return img[y0:y1,x0:x1]
    res=P*(1-Mo[...,None])+out*Mo[...,None]
    return res*255
def apply(img,c,dxy=None):
    if c<=0.001: return img
    out=img.copy()
    for k,e in EYES.items():
        x0,y0,x1,y1=e['box']
        out[y0:y1,x0:x1]=blink_eye(img,e,c)
    return out
