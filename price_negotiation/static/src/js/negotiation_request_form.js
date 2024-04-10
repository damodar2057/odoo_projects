//const call_price_negotiation_form = (product_name, product_price, min_quantity, product_id) => {
//    fetch(`/price/negotiation`, {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json'
//        },
//        body: JSON.stringify({
//            'product_name': product_name,
//            'product_price': product_price,
//            'min_quantity': min_quantity,
//            'product_id': product_id
//        })
//    })
//    .then(function (response) {
//        if (response.ok) {
//                window.location.href = '/price/negotiation'; // Redirect to the price/negotiation page
//// Assuming HTML response
//        } else {
//            throw new Error('Network response was not ok.');
//        }
//    })
//    .then(function (data) {
//        // Process the retrieved data
//        // Populate the edit form fields or perform other actions with the data
//    })
//    .catch(function (error) {
//        console.error('There was a problem with the fetch operation:', error);
//        // Handle errors or exceptions here
//    });
//}

const redirect_to_shop = () =>{
  window.location.href = '/shop'
}
