function add_to_database() {

    let nazwa = document.getElementById('add-nazwa').value;
    let numer_partii = document.getElementById('add-numer-partii').value;
    let cena = document.getElementById('add-cena').value;
    let opis = document.getElementById('add-opis').value;
    let liczba = document.getElementById('add-liczba').value;   
    let image = document.getElementById('add-image').value;
    let category = document.getElementById('add-category');
    let value_category = category.options[category.selectedIndex].value;

    if(user === 'AnonymousUser'){
        console.log('Not logged in')

    }else{
        console.log('Logged in')
        add_product_to_database(nazwa, numer_partii, cena, opis, liczba, image, value_category);
    }
}



function add_product_to_database(nazwa, numer_partii, cena, opis, liczba, image, category){
    console.log('User is logged in, process order...')

    let url = '/shop/add_product_to_database/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'nazwa': nazwa,
            'numer_partii': numer_partii,
            'cena': cena,
            'opis': opis,
            'liczba': liczba,
            'image': image,
            'kategoria': category
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