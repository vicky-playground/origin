//load the home page 
function load() {
  // use ajax to get the data
  getData()
    .then(res => { 
      let nextPage = res[0];
      let data = res[1];
      display(nextPage, data);
    });
}

// get the attractions; return a array list of [nextPage, data]
async function getData(page=0, keyword) { 
  // if there is a keyword 
  if ( keyword != null && keyword != undefined && keyword != ""){
    const res = await fetch(`/api/attractions?page=${page}&keyword=${keyword}`)
    .then(response => response.json())
    .then(res => {
      let nextPage = res["nextPage"];
      let data = res["data"];
      console.log(nextPage, data)
      return [nextPage, data]; 
    })
    .catch(function(err) {
      console.log('Fetch problem: ' + err.message);
    });
    return res;  
  }
  // when there is no keyword
  else{ 
    console.log(`/api/attractions?page=${page}`) 
    const res = await fetch(`/api/attractions?page=${page}`)
    .then(response => response.json())
    .then(result => {
      console.log(result) 
      let nextPage = result["nextPage"];
      let data = result["data"]; 
      return [nextPage, data]; 
    })
    .catch(err => {
      console.log('Fetch problem: ' + err.message);
    }); 
    return res;  
  }
}

// display the content of attractions
function display(nextPage, data, keyword) {
  for (let i = 0; i < data.length; i++) {
    let img = data[i].images[0];
    let name = data[i].name;
    let mrt = data[i].mrt;
    let category = data[i].category;
    // Create boxes
    let site = document.createElement('div');
    site.className = 'site';
    let siteImg = document.createElement('img');
    siteImg.src = img;
    let siteName = document.createElement('div');
    siteName.id = 'name';
    siteName.innerHTML = name;
    let siteInfo = document.createElement('div');
    siteInfo.className = 'info';
    let siteMrt = document.createElement('div');
    siteMrt.id = 'mrt';
    siteMrt.innerHTML = mrt;
    let siteType = document.createElement('div');
    siteType.id = 'category';
    siteType.innerHTML = category;
    site.appendChild(siteImg);
    // add the name under the pic
    site.appendChild(siteName);
    // add the info under the name
    site.appendChild(siteInfo);
    siteInfo.appendChild(siteMrt);
    siteInfo.appendChild(siteType);
    document.getElementById('grid-container').appendChild(site);
  }
  // if there is next page
  if (nextPage){ 
    page = nextPage
    let paused = false;
    window.onscroll = function () {
      // when the user is at the bottom of the page
      if (((window.innerHeight + window.scrollY) >= document.body.offsetHeight) && !paused) {
        paused = true;
        getData(page, keyword)
          .then(res => { 
            let nextPage = res[0];
            let data = res[1];
            display(nextPage, data);
          });
      }
    }
  }
  // if there is no next page
  else {
    window.onscroll = () => false;
  }
}


// input keywords
function search() {
  let keyword = document.querySelector('input').value;
  if (keyword != '') {
    getData(0, keyword)
      .then(res => {
        let nextPage = res[0];
        let data = res[1];
        // if there is no such keyword
        if (!data){
          document.getElementById("grid-container").innerHTML="";
          document.getElementById("grid-container").innerHTML="查無資料";
        }
        // if there is the keyword
        else { 
          document.getElementById("grid-container").innerHTML="";
          display(nextPage, data, keyword);
        }
      })
      .catch(err => console.log('Error: ' + err))
  }
  else{
    load()
  }
}

