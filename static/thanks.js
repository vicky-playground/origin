//fetch GET 訂單資訊
async function thanks(){
  let url=window.location.href
  url=url.split('=')
  const orderApi = '/api/order/'+url[1] // get the order number
  //console.log("number: ", orderApi) ///api/order/202204101754187202
  await fetch(orderApi)
      .then(res => res.json())
      .then(res => { 
        let contact = res.data.contact;
        let price = res.data.price;
        let name = res.data.trip.attraction.name;
        let address = res.data.trip.attraction.address;
        let date = res.data.trip.date;
        let time = res.data.trip.time;    
        
        const content = document.getElementById('order-content')
        content.innerHTML =`
        <h2>本次預定行程如下：</h2>
        <h3>訂單編號：${url[1]}</h3>
        <h3>聯絡人：${contact.name}</h3>
        <h3>金額：${price}</h3>
        <h3>地址：${address}</h3>
        <h3>日期時間：${date, time}</h3>
        `
    })
}