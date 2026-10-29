"""달려라 밤톨! — Original, asset-free Korean rooftop runner.

Deploy: streamlit run app.py
No image files, Node, or extra Python libraries are required.
"""

import streamlit as st

st.set_page_config(
    page_title="달려라 밤톨! | 달빛 지붕 달리기",
    page_icon="🐹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp { background: radial-gradient(ellipse at 45% 0%, #172e44 0%, #0a1423 48%, #080d17 100%); }
    .block-container { max-width: 1330px; padding-top: 1.35rem; padding-bottom: 1.2rem; }
    h1, p { color: #f4ecdc; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #102033; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align:center; margin:0; color:#ffe9ad; "
    "font-size:clamp(1.8rem,4vw,3rem); letter-spacing:-.04em'>"
    "🐹 달려라 밤톨! <span style='color:#ffc16e'>달빛 지붕 대모험</span></h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; margin:.2rem 0 .8rem; color:#b8c9d7'>"
    "구덩이를 뛰어넘고 · 갈고리로 탑을 타고 · 왕고양이에게 신기록을 보여줘!"
    "</p>",
    unsafe_allow_html=True,
)

# All gameplay and artwork live in this standalone HTML/Canvas/JavaScript bundle.
# Streamlit only hosts it; JavaScript runs in the player's browser at 60 FPS.
GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>달려라 밤톨!</title>
<style>
  :root { color-scheme:dark; --gold:#ffd17a; --ink:#102638; --cream:#fff2d4; }
  * { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
  html,body { margin:0; padding:0; width:100%; background:transparent; color:#fff6e1;
    font-family:system-ui,-apple-system,"Malgun Gothic","Apple SD Gothic Neo",sans-serif; overflow:hidden; }
  .wrapper { width:100%; max-width:1200px; margin:0 auto; }
  .frame { position:relative; width:100%; aspect-ratio:1200 / 675; isolation:isolate;
    overflow:hidden; border:3px solid #7c6548; border-radius:20px;
    background:#081727; box-shadow:0 14px 0 #182337,0 20px 40px #0008,inset 0 0 45px #000; }
  canvas { display:block; width:100%; height:100%; outline:none; touch-action:manipulation; }
  .screen { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
    justify-content:center; text-align:center; padding:20px; z-index:5;
    background:linear-gradient(180deg,#07172bbb 0%,#101d31a8 70%,#0a172ad0 100%); }
  .hidden { display:none !important; }
  .eyebrow { font-size:clamp(11px,1.5vw,18px); letter-spacing:.36em; color:#ffdda2;
    font-weight:800; text-shadow:0 2px 10px #0009; }
  .headline { margin:8px 0 0; font-weight:1000; font-size:clamp(40px,7.5vw,98px);
    letter-spacing:-.1em; line-height:1.1; color:#ffe5a1;
    -webkit-text-stroke:1px #845229; text-shadow:0 5px 0 #a75d37,0 9px 0 #583b32,0 14px 25px #000; }
  .headline .orange { color:#ffad65; }
  .subline { margin:20px 0 24px; font-size:clamp(12px,1.6vw,20px); color:#f8ecd3;
    line-height:1.5; text-shadow:0 2px 6px #000; }
  .mainbtn { border:2px solid #fff0c1; border-radius:999px; background:linear-gradient(#ffde85,#f59e50);
    color:#613b30; font-weight:1000; font-size:clamp(15px,1.8vw,22px); padding:13px 34px;
    cursor:pointer; box-shadow:0 6px 0 #974b34,0 12px 22px #0008; transition:transform .1s; }
  .mainbtn:hover { filter:brightness(1.07); transform:translateY(-2px); }
  .mainbtn:active { transform:translateY(4px); box-shadow:0 2px 0 #974b34; }
  .keyline { color:#dfcfb2; margin-top:22px; line-height:1.75;
    font-size:clamp(10px,1.18vw,14px); max-width:680px; }
  kbd { background:#20364c; color:#fff1ce; padding:3px 9px; border:1px solid #8193a5;
    border-bottom-width:3px; border-radius:6px; font:inherit; font-weight:800; white-space:nowrap; }
  #toolbar { position:absolute; top:16px; left:16px; z-index:3; display:flex; gap:8px; }
  .roundbtn { background:#142e45df; color:#ffedc6; border:1.5px solid #9b9a8d;
    width:39px; height:39px; border-radius:13px; cursor:pointer; font-size:19px;
    box-shadow:0 3px 0 #07121a; }
  .roundbtn:hover { background:#28526b; }
  .toast { position:absolute; z-index:4; top:29%; left:50%; transform:translateX(-50%);
    background:#132337e8; border:2px solid #ffc77c; box-shadow:0 5px 20px #0009;
    color:#fff2cb; padding:9px 18px; border-radius:999px;
    font-weight:900; font-size:clamp(13px,2.4vw,28px); text-shadow:0 2px 5px #000;
    pointer-events:none; white-space:nowrap; }
  #actionHint { position:absolute; z-index:2; bottom:15px; left:50%; transform:translateX(-50%);
    color:#ffe3a4; background:#142b3ab5; padding:6px 15px; border-radius:18px;
    font-size:clamp(11px,1.15vw,14px); text-align:center; pointer-events:none;
    border:1px solid #b9a16855; max-width:80%; }
  .touch { position:absolute; z-index:3; bottom:17px; right:18px; display:flex; gap:12px; }
  .touch button { border:2px solid #ffedc1; background:#18344ce0; color:#ffe4b6;
    border-radius:50%; width:78px; height:78px; font-size:12px; font-weight:900;
    box-shadow:0 5px 0 #0b1724; cursor:pointer; touch-action:none; }
  .touch button span { display:block; font-size:29px; }
  .touch button:active { transform:translateY(3px); }
  #end .stats { display:flex; gap:18px; justify-content:center; flex-wrap:wrap;
    margin:10px 0 24px; }
  #end .stat { background:#091928c9; border:1px solid #ba9063; min-width:125px;
    border-radius:14px; padding:11px 20px; }
  #end .stat strong { display:block; font-size:clamp(24px,3.8vw,42px); color:#ffe09c; }
  #end .stat small { color:#c5ced4; font-weight:800; }
  .below { display:flex; justify-content:space-between; gap:12px; align-items:center;
    color:#c7d1d8; padding:16px 3px 3px; font-size:clamp(11px,1.25vw,15px); }
  .below strong { color:#ffda94; }
  .below .tag { color:#efc8a1; white-space:nowrap; }
  @media (max-width:650px) {
    .frame { border-width:2px; border-radius:12px; }
    #toolbar { top:8px; left:8px; gap:5px; }
    .roundbtn { width:31px; height:31px; border-radius:9px; font-size:15px; }
    .touch { bottom:8px; right:8px; gap:6px; }
    .touch button { width:54px; height:54px; font-size:9px; }
    .touch button span { font-size:18px; }
    #actionHint { display:none; }
    .subline { margin:6px 0 12px; }
    .headline { margin:0; }
    .keyline { margin-top:11px; }
    .mainbtn { padding:8px 22px; }
    #end .stats { margin:5px 0 11px; gap:7px; }
    #end .stat { min-width:90px; padding:6px 10px; }
    .below { padding:10px 2px; }
  }
</style>
</head>
<body>
<div class="wrapper">
  <div class="frame" id="frame">
    <canvas id="game" width="1200" height="675" tabindex="0" aria-label="기니피그 밤톨의 자동 달리기 게임"></canvas>
    <div id="toolbar">
      <button class="roundbtn" id="pauseBtn" title="일시정지(P)">Ⅱ</button>
      <button class="roundbtn" id="soundBtn" title="효과음 켜기·끄기">♫</button>
    </div>
    <div class="screen" id="cover">
      <div class="eyebrow">달빛 아래 펼쳐지는 대모험</div>
      <h1 class="headline">달려라 <span class="orange">밤톨!</span></h1>
      <div class="subline">🐹 쪼꼬만 기니피그, 누구보다 멀리 달려라!</div>
      <button class="mainbtn" id="startBtn">▶ 모험 시작!</button>
      <div class="keyline"><kbd>SPACE</kbd> 점프 · 두 번 누르면 더블점프<br>
      <kbd>더블클릭</kbd> / <kbd>E</kbd> 갈고리 발사 · <kbd>P</kbd> 일시정지</div>
    </div>
    <div class="screen hidden" id="pauseScreen">
      <div class="eyebrow">잠깐 쉬었다 가자!</div>
      <h2 class="headline" style="font-size:clamp(34px,6vw,75px)">일시정지</h2>
      <div class="subline">밤톨이가 숨을 고르고 있어요 🐹</div>
      <button class="mainbtn" id="resumeBtn">▶ 이어 달리기</button>
    </div>
    <div class="screen hidden" id="end">
      <div class="eyebrow" id="resultLabel">왕고양이의 기록 발표</div>
      <h2 class="headline" style="font-size:clamp(33px,6.5vw,78px)">아이고, 밤톨아!</h2>
      <p class="subline" style="margin:12px 0">구덩이에 퐁당! 다음엔 더 멀리 갈 수 있어.</p>
      <div class="stats">
        <div class="stat"><strong id="finalScore">0</strong><small>이번 점수</small></div>
        <div class="stat"><strong id="finalBest">0</strong><small>최고 기록</small></div>
        <div class="stat"><strong id="finalFish">0</strong><small>모은 붕어빵</small></div>
      </div>
      <button class="mainbtn" id="restartBtn">↻ 다시 도전!</button>
    </div>
    <div id="toast" class="toast hidden"></div>
    <div id="actionHint" class="hidden">🏯 갈고리 탑 등장! 더블클릭 또는 E 키!</div>
    <div class="touch" id="touchControls">
      <button id="hookBtn" aria-label="갈고리 발사"><span>🪝</span>갈고리</button>
      <button id="jumpBtn" aria-label="점프"><span>🐾</span>점프</button>
    </div>
  </div>
  <div class="below">
    <div><strong>조작:</strong> Space 점프/더블점프 · 화면 더블클릭/E 탑 갈고리 · P 멈춤</div>
    <div class="tag">🎮 오리지널 캔버스 게임</div>
  </div>
</div>
<script>
'use strict';
// Canvas runner: no remote images, audio or game-engine dependencies.
(() => {
  const W = 1200, H = 675, FLOOR = 538;
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d', {alpha:false});
  const $ = id => document.getElementById(id);
  const cover=$('cover'), paused=$('pauseScreen'), end=$('end');
  const hint=$('actionHint'), toast=$('toast');
  const TAU=Math.PI*2, clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
  const lerp=(a,b,t)=>a+(b-a)*t;
  const ease=t=>t*t*(3-2*t);
  const hash=n=>{const s=Math.sin(n*127.1+11.7)*43758.5453;return s-Math.floor(s);};
  const world={ platforms:[], towers:[], coins:[], count:0, seed:0 };
  let rng=()=>Math.random(), mode='menu', clock=0, framePrev=0;
  let elapsed=0, camera=0, speed=275, score=0, best=0, fish=0, towersPassed=0;
  let boosted=false, extraRush=0, rushFlash=0, grapple=null, shake=0;
  let particles=[], texts=[], nextToastEnd=0, lastTap=0;
  let soundOn=true, audioCtx=null, lastDbl=0;
  let player={x:165,y:FLOOR,vy:0,grounded:true,jumps:0,coyote:0,blink:0};

  function readBest(){ try{return Number(localStorage.getItem('bamtol-best-v2'))||0;}catch(e){return 0;} }
  function saveBest(v){ try{localStorage.setItem('bamtol-best-v2',String(v));}catch(e){} }
  best=readBest();
  function rand(){return rng();}
  function seeded(seed){ let a=seed|0;return ()=>{a+=0x6D2B79F5;let t=a;
      t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);
      return ((t^(t>>>14))>>>0)/4294967296; }; }
  function resetWorld(){
    world.platforms.length=0;world.towers.length=0;world.coins.length=0;
    world.count=0;world.seed=Math.floor(Math.random()*1e8);rng=seeded(world.seed);
    world.platforms.push({start:-800,end:900});
    addCoins(-50,900);
    while(world.platforms[world.platforms.length-1].end<3200) generateMore();
    particles=[];texts=[];
    player={x:165,y:FLOOR,vy:0,grounded:true,jumps:0,coyote:0,blink:0};
    camera=0;elapsed=0;speed=275;score=0;fish=0;towersPassed=0;
    boosted=false;extraRush=0;rushFlash=0;grapple=null;shake=0;
  }
  function addCoins(start,end){
    for(let x=Math.max(220,start+130);x<end-85;x+=110+rand()*35){
      world.coins.push({x,y:FLOOR-62-(rand()>.76?72:0),taken:false,wave:rand()*TAU});
    }
  }
  function generateMore(){
    const last=world.platforms[world.platforms.length-1];
    world.count++;
    const huge=world.count%5===0;
    const gap=huge?(485+rand()*55):(115+rand()*86);
    const start=last.end+gap;
    const length=huge?(590+rand()*130):(490+rand()*185);
    world.platforms.push({start,end:start+length});
    addCoins(start,start+length);
    if(huge){
      const t={x:last.end+gap*.49,top:270,used:false,id:world.count};
      world.towers.push(t);
      // Attract the player toward the tower with a visible trail of treats.
      for(let j=0;j<3;j++) world.coins.push({x:last.end+60+j*75,y:FLOOR-120-j*31,taken:false,wave:rand()*TAU});
    } else if(rand()>.45) {
      for(let j=0;j<3;j++)world.coins.push({x:last.end+gap*.2+j*gap*.27,y:FLOOR-115-j*24,taken:false,wave:rand()*TAU});
    }
  }
  function groundAt(x){for(const s of world.platforms){if(x>=s.start&&x<=s.end)return true;}return false;}
  function nextTower(){return world.towers.filter(t=>!t.used&&t.x-player.x>-80&&t.x-player.x<430)
    .sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x))[0];}
  function showToast(t,ms=1400){toast.textContent=t;toast.classList.remove('hidden');nextToastEnd=performance.now()+ms;}
  function setOverlay(which){cover.classList.toggle('hidden',which!=='menu');
    paused.classList.toggle('hidden',which!=='paused');end.classList.toggle('hidden',which!=='dead');}
  function focusGame(){try{canvas.focus({preventScroll:true});}catch(e){canvas.focus();}}
  function start(){resetWorld();mode='running';setOverlay('running');focusGame();
    showToast('🐹 밤톨이 출발! 달려라!',1500);sound('start');}
  function togglePause(){
    if(mode==='running'){mode='paused';setOverlay('paused');}
    else if(mode==='paused'){mode='running';setOverlay('running');focusGame();}
  }
  function die(){
    if(mode!=='running')return;
    mode='dead';grapple=null;setOverlay('dead');sound('fall');shake=13;
    if(score>readBest()){best=score;saveBest(best);$('resultLabel').textContent='👑 왕고양이도 놀란 신기록!';}
    else $('resultLabel').textContent='왕고양이의 기록 발표';
    $('finalScore').textContent=score.toLocaleString('ko-KR');
    $('finalBest').textContent=best.toLocaleString('ko-KR');
    $('finalFish').textContent=String(fish);
  }
  function jump(){
    if(mode==='menu'||mode==='dead'){start();return;}
    if(mode!=='running'||grapple)return;
    const grounded=player.grounded||player.coyote>0;
    if(grounded){player.vy=-675;player.grounded=false;player.coyote=0;player.jumps=1;
      puff(player.x,player.y-8,8,'#d6e7e8');sound('jump');}
    else if(player.jumps<2){player.vy=-645;player.jumps=2;
      puff(player.x,player.y-38,14,'#ffe28d');sound('double');
      texts.push({x:player.x,y:player.y-100,label:'더블 점프!',life:.9,color:'#ffe08d'});
    }
  }
  function hook(){
    if(mode!=='running'||grapple)return;
    const t=nextTower();
    if(!t){showToast('🏯 탑 가까이에서 갈고리를 사용해!',1150);return;}
    t.used=true;towersPassed++;
    grapple={tower:t,phase:'shoot',timer:0,fromX:player.x,fromY:player.y-52,
      initialX:player.x,initialY:player.y,hookTip:0};
    player.grounded=false;player.vy=0;player.coyote=0;
    sound('hook');puff(player.x,player.y-42,7,'#ffb85a');
    showToast('🪝 갈고리 발사! 탑을 올라가자!',1150);
  }
  function puff(x,y,n,color){
    for(let i=0;i<n;i++){const a=rand()*TAU,v=35+rand()*180;
      particles.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-40,life:.32+rand()*.55,
        max:.85,size:2+rand()*5,color,grav:170});}
  }
  function speedParticles(){
    for(let i=0;i<2;i++) particles.push({x:player.x-10,y:player.y-18-rand()*65,
      vx:-250-rand()*300,vy:(rand()-.5)*30,life:.18+rand()*.2,max:.4,
      size:1.5+rand()*3,color:rand()>.5?'#f3cf89':'#b0e3e5',grav:0});
  }
  function update(dt){
    clock+=dt;
    if(nextToastEnd && performance.now()>nextToastEnd){toast.classList.add('hidden');nextToastEnd=0;}
    if(mode!=='running')return;
    elapsed+=dt;
    if(!boosted&&elapsed>=9.5){boosted=true;rushFlash=2.3;shake=7;
      sound('boost');showToast('💨 휘이이잉! 가속 시작!',2200);}
    const target=elapsed<9.5?275+elapsed*2.4:Math.min(880,370+(elapsed-9.5)*9.8);
    speed+=(target-speed)*Math.min(1,dt*2.4);
    extraRush=Math.max(0,extraRush-dt);
    rushFlash=Math.max(0,rushFlash-dt);shake=Math.max(0,shake-dt*12);

    const prevY=player.y;
    if(grapple){
      const g=grapple,t=g.tower;
      g.timer+=dt;
      if(g.phase==='shoot'){
        g.hookTip=clamp(g.timer/.23,0,1);
        player.x+=speed*dt*.35;player.y-=24*dt;
        if(g.timer>=.23){g.phase='climb';g.timer=0;g.fromX=player.x;g.fromY=player.y;}
      }else if(g.phase==='climb'){
        const r=ease(clamp(g.timer/.80,0,1));
        player.x=lerp(g.fromX,t.x-58,r);
        player.y=lerp(g.fromY,t.top+18,r)-Math.sin(r*Math.PI)*15;
        if(rand()<dt*20)puff(t.x-50,player.y-35,2,'#ffdf80');
        if(g.timer>=.80){
          player.x=t.x+36;player.y=t.top+9;player.vy=-375;
          grapple=null;extraRush=1.2;shake=5;
          puff(player.x,player.y-38,20,'#ffe3a0');sound('release');
          texts.push({x:player.x,y:player.y-80,label:'탑 돌파 +300!',life:1.3,color:'#ffe49c'});
        }
      }
    }else{
      player.x+=(speed+(extraRush>0?90:0))*dt;
      if(player.grounded&&!groundAt(player.x)){
        player.grounded=false;player.coyote=.115;player.vy=0;
      }
      if(!player.grounded){
        player.coyote=Math.max(0,player.coyote-dt);
        player.vy=Math.min(1350,player.vy+1670*dt);
        player.y+=player.vy*dt;
        if(player.vy>=0&&prevY<=FLOOR&&player.y>=FLOOR&&groundAt(player.x)){
          player.y=FLOOR;player.vy=0;player.grounded=true;player.jumps=0;
          if(rand()>.6)puff(player.x,player.y,3,'#a5cbd2');
        }
      }else{player.y=FLOOR;player.jumps=0;}
    }
    if(player.y>H+125){die();return;}
    camera+=(Math.max(0,player.x-265)-camera)*Math.min(1,dt*7.0);
    while(world.platforms[world.platforms.length-1].end<player.x+2700)generateMore();
    if(world.platforms.length>22){
      const cutoff=player.x-1700;
      world.platforms=world.platforms.filter(s=>s.end>cutoff);
      world.coins=world.coins.filter(c=>c.x>cutoff&&!c.taken);
      world.towers=world.towers.filter(t=>t.x>cutoff);
    }
    for(const c of world.coins){
      if(c.taken)continue;
      if(Math.abs(c.x-player.x)<39&&Math.abs(c.y-(player.y-47))<54){
        c.taken=true;fish++;puff(c.x,c.y,10,'#ffd06c');sound('coin');
        texts.push({x:c.x,y:c.y-18,label:'+100',life:.8,color:'#ffdf84'});
      }
    }
    score=Math.max(0,Math.floor((player.x-165)*.54+fish*100+towersPassed*300));
    if(score>best){best=score;}
    hint.classList.toggle('hidden',!(nextTower()&&!grapple));
    if(boosted&&rand()<dt*30)speedParticles();
    if(player.grounded&&rand()<dt*18)puff(player.x-26,FLOOR-4,1,'#9fadb1');
    for(const p of particles){p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.grav*dt;p.life-=dt;}
    particles=particles.filter(p=>p.life>0).slice(-140);
    for(const t of texts){t.y-=44*dt;t.life-=dt;}
    texts=texts.filter(t=>t.life>0);
  }
  function path(points){ctx.beginPath();ctx.moveTo(points[0][0],points[0][1]);
    for(let i=1;i<points.length;i++)ctx.lineTo(points[i][0],points[i][1]);ctx.closePath();}
  function rect(x,y,w,h,color){ctx.fillStyle=color;ctx.fillRect(x,y,w,h);}
  function ellipse(x,y,rx,ry,color,rot=0){ctx.beginPath();ctx.ellipse(x,y,rx,ry,rot,0,TAU);ctx.fillStyle=color;ctx.fill();}
  function round(x,y,w,h,r,color){ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();}
  function line(x1,y1,x2,y2,color,width=2){ctx.strokeStyle=color;ctx.lineWidth=width;
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();}
  function roof(x,y,w,h,c1,c2){
    ctx.fillStyle=c1;path([[x-w*.61,y+15],[x-w*.52,y-3],[x,y-h],[x+w*.52,y-3],[x+w*.61,y+15],
      [x+w*.43,y+9],[x,y-h*.30],[x-w*.43,y+9]]);ctx.fill();
    ctx.strokeStyle=c2;ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x-w*.60,y+13);
    ctx.quadraticCurveTo(x-w*.18,y-15,x,y-h);ctx.quadraticCurveTo(x+w*.25,y-17,x+w*.60,y+13);ctx.stroke();
    ellipse(x,y-h,5,5,'#e3ab65');
  }
  function drawSky(){
    const grad=ctx.createLinearGradient(0,0,0,H);grad.addColorStop(0,'#08172e');
    grad.addColorStop(.54,'#0b3450');grad.addColorStop(1,'#24625d');
    rect(0,0,W,H,grad);
    // Moon and soft rings.
    const mx=875-camera*.018, my=126;
    const glow=ctx.createRadialGradient(mx,my,18,mx,my,255);
    glow.addColorStop(0,'#f7edd399');glow.addColorStop(.36,'#b3d7df36');glow.addColorStop(1,'#8ad0ce00');
    ellipse(mx,my,255,255,glow);
    ellipse(mx,my,101,101,'#cce6e0');ellipse(mx-5,my-6,95,95,'#e2eedd');
    for(let i=0;i<9;i++){const ox=hash(i+41)*145-70,oy=hash(i+90)*144-70;
      ellipse(mx+ox,my+oy,7+hash(i+5)*19,6+hash(i+5)*9,'#b4d4d132');}
    for(let i=0;i<88;i++){
      const x=((hash(i+220)*W-camera*.012)%W+W)%W;
      const y=18+hash(i+450)*365;const a=.27+Math.sin(clock*2+i*9)*.18;
      ctx.globalAlpha=a;ellipse(x,y,hash(i+700)*1.5+1,hash(i+700)*1.5+1,'#def9ee');ctx.globalAlpha=1;
    }
    // Drifting clouds in three translucent puffs.
    for(let i=0;i<11;i++){
      const x=((i*203+hash(i+4)*200-camera*(.10+hash(i+28)*.05))%(W+400)+(W+400))%(W+400)-150;
      const y=105+hash(i+15)*270;ctx.globalAlpha=.20;
      ellipse(x,y,79,22,'#a8d5de');ellipse(x-34,y-17,46,27,'#a8d5de');
      ellipse(x+12,y-28,50,37,'#a8d5de');ellipse(x+63,y-9,44,24,'#a8d5de');ctx.globalAlpha=1;
    }
    // Distant jagged hills.
    ctx.fillStyle='#123b4c';ctx.beginPath();ctx.moveTo(0,480);
    for(let x=0;x<=W+30;x+=23){let y=420+hash(Math.floor((x+camera*.07)/43)+155)*76;
      ctx.lineTo(x,y);}ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.fill();
    // Parallax city / pagoda rooftops.
    for(let i=-1;i<15;i++){
      const x=i*124-((camera*.20)%124),by=475+hash(i+300)*85;
      rect(x+10,by-12,95,H-by,'#102d3b');
      roof(x+55,by,102,41,'#173e4a','#285763');
      if(i%3===0){rect(x+33,by-88,52,70,'#112e3b');roof(x+60,by-82,85,34,'#1a4550','#315b66');
        ellipse(x+58,by-48,5,8,'#a6a463');}
      if(i%2===0)for(let j=0;j<2;j++)round(x+26+j*36,by+16,10,16,3,'#dca95d50');
    }
  }
  function drawPitGlow(){
    const g=ctx.createLinearGradient(0,FLOOR,0,H);
    g.addColorStop(0,'#03131c');g.addColorStop(1,'#010609');
    rect(0,FLOOR,W,H-FLOOR,g);
    for(let i=0;i<23;i++){
      const x=((hash(i+41)*1500-camera*.33)%(W+110)+(W+110))%(W+110)-35;
      ellipse(x,585+Math.sin(clock+i)*10,25+hash(i+21)*70,9,'#72d5c211');
    }
  }
  function drawGround(){
    for(const s of world.platforms){
      const l=s.start-camera,r=s.end-camera;
      if(r< -30||l>W+30)continue;
      const x=Math.max(-20,l),right=Math.min(W+25,r);
      rect(x,FLOOR+5,right-x,H-FLOOR,'#11272e');
      rect(x,FLOOR+5,right-x,15,'#c5aa74');
      rect(x,FLOOR+20,right-x,6,'#4d6770');
      for(let xx=Math.floor(l/37)*37+18-camera;xx<right;xx+=37){
        if(xx<x-40)continue;
        line(xx,FLOOR+27,xx+16,FLOOR+59,'#294a50',3);
        line(xx+15,FLOOR+27,xx+30,FLOOR+59,'#0a1721',2);
      }
      for(let xx=Math.floor(l/83)*83+20-camera;xx<right;xx+=83){
        if(xx<x-90)continue;
        rect(xx,FLOOR+84,42,7,'#1c3940');
        rect(xx+13,FLOOR+100,5,22,'#557d7355');
      }
      // The hanging moss at cliff edges makes gaps readable.
      if(l>0&&l<W){rect(l,FLOOR,8,92,'#e4b873');ellipse(l+7,FLOOR+15,9,7,'#dac582');}
      if(r>0&&r<W){rect(r-8,FLOOR,8,92,'#d6a46a');ellipse(r-7,FLOOR+15,9,7,'#e8c683');}
    }
  }
  function drawTower(t){
    const x=t.x-camera;if(x< -220||x>W+220)return;
    ctx.save();
    // Base, wall bricks, gold windows.
    rect(x-54,315,108,315,'#4f5552');rect(x-47,320,94,306,'#7f6b56');
    for(let y=333;y<610;y+=22){line(x-49,y,x+49,y,'#574d48',2);
      for(let xx=x-45+(Math.floor(y/22)%2)*18;xx<x+47;xx+=35)line(xx,y,xx,y+21,'#5a4d45',1.5);}
    for(let y=363;y<=540;y+=78){
      round(x-18,y-13,36,54,15,'#302c35');round(x-10,y-4,20,37,9,'#ffd277');
      line(x,y-2,x,y+30,'#7f5849',3);
    }
    for(let layer=2;layer>=0;layer--){
      const y=471-layer*83,w=164-layer*20;
      rect(x-w*.32,y+10,w*.64,37,'#634d4b');
      line(x-w*.3,y+20,x+w*.3,y+20,'#ac8560',5);
      roof(x,y,w,47,'#223e52','#efbe75');
      for(let j=-1;j<=1;j++)ellipse(x+j*29,y+29,5,9,'#e1a45e');
    }
    // Tower top and sparkle marking the usable anchor.
    line(x,262,x,222,'#ffda89',4);ellipse(x,220,9,9,'#ffe19c');
    const a=1+Math.sin(clock*4+t.id)*.20;
    ctx.globalAlpha=t.used?.25:.75;
    ellipse(x+12,285,24*a,24*a,'#ffe89c31');
    ellipse(x+12,285,9*a,9*a,'#ffe69e');ctx.globalAlpha=1;
    ctx.font='bold 16px system-ui';ctx.textAlign='center';
    ctx.fillStyle='#fbe3a3';ctx.fillText('갈고리 탑',x,196);
    ctx.restore();
  }
  function drawWarning(){
    for(let i=0;i<world.platforms.length-1;i++){
      const a=world.platforms[i],b=world.platforms[i+1];
      const x=a.end-camera;
      if(x<0||x>W+100)continue;
      const huge=b.start-a.end>400;
      const height=huge?87:55;
      line(x-40,FLOOR-height,x-40,FLOOR-2,'#ddc49e',5);
      round(x-80,FLOOR-height-46,80,44,8,huge?'#9c4550':'#896744');
      ctx.strokeStyle='#f6d99f';ctx.lineWidth=2;
      ctx.strokeRect(x-76,FLOOR-height-43,71,37);
      ctx.fillStyle='#fff0c7';ctx.textAlign='center';ctx.font='bold 19px system-ui';
      ctx.fillText(huge?'위험!':'조심!',x-40,FLOOR-height-17);
      if(huge){ctx.font='bold 15px system-ui';ctx.fillStyle='#ffbfa4';
        ctx.fillText('🪝',x-40,FLOOR-height-53);}
    }
  }
  function drawTreat(c){
    if(c.taken)return;const x=c.x-camera;
    if(x< -40||x>W+40)return;
    const y=c.y+Math.sin(clock*4+c.wave)*5;
    ctx.save();ctx.translate(x,y);ctx.rotate(Math.sin(clock*2+c.wave)*.12);
    ellipse(0,2,20,16,'#f0a94e');ellipse(0,-1,18,13,'#ffcf7d');
    ctx.fillStyle='#f8c46a';path([[10,-8],[26,-18],[25,17],[10,9]]);ctx.fill();
    ellipse(-10,-5,3,3,'#78503a');
    for(let j=-1;j<=1;j++)line(j*5-1,8,j*5+4,12,'#b56e33',1.5);
    ellipse(-2,-6,22,19,'#ffe5a222');ctx.restore();
  }
  function drawParticles(){
    for(const p of particles){const x=p.x-camera;if(x<-60||x>W+60)continue;
      ctx.globalAlpha=clamp(p.life/p.max,0,1);ellipse(x,p.y,p.size,p.size,p.color);
    }ctx.globalAlpha=1;
    for(const t of texts){const x=t.x-camera;
      ctx.globalAlpha=clamp(t.life,0,1);ctx.font='900 22px system-ui';ctx.textAlign='center';
      ctx.strokeStyle='#0b2436';ctx.lineWidth=5;ctx.strokeText(t.label,x,t.y);
      ctx.fillStyle=t.color;ctx.fillText(t.label,x,t.y);
    }ctx.globalAlpha=1;
  }
  function drawRope(){
    if(!grapple)return;
    const g=grapple,x1=player.x-camera,y1=player.y-44;
    const x2=g.tower.x+12-camera,y2=285;
    const f=g.phase==='shoot'?g.hookTip:1;
    const ex=lerp(x1,x2,f),ey=lerp(y1,y2,f);
    ctx.strokeStyle='#10232c';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(ex,ey);ctx.stroke();
    ctx.strokeStyle='#f9cb6c';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(ex,ey);ctx.stroke();
    ctx.save();ctx.translate(ex,ey);ctx.rotate(Math.atan2(ey-y1,ex-x1)+Math.PI/2);
    line(0,0,0,19,'#dce9ec',5);line(0,19,-11,10,'#dce9ec',4);line(0,19,11,10,'#dce9ec',4);
    ctx.restore();
  }
  function drawGuineaPig(){
    const x=player.x-camera,y=player.y;
    // Soft ground shadow, even while flying.
    const lift=Math.max(0,FLOOR-y);
    ctx.globalAlpha=clamp(.30-lift/900,.05,.3);
    ellipse(x,FLOOR+6,45+lift*.04,8,'#061218');ctx.globalAlpha=1;
    ctx.save();ctx.translate(x,y);
    const run=clock*(12+speed/35);
    const leap=!player.grounded||!!grapple;
    const bob=leap?-2:Math.sin(run*2)*2.4;
    ctx.translate(0,bob);
    ctx.rotate(leap?clamp(player.vy/2600,-.16,.14):Math.sin(run)*.025);
    // Scarf and tiny fluttering cape.
    ctx.fillStyle='#d65b52';
    path([[-22,-72],[-43-(boosted?12:0),-65+Math.sin(run)*6],[-32,-45],[-17,-45]]);ctx.fill();
    // Back feet alternate while running.
    for(let j=0;j<2;j++){
      const xx=j?17:-14;const stride=leap?(j?10:-10):Math.sin(run+j*Math.PI)*11;
      ellipse(xx+stride, -4-(leap?9:Math.max(0,-stride*.22)),16,10,'#8a513a',stride*.016);
      ellipse(xx+stride+4,-4-(leap?9:Math.max(0,-stride*.22)),12,7,'#e1a27b');
    }
    // Round guinea pig torso / rump.
    ellipse(-4,-39,38,35,'#a65f3d');ellipse(11,-40,30,30,'#d58a56');
    ellipse(11,-34,24,24,'#ffe4ac');
    ellipse(-19,-50,19,21,'#a65b3e');
    // Harness buckle.
    round(-29,-40,61,8,4,'#aa4b47');round(-1,-45,17,17,5,'#f3c868');
    ellipse(7,-37,3,3,'#a9693e');
    // Front paws clasp a tiny adventure pouch.
    ellipse(23,-39,14,12,'#9f5e42');ellipse(26,-36,11,10,'#e5ae81');
    ellipse(-25,-35,13,12,'#ad6a4c');ellipse(-25,-34,9,8,'#edbc91');
    // Face: wide cream/chestnut color patches, characteristic guinea pig ears.
    ellipse(-21,-88,17,18,'#9b5e43',-.34);
    ellipse(21,-88,17,18,'#9b5e43',.34);
    ellipse(-21,-88,10,11,'#f3a8a0',-.34);
    ellipse(21,-88,10,11,'#f3a8a0',.34);
    ellipse(1,-72,39,33,'#d78d5d');
    ellipse(-14,-75,20,28,'#a65e3d',-.1);
    ellipse(14,-67,23,24,'#fff1c7',.1);
    ellipse(0,-54,20,15,'#fff0d3');
    ellipse(-16,-71,7,10,'#2b2528');ellipse(16,-71,7,10,'#2b2528');
    ellipse(-18,-75,2.5,3.5,'#fff');ellipse(14,-75,2.5,3.5,'#fff');
    ellipse(0,-57,5,3.5,'#a35f65');
    ctx.strokeStyle='#6e4641';ctx.lineWidth=1.8;
    ctx.beginPath();ctx.moveTo(0,-53);ctx.quadraticCurveTo(-6,-46,-10,-50);
    ctx.moveTo(0,-53);ctx.quadraticCurveTo(6,-46,10,-50);ctx.stroke();
    ellipse(-25,-56,8,5,'#eea69a80');ellipse(25,-56,8,5,'#eea69a80');
    for(let side of [-1,1]){
      line(side*11,-53,side*42,-57,'#f0d6b0',1.5);
      line(side*11,-50,side*39,-47,'#f0d6b0',1.5);
    }
    // Gold bell and tiny scarf knot.
    ellipse(-12,-45,7,7,'#f2d36f');ellipse(-12,-43,2,2,'#986942');
    if(boosted){
      // Speed tears and wind streak across the cute little face.
      ctx.globalAlpha=.65;ellipse(32,-71,3,5,'#a1e7ee');ctx.globalAlpha=1;
    }
    ctx.restore();
  }
  function drawRoyalCat(){
    // King cat is behind the scoreboard and holds it with both paws.
    const cx=1070;
    ctx.save();
    ellipse(cx+33,150,85,58,'#755042');
    ellipse(cx,88,58,53,'#bb8255');
    path([[cx-47,55],[cx-42,17],[cx-13,43]]);ctx.fillStyle='#bd845a';ctx.fill();
    path([[cx+22,44],[cx+51,13],[cx+54,65]]);ctx.fill();
    path([[cx-36,48],[cx-33,29],[cx-20,45]]);ctx.fillStyle='#dfab94';ctx.fill();
    path([[cx+34,44],[cx+45,25],[cx+46,53]]);ctx.fill();
    ellipse(cx-21,89,8,12,'#282b31');ellipse(cx+22,89,8,12,'#282b31');
    ellipse(cx-22,85,3,4,'#fff4df');ellipse(cx+21,85,3,4,'#fff4df');
    ellipse(cx,109,23,17,'#f9dcb9');ellipse(cx,106,6,5,'#7a5153');
    line(cx,111,cx-7,117,'#6f5250',2);line(cx,111,cx+7,117,'#6f5250',2);
    for(let side of [-1,1])for(let j=0;j<2;j++)line(cx+side*14,112+j*7,cx+side*55,109+j*11,'#dac1aa',1.5);
    // Crown on cat's head.
    path([[cx-27,49],[cx-34,10],[cx-13,24],[cx,1],[cx+15,25],[cx+38,7],[cx+30,49]]);
    ctx.fillStyle='#f7bf55';ctx.fill();
    rect(cx-27,44,57,11,'#efb65d');ellipse(cx,33,7,8,'#e85662');
    for(let dx of [-24,25])ellipse(cx+dx,20,5,5,'#f5e6b0');
    // Score panel with lacquer frame (in front of royal cat).
    round(837,128,348,118,19,'#6f462f');round(844,133,334,106,15,'#e7ad64');
    round(852,140,318,92,10,'#183b4b');
    ctx.strokeStyle='#f9df9b';ctx.lineWidth=2;ctx.strokeRect(864,148,294,76);
    ellipse(875,180,18,30,'#b8835d');ellipse(1154,180,18,30,'#b8835d');
    // Paws grip the wooden sign.
    ellipse(850,152,23,17,'#c18b61');ellipse(1168,152,23,17,'#c18b61');
    for(let px of [838,851,864,1156,1169,1182])ellipse(px,145,5,6,'#d8a47c');
    ctx.fillStyle='#f8dcb0';ctx.font='900 18px system-ui';ctx.textAlign='center';
    ctx.fillText('👑 왕고양이의 점수판',1010,168);
    ctx.font='900 32px system-ui';ctx.fillStyle='#ffe2a0';
    ctx.fillText(score.toLocaleString('ko-KR'),1004,205);
    ctx.font='bold 14px system-ui';ctx.fillStyle='#bfd2d3';
    ctx.fillText('최고 '+best.toLocaleString('ko-KR')+'  ·  🐟 '+fish,1005,223);
    ctx.restore();
  }
  function drawLeftHUD(){
    round(20,68,210,78,14,'#102736d9');
    ctx.strokeStyle='#c3a878';ctx.lineWidth=1.5;ctx.strokeRect(28,77,194,61);
    ctx.fillStyle='#ffdb91';ctx.textAlign='left';ctx.font='900 18px system-ui';
    ctx.fillText('🐹 밤톨이 달리기',43,101);
    ctx.font='bold 17px system-ui';ctx.fillStyle='#cbe6e0';
    ctx.fillText('속도  '+Math.round(speed/10)+' km/h',43,128);
    const bar=clamp((speed-250)/630,0,1);
    round(20,155,210,9,5,'#34505b');round(20,155,Math.max(8,210*bar),9,5,'#f3c16b');
    if(rushFlash>0){
      ctx.globalAlpha=Math.min(1,rushFlash/1.5);
      ctx.font='900 24px system-ui';ctx.fillStyle='#ffd38d';ctx.fillText('💨 휘이이잉!!',30,198);
      ctx.globalAlpha=1;
    }
    if(!player.grounded&&!grapple){
      ctx.font='900 16px system-ui';ctx.fillStyle=player.jumps<2?'#ffe9a8':'#9fb3c0';
      ctx.fillText(player.jumps<2?'★ 더블 점프 가능':'☆ 점프 사용 완료',28,236);
    }
  }
  function drawVignette(){
    const g=ctx.createRadialGradient(W/2,H/2,H*.27,W/2,H/2,W*.8);
    g.addColorStop(0,'#00000000');g.addColorStop(1,'#020913a1');rect(0,0,W,H,g);
    if(rushFlash>0){ctx.globalAlpha=.075*Math.min(1,rushFlash);
      rect(0,0,W,H,'#fbd99c');ctx.globalAlpha=1;}
    if(speed>380&&mode==='running'){
      ctx.globalAlpha=.10+Math.min(.12,(speed-380)/3000);
      for(let i=0;i<23;i++){
        const x=hash(i+100)*W, y=hash(i+200)*H;
        line(x,y,x-(speed/8+50),y+2,'#c9f0e6',1+hash(i+300)*1.5);
      }ctx.globalAlpha=1;
    }
  }
  function render(){
    ctx.clearRect(0,0,W,H);
    ctx.save();
    if(shake>0)ctx.translate((rand()-.5)*shake,(rand()-.5)*shake*.7);
    drawSky();drawPitGlow();
    for(const t of world.towers)drawTower(t);
    drawGround();drawWarning();
    for(const c of world.coins)drawTreat(c);
    drawParticles();drawRope();drawGuineaPig();
    drawVignette();drawLeftHUD();drawRoyalCat();
    ctx.restore();
  }
  function loop(now){
    const dt=framePrev?Math.min((now-framePrev)/1000,.033):.016;
    framePrev=now;
    update(dt);render();requestAnimationFrame(loop);
  }
  // Browser-synthesized effects: don't require loading any audio assets.
  function sound(name){
    if(!soundOn)return;
    try{
      const C=window.AudioContext||window.webkitAudioContext;
      if(!C)return;
      audioCtx=audioCtx||new C();if(audioCtx.state==='suspended')audioCtx.resume();
      const now=audioCtx.currentTime;
      const tone=(a,b,d,type='sine',vol=.09,delay=0)=>{
        const osc=audioCtx.createOscillator(),gain=audioCtx.createGain();
        osc.type=type;osc.frequency.setValueAtTime(a,now+delay);
        osc.frequency.exponentialRampToValueAtTime(Math.max(40,b),now+delay+d);
        gain.gain.setValueAtTime(.001,now+delay);
        gain.gain.exponentialRampToValueAtTime(vol,now+delay+.018);
        gain.gain.exponentialRampToValueAtTime(.001,now+delay+d);
        osc.connect(gain);gain.connect(audioCtx.destination);osc.start(now+delay);
        osc.stop(now+delay+d+.03);
      };
      if(name==='jump')tone(330,610,.16,'sine',.085);
      if(name==='double'){tone(460,930,.24,'triangle',.095);tone(700,1040,.17,'sine',.045,.08);}
      if(name==='coin'){tone(850,1150,.12,'sine',.06);tone(1080,1600,.13,'sine',.055,.08);}
      if(name==='hook'){tone(210,880,.30,'sawtooth',.075);}
      if(name==='release'){tone(540,920,.22,'triangle',.08);tone(790,1300,.19,'sine',.07,.11);}
      if(name==='boost'){tone(135,580,.54,'sawtooth',.07);tone(260,940,.54,'triangle',.045,.07);}
      if(name==='fall'){tone(610,140,.52,'triangle',.09);}
      if(name==='start'){tone(440,660,.15,'sine',.07);tone(580,880,.18,'sine',.07,.17);}
    }catch(e){/* Silent mode if browser audio is blocked. */}
  }
  // High-DPI rendering, stable game coordinates, and responsive CSS sizing.
  function resize(){const dpr=Math.min(window.devicePixelRatio||1,2);
    canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  resize();window.addEventListener('resize',resize);
  $('startBtn').addEventListener('click',start);
  $('restartBtn').addEventListener('click',start);
  $('resumeBtn').addEventListener('click',togglePause);
  $('pauseBtn').addEventListener('click',()=>{togglePause();});
  $('soundBtn').addEventListener('click',()=>{soundOn=!soundOn;$('soundBtn').textContent=soundOn?'♫':'♪̸';focusGame();});
  $('jumpBtn').addEventListener('pointerdown',e=>{e.preventDefault();jump();focusGame();});
  $('hookBtn').addEventListener('pointerdown',e=>{e.preventDefault();hook();focusGame();});
  canvas.addEventListener('pointerdown',e=>{
    focusGame();
    if(e.pointerType==='touch'){
      const t=performance.now();
      if(t-lastTap<340){hook();lastTap=0;}else{lastTap=t;}
    }
  });
  canvas.addEventListener('dblclick',e=>{e.preventDefault();
    const t=performance.now();if(t-lastDbl>250){hook();lastDbl=t;}
  });
  document.addEventListener('keydown',e=>{
    if(['Space','ArrowUp','KeyW','KeyE','KeyP','Escape'].includes(e.code))e.preventDefault();
    if(e.repeat)return;
    if(['Space','ArrowUp','KeyW'].includes(e.code))jump();
    if(e.code==='KeyE')hook();
    if(e.code==='KeyP'||e.code==='Escape')togglePause();
    if(e.code==='Enter'&&(mode==='menu'||mode==='dead'))start();
  },{passive:false});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&mode==='running')togglePause();});
  resetWorld();setOverlay('menu');requestAnimationFrame(loop);
  // Non-essential diagnostics for testing inside a browser, never sent to server.
  window.__bamtolDebug={start,jump,hook,update,get:()=>({mode,x:player.x,y:player.y,
    speed,score,fish,grounded:player.grounded,jumps:player.jumps,grappling:!!grapple,
    towers:world.towers.map(t=>({x:t.x,used:t.used})),elapsed})};
})();
</script>
</body>
</html>
"""

# st.iframe was introduced as the preferred HTML iframe host in recent Streamlit.
# Older Streamlit installations still work using the legacy component.
if hasattr(st, "iframe"):
    st.iframe(GAME_HTML, height=780)
else:
    import streamlit.components.v1 as components

    components.html(GAME_HTML, height=780, scrolling=False)

st.caption(
    "게임 영역을 한 번 클릭하면 키보드 조작이 활성화됩니다. "
    "모바일에서는 화면의 점프·갈고리 버튼을 사용하세요. "
    "최고 점수는 사용 중인 브라우저에 저장됩니다."
)
