// SAVE: add a product in the user's favorites
var btnElts = document.getElementsByClassName('saveProduct');
var btnEltsCounter = btnElts.length;

const eltsSave = []

// iterate on each "save" button
for (let i = 0; i < btnEltsCounter; i++) {
  var btnEltI = document.getElementsByClassName('saveProduct')[i];
  eltsSave.push(btnEltI);

  // listen if a "save" button is clicked
  eltsSave[i].addEventListener("click", function (e) {
    e.preventDefault();
    // execute AJAX POST request
    $.ajax({
      type: 'POST',
      url: eltsSave[i].getAttribute('ajax-save-product-url'),
      data: {
        'product_id': eltsSave[i].getAttribute('property'),
        csrfmiddlewaretoken:$( 'input[name=csrfmiddlewaretoken]' ).val()
      },
      dataType: 'json',
      success: function (data) {
        // replace the "save" button by the "unsave" button
        var formId = document.getElementById(`${data.product_id}`);
        var blockCounter = formId.getElementsByClassName('d-block').length;
        for (let j = 0; j < blockCounter; j++) {
          var divElt = formId.getElementsByClassName('d-block')[j];
          divElt.setAttribute("class", "d-temp");
          // we can also use 'j' for "d-none" because there are as many "d-none" as "d-block"
          var divElt = formId.getElementsByClassName('d-none')[j];
          divElt.setAttribute("class", "d-block");
          // we can also use 'j' for "d-temp" due to previous action ("d-block > "d-temp")
          var divElt = formId.getElementsByClassName('d-temp')[j];
          divElt.setAttribute("class", "d-none");
        }
      }
    });
  });
}




// UNSAVE: remove a product from the user's favorites
var btnElts = document.getElementsByClassName('unsaveProduct');
var btnEltsCounter = btnElts.length;

const eltsUnsave = []

// iterate on each "save" button
for (let i = 0; i < btnEltsCounter; i++) {
  var btnEltI = document.getElementsByClassName('unsaveProduct')[i];
  eltsUnsave.push(btnEltI);

  // listen if a "save" button is clicked
  eltsUnsave[i].addEventListener("click", function (e) {
    e.preventDefault();
    // execute AJAX POST request
    $.ajax({
      type: 'POST',
      url: eltsUnsave[i].getAttribute('ajax-unsave-product-url'),
      data: {
        'product_id': eltsUnsave[i].getAttribute('property'),
        csrfmiddlewaretoken:$( 'input[name=csrfmiddlewaretoken]' ).val()
      },
      dataType: 'json',
      success: function (data) {
        // replace the "unsave" button by the "save" button
        var formId = document.getElementById(`${data.product_id}`);
        var blockCounter = formId.getElementsByClassName('d-block').length;
        for (let j = 0; j < blockCounter; j++) {
          var divElt = formId.getElementsByClassName('d-block')[j];
          divElt.setAttribute("class", "d-temp");
          // we can also use 'j' for "d-none" because there are as many "d-none" as "d-block"
          var divElt = formId.getElementsByClassName('d-none')[j];
          divElt.setAttribute("class", "d-block");
          // we can also use 'j' for "d-temp" due to previous action ("d-block > "d-temp")
          var divElt = formId.getElementsByClassName('d-temp')[j];
          divElt.setAttribute("class", "d-none");
        }
      }
    });
  });
}


// var save_form = $('#save');
// save_form.submit(function () {
//   $.ajax({
//     type: save_form.attr('method'),
//     url: save_form.attr('action'),
//     data: save_form.serialize(),
//     success: function (data) {
//       $("#SOME-DIV").html(data);
//     },
//     error: function(data) {
//       $("#MESSAGE-DIV").html("Something went wrong!");
//     }
//   });
//   return false;
// });