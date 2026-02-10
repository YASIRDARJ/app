let stop=false, queue=[], running=0;
let stats={checked:0,live:0,approved:0,declined:0};

function toast(msg){
  toastEl.innerText=msg;
  toastEl.style.display="block";
  setTimeout(()=>toastEl.style.display="none",2000);
}

fileInput.onchange=()=>{
  const f=fileInput.files[0];
  if(!f)return;
  f.text().then(t=>{
    cardsInput.value+= "\n"+t.trim();
    toast(`Added ${t.trim().split("\n").length} cards`);
  });
};

start.onclick=()=>{
  stop=false;
  start.style.display="none";
  stopBtn.style.display="block";

  Object.keys(stats).forEach(k=>stats[k]=0);
  updateStats();

  liveBox.innerHTML=deadBox.innerHTML="";
  queue=cardsInput.value.split("\n").filter(x=>x.trim());
  run();
};

stopBtn.onclick=()=>stop=true;

function run(){
  while(running < threads.value && queue.length){
    check(queue.shift());
  }
}

async function check(card){
  running++;
  const t0=performance.now();
  try{
    const r=await fetch("/check",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({cards:[card]})
    });
    const d=await r.json();
    const x=d.results[0];
    const ms=Math.round(performance.now()-t0);

    stats.checked++;
    if(x.success){
      stats.live++;stats.approved++;
      liveBox.innerHTML+=`<div>${card}<br><small>${x.response} • ${ms}ms</small></div>`;
    }else{
      stats.declined++;
      deadBox.innerHTML+=`<div>${card}<br><small>${x.response} • ${ms}ms</small></div>`;
    }
    updateStats();
  }catch{}
  running--;
  if(!stop)run();
}

function updateStats(){
  checked.innerText=stats.checked;
  live.innerText=stats.live;
  approved.innerText=stats.approved;
  declined.innerText=stats.declined;

  p_checked.innerText=stats.checked;
  p_live.innerText=stats.live;
  p_approved.innerText=stats.approved;
  p_declined.innerText=stats.declined;
}

function openTab(t){
  checkerTab.classList.add("hidden");
  profileTab.classList.add("hidden");
  leaderTab.classList.add("hidden");
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));

  if(t=="checker") checkerTab.classList.remove("hidden");
  if(t=="profile") profileTab.classList.remove("hidden");
  if(t=="leader"){
    leaderTab.classList.remove("hidden");
    leaderList.innerHTML=`<div>🔥 You – ${stats.approved} Approved</div>`;
  }
  event.target.classList.add("active");
}

const toastEl=document.getElementById("toast");
