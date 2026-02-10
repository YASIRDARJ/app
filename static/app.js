let stop = false;
let liveCards = [];

start.onclick = async ()=>{
  stop=false;
  start.style.display="none";
  stopBtn.style.display="block";

  results.innerHTML="";
  live.innerText=approved.innerText=declined.innerText=0;
  liveCards=[];

  const cards = cardsInput.value.split("\n");

  const r = await fetch("/check",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({cards})
  });

  const d = await r.json();

  d.results.forEach(x=>{
    if(stop) return;

    const div=document.createElement("div");
    div.className="result "+(x.success?"approved":"declined");
    div.innerHTML=`
      <b>${x.card}</b><br>
      ${x.response}<br>
      <small>${x.time} ms</small>
    `;
    results.prepend(div);

    if(x.success){
      live.innerText++;
      approved.innerText++;
      liveCards.push(x.card);
    }else{
      declined.innerText++;
    }
  });

  start.style.display="block";
  stopBtn.style.display="none";

  popText.innerText="Live: "+live.innerText;
  popup.style.display="flex";
};

stopBtn.onclick=()=>stop=true;

function copyLive(){
  navigator.clipboard.writeText(liveCards.join("\n"));
  }
