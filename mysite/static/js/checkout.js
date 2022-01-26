
// ordernumber is sent to checkout.html
function order_checkout() {

    let select = document.getElementById('order-checkout').innerHTML;
    if(user === 'AnonymousUser'){
        console.log('Not logged in')

    }else{
        console.log('Logged in')
        process_order(select);
    }
}


function process_order(order_number){
    console.log('User is logged in, process order...')

    let url = '/shop/process_order/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'order_number': order_number, 
        })
    })


    .then((response) => {
                return response.json()
            })
            .then((data) => {
                location.href = "/shop/";
            })
            .catch(error => {
                console.error(error);
            })
} 