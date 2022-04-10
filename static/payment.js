// Use TPDirect.setupSDK set up your enviroment.
TPDirect.setupSDK(
    124019, 
    "app_d2djo3V2HuMAyHdJnash82BhJww374EO3XOfw20H122xWGkZyB8AxBgUk8xq", 
    "sandbox"
)
// Display ccv field
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
};

// TPDirect.card.setup
TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
        //     'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            // 'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            // 'font-size': '16px'
        },
        // style focus state
        ':focus': {
             'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    }
});


function onSubmit(event) {
    event.preventDefault()
    if (document.getElementById('contact-name').value == "" || document.getElementById('contact-email').value== "" || document.getElementById('contact-phone').value == ""){
        alert("Please fill in all the contact info")
        return;
    }

    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    console.log(tappayStatus)

    // Check TPDirect.card.getTappayFieldsStatus().canGetPrime before TPDirect.card.getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('The info of credit card is incorrect')
        return;
    }
    
    // Get prime
    TPDirect.card.getPrime(function (result) {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return;
        }
        alert('get prime successful! Prime: ' + result.card.prime)
           // send prime to the server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api

        let data = {
            "prime": result.card.prime,
            "order": {
              "price": document.getElementById('total').innerHTML,
              "trip": {
                "attraction": {
                  "id": siteId,
                  "name": siteName,
                  "address": addr,
                  "image": img
                },
                "date": date,
                "time": time
              },
              "contact": {
                "name": document.getElementById('contact-name').value,
                "email": document.getElementById('contact-email').value,
                "phone": document.getElementById('contact-phone').value
              }
            }
          }
        const ordersApi = '/api/orders'
        fetch(ordersApi, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })
        .then(result => result.json())
        .then(order => {
            console.log(order.number)
            window.location='http://127.0.0.1:3000/thankyou?number='+order.number
        })
        
        
 
    })
}

document.getElementById('onSubmit').addEventListener('click', onSubmit)
