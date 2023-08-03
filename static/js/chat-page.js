let dataToSend = {
  counter: '0'
}
let fetchurl = setFetchUrl();

function setFetchUrl(){
  let queryParams = new URLSearchParams(dataToSend).toString();
  let fetchurl = '/messages?' + queryParams;
  return fetchurl
}

function runWithInterval() {
  fetchurl = setFetchUrl();
  fetchDataFromDatabase(fetchurl);
}



function setup(){


    document.getElementById("chatForm").addEventListener("submit", function (event) {
        event.preventDefault(); 

        const author = document.getElementById("author").value;
        const message = document.getElementById("message").value;

        fetch("/new_message/", {
        method: "post",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `username=${encodeURIComponent(author)}&message=${encodeURIComponent(message)}`
        })
        .then(response => response.json())
        .then(data => {
            let j = data.Key1;
            let k = data.Key2;
            console.log(j);
            console.log(k);
            document.getElementById("chat-history").innerHTML += `${j}: ${k} <br> <br>`;
            let q = document.getElementById("message");
            q.value = "";
            dataToSend.counter = (parseInt(dataToSend.counter) + 1).toString();
        })
        .catch(error => {
            console.error("Error:", error);
        });

    });

    fetchDataFromDatabase(fetchurl);

    setInterval(runWithInterval, 15000);
  } 



function fetchDataFromDatabase(fetchurl) {

    console.log("Fetching data from the database...");
    console.log(dataToSend)
    let ch = document.getElementById("chat-history")

    fetch(fetchurl)
      .then(response => response.json())
      .then(data => {
        console.log("Fetched data:", data);
        for (const obj of data) {
            for (const key in obj) {
                console.log(`Key: ${key}, Value: ${obj[key]}`);
                ch.innerHTML+=`${key}: ${obj[key]} <br> <br>`;
                dataToSend.counter = (parseInt(dataToSend.counter) + 1).toString();
            }
          }
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }
/*
  function get_new_messages() {

    console.log("Fetching data from the database...");
  
    fetch("/get_new_messages/")
      .then(response => response.json())
      .then(data => {
        console.log("Fetched data:", data);
        let ch = document.getElementById("chat-history")
        for (const obj of data) {
            for (const key in obj) {
                console.log(`Key: ${key}, Value: ${obj[key]}`);
                ch.innerHTML+=`${key}:${obj[key]}`
                ch.innerHTML+='<br> <br>'
            }
          }
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }
  */

window.addEventListener('load', setup);