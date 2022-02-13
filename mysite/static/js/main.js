let update_cart_buttons = document.getElementsByClassName('update-cart')


// dropdown menu 
document.addEventListener("DOMContentLoaded", function(){

    document.querySelectorAll('.dropdown-menu').forEach(function(element){
        element.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    })
}); 


for(let i = 0; i < update_cart_buttons.length; i++){

    update_cart_buttons[i].addEventListener('click', function(){

        let product_id = this.dataset.product // product.id_produktu
        let producent_id = this.dataset.producent
        console.log('product_id:', product_id)
        console.log('producent_id:', producent_id)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){

            // TODO: delete it once login is done 
            update_user_order(product_id, producent_id)
            console.log('Not logged in')
        }else{
            update_user_order(product_id, producent_id)
        }

    })
}


function update_user_order(product_id, producent_id){
    console.log('User is logged in, sending data...')

    let url = '/shop/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': product_id, 
            'producent_id': producent_id,
        })
    })


    .then((response) => {
                return response.json()
            })
            .then((data) => {
                //console.log('data: ', data);
                location.reload;
            })
            .catch(error =>{
                console.error(error);
            })
} 


function find_product(){
    let product_pattern = document.getElementById('find-product').value;
    
    if(user !== 'AnonymousUser'){
        console.log('User is logged in, find product...')
        let url = '/shop/find_product/'

        fetch(url, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product_pattern': product_pattern,
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