console.log("Running contentScript")

let price_el = document.querySelector("#vip-ad-price-container > span:nth-child(1)");
const price = price_el.innerHTML
price_el.innerHTML = "Berekenen...";


const auto = {}

//auto['kilometer_stand'] = parseInt(document.querySelector("#usps-block-container > div:nth-child(1) > div.usp-block-value").innerHTML.replace(/\D/g,''))
auto['upload_datum'] = document.querySelector("#displayed-since > span:nth-child(3)").innerHTML;
//auto['bouwjaar'] = document.querySelector("#usps-block-container > div:nth-child(2) > div.usp-block-value").innerHTML;
var divs = document.querySelectorAll('#car-attributes > div.car-feature-table.spec-table.spec-table_flex > .spec-table-item'), i;

divs.forEach(feature => {
    let key = feature.getElementsByClassName('key')[0].innerText;
  let value = feature.getElementsByClassName('value')[0].innerText;


  if (key.includes("Kenteken")) {
      auto['kenteken'] = value
  }
  if (key.includes("Brandstof")) {
      auto['is_benzine'] = value.includes('Benzine')
  }
  if (key.includes("Transmissie")) {
      auto['is_handgeschakeld'] = value.includes('Handmatig')
  }
  if (key.includes("Vermogen")) {
      auto['vermogen'] = parseInt(value)
  }
  if (key.includes('Kilometerstand')) {
      auto['kilometer_stand'] = parseInt(value.replace(/\D/g,''))
  }
  if (key.includes('Bouwjaar')) {
      auto['bouwjaar'] = parseInt(value.replace(/\D/g,''))
  }
})

fetch('http://127.0.0.1:8000/predict/', {
    method: 'post',
    body: JSON.stringify(auto)
}).then(response => {
    return response.json();
})
    .then(prediction_obj => {
        const prediction = prediction_obj.prediction
        console.log(prediction);

        let price_el = document.querySelector("#vip-ad-price-container > span:nth-child(1)");
        let prediction_el = price_el.cloneNode(true);

        prediction_el.innerHTML = '\u20AC ' + prediction + ',00'

        price_el.innerHTML = price
        prediction_el.innerHTML = " 🤖" + '👉 ' + prediction_el.innerHTML

        if (prediction > parseInt(price.replace(/\D/g,'')) / 100) {
            prediction_el.innerHTML = prediction_el.innerHTML + ' 🤑'
        } else {
            prediction_el.innerHTML = prediction_el.innerHTML + ' 😤'
        }

        document.querySelector("#vip-ad-price-container").appendChild(prediction_el)


    })