// set the variable to get the value of id when calling onload=load(id) in the beginning
let id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
let imgId = 0;
const bookingApi = '/api/booking' ;
let addr;
let site;
let date;
let price;
let time;

//load the page 
function load(id) {
  console.log(id)  // 1
    // use ajax call to get the data
    getData(id)
    .then(res => {
      display(res)
    });
}


// get the data of the attraction where id is assigned
async function getData(id) {
    console.log(id) // 1
    const res = await fetch(`/api/attraction/${id}`)
      .then(response => response.json())
      .then(res => {
        return res["data"]
      })
      .catch(err => console.log('Error: ' + err));
    return res;  
} 

// display the content of the attraction incl.:
// image, name, type +" at "+ place  
// desc. -> addr. -> transit
function display(res) {
  console.log(res)
  // res: {"data":OrderedDict(id = result["id"], name = result["stitle"], category = result["CAT2"], description = result["xbody"], address = result["address"], transport = result["info"], mrt = result["MRT"], latitude = result["latitude"], longitude = result["longitude"], images = result["file"])}
  let name = res["name"]
  let category = res["category"]
  let desc = res["description"]
  addr = res["address"]
  let transport = res["transport"]
  let mrt = res["mrt"]
  let img = res["images"]
  let index = 0
  
  //img
  let siteImg = document.createElement('img');
  siteImg.src = img[index];
  siteImg.id = 'img';
  document.getElementById('image').appendChild(siteImg);
  // name
  let siteName = document.createElement('div');
  siteName.id = 'name';
  document.getElementById('name').innerHTML = name;
  // type +" at "+ place  
  let siteInfo = document.createElement('div');
  siteInfo.id = 'info';
  document.getElementById('info').innerHTML = `${category} at ${mrt}`;
  // desc
  let siteDesc = document.createElement('div');
  siteDesc.id = 'desc';
  document.getElementById('desc').innerHTML = desc;
  // addr
  let siteAddr = document.createElement('div');
  siteAddr.id = 'address';
  document.getElementById('addr').innerHTML = addr;
  // transit
  let siteTransit = document.createElement('div');
  siteTransit.id = 'transport';
  document.getElementById('transport').innerHTML = transport;

  // render circles
  circle = document.querySelector('.circle')
  for (let i = 0; i < res["images"].length; i++) {
    let li = document.createElement('li');
		circle.appendChild(li) ;
  }
 
	// change circle color when changing pic
  let currentDot = document.querySelector(`.circle-sec li:nth-child(${imgId+1})`) 
  currentDot.classList.add('circle-black')
}

function addBlackDot() {
  // change circle color when changing pic
  let currentDot = document.querySelector(`.circle-sec li:nth-child(${imgId+1})`) 
  let blackDot = document.querySelector('.circle-black')
  blackDot = document.querySelector('.circle-black')
  blackDot.removeAttribute('class') 
  currentDot = document.querySelector(`.circle-sec li:nth-child(${imgId+1})`) 
  currentDot.classList.add('circle-black')
}

async function getImageList(id) {
  let data = await fetch(`/api/attraction/${id}`)
    .then(response => response.json())
    .then(result => {
      let images = result.data.images;
      return images
    })
    .catch(error => console.log('Error: ' + error))
  return data;
}

function NextImg() {
  getImageList(id).then(images => {
    let count = images.length;
    if (imgId < count - 1) {
      imgId += 1;
       // img
      document.querySelectorAll('#img').forEach(i => i.remove());
      let siteImg = document.createElement('img');
      siteImg.src = images[imgId];
      siteImg.id = 'img';
      document.getElementById('image').appendChild(siteImg);
      addBlackDot();
    } else {
      imgId = 0;
      // img
      document.querySelectorAll('#img').forEach(i => i.remove());
      let siteImg = document.createElement('img');
      siteImg.src = images[imgId];
      siteImg.id = 'img';
      document.getElementById('image').appendChild(siteImg);
      document.getElementById('current-dot').remove();
      addBlackDot();
    }
  })
}

function LastImg() {
  getImageList(id).then(images => {
    let count = images.length;
    if (imgId > 0) {
      imgId -= 1;
      document.querySelectorAll('#img').forEach(i => i.remove());
      let siteImg = document.createElement('img');
      siteImg.src = images[imgId];
      siteImg.id = 'img';
      document.getElementById('image').appendChild(siteImg);
      addBlackDot();
    } else {
      imgId = count - 1;
      document.querySelector('.image').style.backgroundImage = `url('${images[imgId]}')`;
      addBlackDot();
    }
  })
}




function displayAM() {
  pmMark.style.visibility = 'hidden';
  amMark.style.visibility = 'visible';
  document.querySelector('.price').innerHTML = ' 新台幣 2000 元';
}

function displayPM() {
  amMark.style.visibility = 'hidden';
  pmMark.style.visibility = 'visible';
  document.querySelector('.price').innerHTML = ' 新台幣 2500 元';
}

let rightArrow = document.getElementById('right-arrow');
rightArrow.addEventListener('click', NextImg);

let leftArrow = document.getElementById('left-arrow');
leftArrow.addEventListener('click', LastImg);

let am = document.getElementById('am');
let pm = document.getElementById('pm');
let amMark = document.getElementById('am-mark');
let pmMark = document.getElementById('pm-mark');
am.addEventListener('click', displayAM);
pm.addEventListener('click', displayPM);

function openForm() {
  document.getElementById("login").style.display = "block";
}

function closeForm() {
  document.getElementById("login").style.display = "none";
}

async function book(){
  if (document.getElementById('logout-btn').style.display == 'none'){
    await openLoginForm();
    return;
  }
  site = window.location.href.split("/")[4];
  date = document.getElementById("date").value;
  price = document.getElementById("price").innerHTML.match(/\d/g).join("");
  
  if (price == 2500){
    time = "afternoon"
  }
  else{
    time = "morning"
  }
  if(date == false){
    alert("請選擇日期");
    return;
  }
  // the order info
  else{ 
    console.log(site, date, time, price); 
    await fetch(bookingApi, {
        method: 'POST',
        body: JSON.stringify({ attractionId: site, date: date, time: time, price:price }),
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    })
    .then(result => result.json())
    .then(data => {
      if (data.ok) {
        window.location.href='/booking';
      }
      else{
        console.log(data.message);
      }
    })
  }
}