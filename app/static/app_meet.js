// составление списка услуг и подсчет стоимости
services = document.getElementById('service-select');

// lineServices = document.getElementById('m-service')

services.addEventListener('change', makeValue);

function makeValue(){
    // lineServices.value = lineServices.value + " " + services.options[services.selectedIndex].text;
    console.log("change");
    // let _sum = parseFloat(lineValue.value);
    // let _val = parseFloat(services.value);
    // let _s = _sum + _val;
    // lineValue.value = _s.toFixed(2);
}
//---------------------------------------------

// очитска строки списка услуг 
// btn_clear = document.getElementById('clear_service');
// btn_clear.addEventListener('click', clearService);
// function clearService(){
//     lineServices.value = "";
//     lineValue.value = 0;
// }
//---------------------------------------------