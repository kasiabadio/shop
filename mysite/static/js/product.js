function edit_product(){
    let opis = document.getElementById('add-opis').value;

    let el = document.querySelector('#product-update');
    let product_id = el.dataset.product;
    

    if(user !== 'AnonymousUser'){
        console.log('User is logged in, edit product...')
        let url = '/shop/edit_product/'

        fetch(url, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'opis': opis,
                'product_id': product_id,
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