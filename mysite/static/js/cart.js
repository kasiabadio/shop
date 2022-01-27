
// ordernumber is sent to checkout.html
function order_cart() {

    let select = document.getElementById('order-selection-cart');
    let value = select.options[select.selectedIndex].value;
    
    if(user === 'AnonymousUser'){
        console.log('Not logged in')

    }else{
        console.log('Logged in')
        update_order_number(value);
    }

}


function update_order_number(order_number){
    console.log('User is logged in, update order number...')

    let url = '/shop/curr_order_number/'

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
                location.href = "/shop/checkout/";
            })
            .catch(error => {
                console.error(error);
            })
} 