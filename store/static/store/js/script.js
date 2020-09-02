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
});


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
  input = modal.find('input')
  input.parents(':eq(1)').attr("data-id", product.data('id'))
  input.attr("max", product.data('stock'))

  if (product.attr('data-cart')) {
    input.attr("value",product.attr('data-cart'))
    input.val(product.attr('data-cart'))
    input.parent("div").css("display","block")
    modal.find('.add').css("display","none")
    minus = modal.find(".minus")
    plus = modal.find(".plus")
    update_button(input.attr("value"), input.attr("max"), minus, plus)
  }
  else{
    input.attr("value",1)
    input.val(1)
    input.parent("div").css("display","none")
    modal.find('.add').css("display","block")
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



// ****** CART INTERFACE ******
function update_total_cart() {
  var total_result=0;
  var subtotal = $(".subtotal");
  for (var i = 0; i < subtotal.length; i++) {
    value = parseFloat($(subtotal[i]).text())
    total_result+=value
  };
  $("#total_cart").text(total_result.toFixed(2))
};

function update_cart(origin, value){
  subtotal = origin.parents("tr").find(".subtotal");
  price = origin.parents("tr").attr("data-price");
  result = price * value;
  subtotal.text(result.toFixed(2));
  update_total_cart()
};

function update_button(value, max, minus, plus){
  if (value == 1)
  {
    minus.text("del")
    minus.addClass("del")
  }
  else
  {
    minus.text("-")
    minus.removeClass("del")
  }

  if (value == max)
  {
    plus.text("max")
    plus.prop("disabled", true)
  }
  else
  {
    plus.text("+")
    plus.prop("disabled", false)
  }
};

function ajax_update(input, id_product, value, action){
  $.ajax({
    type:"POST",
    headers:{'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    url:input.parent("div").attr('data-url'),
    data : {
      "cart_object" : id_product,
      "quantity" : value,
      "action" : action
    },
    error : function() {
      alert("error")
    },
    success:function(){
      input.attr("value",value)
      input.val(value)
      minus = input.siblings(".minus")
      plus = input.siblings(".plus")
      max = input.attr("max")
      update_button(value, max, minus, plus)

      if ($.contains(document.body, $(".table")[0]))
      {
        update_cart(input, value)
      }
      else
      {
        product_catalog = $(".img_product[data-id="+product+"]")
        product_catalog.attr('data-cart', value)

        if ($("body").hasClass("modal-open"))
        {
          product_catalog_cart = product_catalog.parent().find(".cart_interface")
          input_catalog = product_catalog_cart.find("input")
          input_catalog.attr('value', value)
          input_catalog.val(value)
          minus = input_catalog.siblings(".minus")
          plus = input_catalog.siblings(".plus")
          update_button(value, max, minus, plus)
        }
      }
    },
    dataType : "json"
  });
};

function ajax_remove(input, id_product, action){
  $.ajax({
    type:"POST",
    headers:{'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    url:input.parent(".modif").attr('data-url'),
    data : {
      "cart_object" : id_product,
      "action" : action
    },
    error : function() {
      alert("error")
    },
    success:function(){
      if ($.contains(document.body, $(".table")[0]))
      {
        input.parents("tr").remove();
        update_total_cart()
      }
      else
      {
        var product_catalog = $(".img_product[data-id="+id_product+"]")
        product_catalog.removeAttr('data-cart')
        var cart_elt = input.parents('.cart_interface')
        cart_elt.find(".modif").css("display","none")
        cart_elt.find(".add").css("display","block")

        if ($("body").hasClass("modal-open"))
        {
          var cart_catalog = product_catalog.parent().find('.cart_interface')
          cart_catalog.find(".modif").css("display","none")
          cart_catalog.find(".add").css("display","block")
        }
      }
    },
    dataType : "json"
  });
}

$(".add").click(function(event){
  add_button = $(event.target)
  cart_elt = add_button.parent('.cart_interface')
  quantity = 1
  product = cart_elt.attr('data-id')
  $.ajax({
    type:"POST",
    headers:{'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    url:add_button.attr('data-url'),
    data :
    {
      "quantity" : quantity,
      "product" : product,
    },
    success:function(){
      modify_cart = $(cart_elt.find(".modif"))
      modify_cart.css('display', 'block')
      add_button.css('display','none')

      product_catalog = $(".img_product[data-id="+product+"]")
      product_catalog.attr('data-cart', quantity);

      if ($("body").hasClass("modal-open")) {
        var cart_catalog = product_catalog.parent().find(".cart_interface")
        cart_catalog.find(".modif").css("display","block")
        cart_catalog.find(".add").css("display","none")
        cart_catalog.find(".minus").text("del")
        cart_catalog.find(".minus").addClass("del")
      }

    },
    dataType : "json"
  });
});

$(".changebutton").click(function(event){
  modify_button = $(event.target)
  cart_elt = modify_button.parents(':eq(1)')
  product = cart_elt.attr('data-id')
  input = cart_elt.find("input")
  initial_value = parseInt( input.attr('value') )
  max = parseInt( input.attr("max") )

  if (modify_button.hasClass("plus")) {
    expectedvalue = initial_value+1
  }else{
    expectedvalue = initial_value-1
  }
  if(expectedvalue > max){
    expectedvalue = max
  } else if (expectedvalue <= 0) {
    expectedvalue = 1
  }

  if (modify_button.hasClass("del")) {
    ajax_remove(input, product, "remove")
  }else{
    ajax_update(input, product, expectedvalue, "update")
  }
});

$(".quantity").change(function(event){
  input = $(event.target);
  user_entry = parseInt(input.val());
  max = parseInt(input.attr("max"));

  if ((user_entry <= 0) || (isNaN(user_entry))){
    input.val(1)
    input.attr('value', 1)
  }
  else if (user_entry > max) {
    input.val(max)
    input.attr('value', max)
  }
  else{
    input.attr('value',user_entry)
  }

});

$(".quantity").focusout(function(e){
  input = $(event.target)
  cart_elt = input.parents(':eq(1)')
  product = cart_elt.attr('data-id')
  value = parseInt(input.attr('value'))
  ajax_update(input, product, value, "update")
});
