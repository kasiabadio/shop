//let updateBtns = document.getElementsByClassName('update-cart')
let order_option = document.getElementById('order-selection-cart')

// dropdown menu in main.html
document.addEventListener("DOMContentLoaded", function(){

    document.querySelectorAll('.dropdown-menu').forEach(function(element){
        element.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    })

}); 



// ordernumber update in cart.html
function order_cart() {
    let user = '{{request.user}}'

    let select = document.getElementById('order-selection-cart');
    //let select1 = document.getElementById('order-details');

    let value = select.options[select.selectedIndex].value;
    //select1.innerHTML = value;

    
    if(user === 'AnonymousUser'){
        console.log('Not logged in')

        // TODO: delete it once login is done 
        update_order_number(value);
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


// TODO: checking all buttons which have class name update-cart
// for(let i = 0; i < updateBtns.length; i++){

//     updateBtns[i].addEventListener('click', function(){

//         let product_id = this.dataset.product
//         let action = this.dataset.action
//         console.log('product_id:', product_id, 'action:', action)

//         console.log('USER:', user)
//         if(user === 'AnonymousUser'){
//             console.log('Not logged in')
//         }else{
//             update_user_order(product_id, action)
//         }

//     })
// }


// function update_user_order(product_id, action){
//     console.log('User is logged in, sending data...')

//     let url = '/update_item/'

//     // whenever we are sending POST data to the backend in Django, is we need to send CSRF token
//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             'product_id': product_id, 'action': action
//         })
//     })


//     .then((response) => {
//                 return response.json()
//             })

//             .then((data) => {
//                 console.log('data: ', data)
//             })
// } 