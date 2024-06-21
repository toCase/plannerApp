const btn_pls = document.querySelector('.columnA .btn-pls');
const btn_upd = document.querySelector('.columnA .btn-upd');
const btn_gen = document.querySelector('.columnA .btn-gen');
const btn_ok = document.querySelector('.columnA .btn-ok');
const el_template = document.getElementById('st-control');
const el_temp_form = document.getElementById('st_template');

var el_start = document.getElementById('start');
var el_fin = document.getElementById('fin');
var el_dur = document.getElementById('dur');

el_start.addEventListener('input', changeStart);
el_fin.addEventListener('input', changeFin);
el_dur.addEventListener('input', changeDur);

btn_pls.addEventListener('click', addSection);
btn_upd.addEventListener('click', clearTemplate);
btn_ok.addEventListener('click', templateOk);

var session = "";

function changeStart(el){ 
    console.log("session");

    var s = Number(el.target.value);
    if (s > 23){
        el_start.value = 23;
        s = 23;
    }
    if (s < 0){
        el_start.value = 0;
        s = 0;
    }       
    el_fin.min = s + 1;
    if (el_fin.value <= s){
        el_fin.value = s + 1;
    }
    makeTempalate();
}

function changeFin(el){   
    var s = Number(el_start.value);
    var f = Number(el.target.value);
    if (f > 24){
        el_fin.value = 24;
        f = 24;
    } 
    if (f < s){
        el_fin.value = s + 1;
        f = s + 1;
    }
    makeTempalate();
}

function changeDur(el){
    makeTempalate();
}

function addSection(){
    session = el_template.value;
}

function makeTempalate(){
    el_template.value = session + el_start.value + ":" +el_fin.value + ":" + el_dur.value + "|";
}

function clearTemplate(){
    session = "";
    el_template.value = "";
}

function templateOk(){
    el_temp_form.value = el_template.value;
}