//Display product depending filter
$(".filtres").on('click', function (event){
  var elt = $(event.target).html()
  var product = $(".product")
  for (var i = 0; i < product.length; i++) {
    categ = $(product[i]).data('category')
    if (categ == elt) {
      $(product[i]).show()
    }
    else {
      $(product[i]).hide()
    }
  }
})


// MODAL
$('#detailProduct').on('show.bs.modal', function (event) {
  var product = $(event.relatedTarget)
  var modal = $(this)

  modal.find('.modal-title').text(
    product.data('product') + " - " + product.data('variety')
  )
  modal.find('.price').text(
    product.data('price') + "€ / " + product.data('unity')
  )
  modal.find('#quantity').attr("data-id", product.data('id'))
  modal.find('#quantity').attr("max", product.data('stock'))

  if (product.data('cart')) {
    modal.find('#quantity').val(product.data('cart'))
  }
  else{
    modal.find('#quantity').val(1)
  }

  //var vids = $(".videorecette");
  //for (var i = 0; i < vids.length; i++) {
//    vids[i].load()
  //}

//  var active = $(this).find(".active video");
//  active[0].play()
});

$("#carouselExampleCaptions").on('slid.bs.carousel', function () {
   var vids = $(this).find(".active video");
   vids[0].currentTime = 0;
   vids[0].play()
})

$('#cartform').submit(function(event){
  event.preventDefault();
  $.ajax({
    type:"POST",
    headers:{'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    url:$("#cartform").attr('action'),
    data :
    {
      "quantity" : $('#quantity').val(),
      "product" : $('#quantity').attr('data-id'),
    },
    dataType : "json"
  });

});


//LOGIN FORM

// events for adaptative and dynamic login form in modal
$('#ModalLogin').on('show.bs.modal', function (event) {
  $('#have_account').prop('checked', true);
  $("#create_account").hide();
  $(":input.req").prop('required',false);
  $("#confirmpass").hide();
})

// adaptative form if connect or create account
$("input[name='formchoice']").click(function(){
  if ($('#have_account').is(':checked')) {
    $("#create_account").hide();
    $(":input.req").prop('required',false);
    $("#confirmpass").hide();
  } else if ($('#no_account').is(':checked')) {
    $("#create_account").show();
    $(":input.req").prop('required',true);
    $('#partic').prop('checked', true);
    $("#type_account label[for='name']").html("Nom *");
    $("#type_account input[name='phone']").prop('required',false);
    $("#type_account label[for='phone']").html("Téléphone");
    $("#confirmpass").show();
  }
})

// adaptative create form depending client type
$("input[name='clienttype']").click(function(){
  if ($('#partic').is(':checked')) {
    $("#type_account label[for='name']").html("Nom *");
    $("#type_account input[name='phone']").prop('required',false);
    $("#type_account label[for='phone']").html("Téléphone");
  } else if ($('#rest').is(':checked')) {
    $("#restaurantname").show();
    $("#type_account input[name='phone']").prop('required',true);
    $("#type_account label[for='phone']").html("Téléphone *");
    $("#type_account label[for='name']").html("Restaurant *");
  }
})


const login = () => {
  $.ajax({
    type:"POST",
    headers:{'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    url:$("#loginform").attr('action'),
    data : data,
    success: $("#ModalLogin").modal('hide'),
    dataType : "json"
  });
};


$("#loginform").submit(function(event){
  event.preventDefault();
  if (($('#have_account').is(':checked'))) {
    data = {
      "choice" : $('input[name="formchoice"]:checked').val(),
      "email" : $("input[name='mail']").val(),
      "password" : $("input[name='password']").val()
    }
    login()
  }
  else if (($('#no_account').is(':checked'))) {
    if ($("input[name='password']").val() == $("input[name='confirmpassword']").val()) {
      data = {
        "choice" : $('input[name="formchoice"]:checked').val(),
        "type" : $('input[name="clienttype"]:checked').val(),
        "email" : $("input[name='mail']").val(),
        "name" : $("input[name='name']").val(),
        "phone": $("input[name='phone']").val(),
        "number": $("input[name='number']").val(),
        "street" : $("input[name='rue']").val(),
        "cplt" : $("input[name='cplt']").val(),
        "cp" : $("input[name='code_postal']").val(),
        "city" : $("input[name='ville']").val(),
        "password" : $("input[name='password']").val()
      }
      login()
    } else {
      $('#alertmdp').html('Veuillez saisir un même mot de passe')
    }
  }

});


function update_total_cart() {
  var total_result=0;
  var subtotal = $(".subtotal");
  for (var i = 0; i < subtotal.length; i++) {
    value = parseFloat($(subtotal[i]).text())
    total_result+=value
  };
  $("#total_cart").text(total_result.toFixed(2))
};

//remove from Cart
$('.remove').on('click', function(event) {
  event.preventDefault()
  var button = $(event.target);

  $.ajax({
    type:"POST",
    headers:{'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    url:$(button).parents("table").attr('data-remove'),
    data : {"cart_object" : button.parents("tr").attr('data-product')},
    success : function() {
      $(button).parents("tr").remove();
      update_total_cart()
    },

    dataType : "json"
  });

  return false;
})
