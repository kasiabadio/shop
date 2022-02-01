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


function remove_order_from_cart(){

    if(user !== 'AnonymousUser'){
        console.log('User is logged in, remove order from cart...')

        let el = document.querySelector('#order-removal-cart');
        let order_id = el.dataset.orderid;
        let url = '/shop/remove_order/'

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'order_id': order_id,
            })
        })


        .then((response) => {
                    return response.json()
                })
                .then((response) => {
                    console.log(response)
                })
                .catch(error => {
                    console.error(error);
                })
    }
}


function remove_product_from_order(){

    if(user !== 'AnonymousUser'){

        console.log('User is logged in, remove product from order...')

        let el = document.querySelector('#product-removal-cart');
        let product_id = el.dataset.idproduktu;
        let order_id = el.dataset.orderid;
        let url = '/shop/remove_product/'
    
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product_id': product_id,
                'order_id': order_id,
            })
        
        })
    
    
        .then((response) => {
                    return response.json()
                })
                .then((data) => {
                    location.reload; 
                })
                .catch(error => {
                    console.error(error);
                })

    }
}