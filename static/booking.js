const bookingApi = '/api/booking' ;

async function signinCheck() {
  const UserApi = '/api/user'
  await fetch(UserApi)
      .then(res => res.json())
      .then(result => {
          console.log("result: ", result.data, result.data == null)
          if (result.data != null) { 
            document.getElementById('login-btn').style.display = 'none';
            document.getElementById('logout-btn').style.display = 'block';
            console.log('user has already logged in')
          } else {
            document.getElementById('login-btn').style.display = 'block';
            document.getElementById('logout-btn').style.display = 'none';
            console.log('user has not logged in yet.')
            window.location='http://127.0.0.1:3000/';
          }
      })
}
signinCheck()

//render the view of the trip
async function renderTrip(){
  let noOrder = document.getElementById("no-order");

  await fetch(bookingApi)      
  .then(res => res.json())
  .then(result => {
  // when there is no order yet
  if(result.data == null){
    noOrder.style.display= 'flex';
    let footer = document.getElementById('footer');
    footer.style.paddingBottom = "1000px";
    return false;
  }else{
    noOrder.style.display = 'none';
  }
  
  // show the area of order info
  document.getElementById('order-sec').style.display = 'block'
  // build the parent of the trip contents (img, text..)
  tripInfo = document.getElementById("trip-info");
  // child 
  let siteId = result.data['id'];
  let img = result.data['image']; 
  let name = result.data['name'];
  let date = result['date'];
  let time = result['time'];
  // revise the info of time
  if (time == 'morning'){
    time = "早上九點到下午四點"
  }
  else{
    time = '下午兩點到晚上九點'
  }
  let price = result['price'];
  let addr = result.data['address'];
  // img
  let tripImg = document.createElement("img");
  tripImg.setAttribute('class', 'trip-img');
  tripImg.setAttribute("src", img);
  let picture = document.createElement('picture');
  picture.setAttribute("class", 'trip-img-sec');
  picture.appendChild(tripImg);
  let tripImgC = document.createElement("div");
  tripImgC.setAttribute("class", "trip-img-container");
  tripImgC.appendChild(picture);
  // title
  let orderName=document.createElement("div")
  orderName.setAttribute("class","order-name")
  webName=document.createTextNode("台北一日遊 :")
  orderName.appendChild(webName)
  // date
  let tripDate = document.createElement("div");
  tripDate.setAttribute("class", 'order-trip');
  trip_d = document.createTextNode("日期 :");
  tripDate.appendChild(trip_d);
  // am/pm
  let tripTime = document.createElement("div");
  tripTime.setAttribute("class", 'order-trip');
  webName=document.createTextNode("時間 :")
  tripTime.appendChild(webName)
  // price
  let tripPrice = document.createElement("div");
  tripPrice.setAttribute("class", 'order-trip');
  trip_f = document.createTextNode("費用 :");
  tripPrice.appendChild(trip_f);
  // address
  let tripAddr = document.createElement("div");
  tripAddr.setAttribute("class", 'order-trip');
  trip_a = document.createTextNode("地址 :");
  tripAddr.appendChild(trip_a);
  // site name
  let nameSec=document.createElement("div");
  nameSec.setAttribute("class",'order-name-sec')
  nameSec.setAttribute("id","trip_name="+siteId);
  name=document.createTextNode(name)
  nameSec.appendChild(orderName)
  nameSec.appendChild(name)
  // date
  let dateSec=document.createElement("div")
  dateSec.setAttribute("class",'order-trip-sec')
  dateSec.setAttribute("id","trip_date="+siteId)
  date=document.createTextNode(date)
  dateSec.appendChild(tripDate)
  dateSec.appendChild(date);
  // time
  let timeSec=document.createElement("div");
  timeSec.setAttribute("class",'order-trip-sec')
  timeSec.setAttribute("id","trip_time="+siteId)
  time=document.createTextNode(time)
  timeSec.appendChild(tripTime);
  timeSec.appendChild(time)
  // price
  let priceSec = document.createElement("div");
  priceSec.setAttribute("class", 'trip-price');
  priceSec.setAttribute("id", "trip_cost="+siteId);
  price=document.createTextNode(price)
  priceSec.appendChild(tripPrice);
  priceSec.appendChild(price);
  // address
  let addrSec = document.createElement("div");
  addrSec.setAttribute("class", 'order-trip-sec');
  addrSec.setAttribute("id", "trip_add="+siteId);
  addr=document.createTextNode(addr)
  addrSec.appendChild(tripAddr)
  addrSec.appendChild(addr);
  // put the above info into the 'book-info'
  let bookInfo=document.createElement("div")
  bookInfo.setAttribute('class','book-info')
  bookInfo.appendChild(nameSec)
  bookInfo.appendChild(dateSec)
  bookInfo.appendChild(timeSec);
  bookInfo.appendChild(priceSec);
  bookInfo.appendChild(addrSec);
  // put info and image into renderTrip div
  let view=document.createElement("div")
  view.setAttribute("class","renderTrip")
  view.appendChild(bookInfo)
  view.appendChild(tripImgC)
  // deletion button 
  deleteBtn=document.createElement("div")
  deleteBtn.setAttribute("class",'book-delete')
  deleteBtn.setAttribute("id",'delete-id='+siteId)
  deleteBtn.setAttribute("onclick","deleteTrip(this.id)") // this.id = siteId
  deleteBtnImg=document.createElement("img")
  deleteBtnImg.setAttribute("src",'../static/IMG/trash.png')
  deleteBtn.appendChild(deleteBtnImg)
  // build the parent of the upper part in the page
  upper=document.createElement("div")
  upper.setAttribute("class",'upper')
  upper.setAttribute("id",'upper='+siteId)
  upper.appendChild(tripImgC)
  upper.appendChild(bookInfo)
  upper.appendChild(deleteBtn)
  // put into the first parent
  tripInfo.appendChild(upper);
})
  renderPrice();
}

// render the price of the trip
renderPrice=()=>{
  let tripPrice = document.getElementsByClassName('trip-price');
  let total = document.getElementById('total');
  let subtotal = 0;
  let noOrder = document.getElementById('no-order');
  for(i of tripPrice){
    subtotal += Number(i.innerHTML.split("</div>")[1]);
  }
  console.log(subtotal)
  total.innerHTML = subtotal;// change $0 to subtotal
  if(subtotal == 0){
    noOrder.style.display = 'flex'
    document.getElementById('order-sec').innerHTML = null;
    document.getElementById('border').style.display = "none";
    document.getElementById('footer').style.paddingBottom = "1000px";
  }
}

//delete
async function deleteTrip(siteId){
  let id = siteId.split("=")[1]
  //console.log(id);
  await fetch(bookingApi,{
    method: 'DELETE',
    headers: new Headers({
        'Content-Type': 'application/json'
    })
  })      
  .then(result => result.json())
  .then(data => {
    if (data.ok){
      let upper = document.getElementById('upper='+id)
      upper.remove();
      let noOrder = document.getElementById('no-order')
      noOrder.style.display = 'block'
      noOrder.style.textAlign = 'left'
      let orderData = document.getElementById("order-sec")
      orderData.style.display = 'none'
      let footer = document.getElementById("footer")
      footer.style.paddingBottom = "1000px";
    }else{
      console.log('API error')
    }
  })
}