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
        console.log('product_id:', product_id)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){

            // TODO: delete it once login is done 
            update_user_order(product_id)
            console.log('Not logged in')
        }else{
            update_user_order(product_id)
        }

    })
}


function update_user_order(product_id){
    console.log('User is logged in, sending data...')

    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': product_id, 
        })
    })


    .then((response) => {
                return response.json()
            })
            .then((data) => {
                console.log('data: ', data)
            })
            .catch(error =>{
                console.error(error);
            })
} 