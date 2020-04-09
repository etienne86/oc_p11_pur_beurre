// Code from jQuery UI Autocomplete
// The purpose is helping the user to find a product in the database

$( function() {
  var allProducts = JSON.parse(
    document.getElementById('pythonProducts').textContent
  );
  // autocomplete search field in navbar
  $( "#autocompletion-0" ).autocomplete({
    source: allProducts
  });
  // autocomplete search field in home page (masthead section)
  $( "#autocompletion-1" ).autocomplete({
    source: allProducts
  });
} );

// adjust size of menu
jQuery.ui.autocomplete.prototype._resizeMenu = function () {
  var ul = this.menu.element;
  ul.outerWidth(this.element.outerWidth());
}


// Block with AJAX POST:
// - to send the product selected by the user to the Python view
// - to deal with the feedback from Python

var formElts = document.getElementsByClassName('productSubmitForm');
var formEltsCounter = formElts.length; // expect 2 (home page) or 1

const elts = []

// iterate on each search form
for (let i = 0; i < formEltsCounter; i++) {
  var formEltI = document.getElementsByClassName('productSubmitForm')[i];
  elts.push(formEltI);
  
  // listen if a search form is submitted
  elts[i].addEventListener("submit", function (e) {
    e.preventDefault();
    // get the input text
    var productString = document.getElementById(`autocompletion-${i}`).value;
    // if there is an input
    if (productString != "") {
      // execute AJAX POST request
      $.ajax({
        type: 'POST',
        url: elts[i].getAttribute('ajax-find-product-url'),
        data: {
          'product_string': productString,
          csrfmiddlewaretoken:$( 'input[name=csrfmiddlewaretoken]' ).val()
        },
        dataType: 'json',
        success: function (data) {
          // redirect to the product page
          var action = elts[i].getAttribute("action");
          var newAction = action.replace("0", `${data.product_id}`);
          elts[i].setAttribute("action", newAction);
          elts[i].submit();
        }
      });
    };
  });
}