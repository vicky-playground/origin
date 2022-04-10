//fetch GET 訂單資訊
async function thanks(){
  let url=window.location.href
  url=url.split('=')
  const orderApi = '/api/order/'+url[1] // get the order number
  //console.log("number: ", orderApi) ///api/order/202204101754187202
  await fetch(orderApi)
      .then(res => res.json())
      .then(res => { 
        let data = res.data;
        console.log(data)
        const content = document.getElementById('order-content')
        content.innerHTML =`
        <h2>本次預定行程如下：</h2>
        <h3>訂單編號：${url[1]}</h3>
        <h3>明細（請查閱console）：${data}</h3>
        `
    })
}
