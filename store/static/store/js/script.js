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
$("#loginform input[name='formchoice']").click(function(){
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
$("#loginform input[name='clienttype']").click(function(){
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
      "choice" : $('#loginform input[name="formchoice"]:checked').val(),
      "email" : $("#loginform input[name='mail']").val(),
      "password" : $("#loginform input[name='password']").val()
    }
    login()
  }
  else if (($('#no_account').is(':checked'))) {
    if ($("#loginform input[name='password']").val() == $(" #loginform input[name='confirmpassword']").val()) {
      data = {
        "choice" : $('#loginform input[name="formchoice"]:checked').val(),
        "type" : $('#loginform input[name="clienttype"]:checked').val(),
        "email" : $("#loginform input[name='mail']").val(),
        "name" : $("#loginform input[name='name']").val(),
        "phone": $("#loginform input[name='phone']").val(),
        "number": $("#loginform input[name='number']").val(),
        "street" : $("#loginform input[name='rue']").val(),
        "cplt" : $("#loginform input[name='cplt']").val(),
        "cp" : $("#loginform input[name='code_postal']").val(),
        "city" : $("#loginform input[name='ville']").val(),
        "password" : $("#loginform input[name='password']").val()
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
        product_catalog = $(".img_product[data-id="+id_product+"]")
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


// ****** UPDATE PROFIL ******
function update_profil(form, data){
  $.ajax({
    type:"POST",
    headers:{'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    url:$(form).attr('action'),
    data : data,
    dataType : "json"
  });
};

$("#update_infos_button").click(function(event){
  var text = $(this).text()
  if (text == "Modifier") {
    $("#infosprofil").hide();
    $("#update_password_form").hide();
    $("#update_infos_form").show();
    $(this).text("retour")
    $("#update_password_button").text('Changer de mot de passe')
  }
  else{
    $("#update_infos_form").hide();
    $("#update_password_form").hide();
    $("#infosprofil").show();
    $(this).text("Modifier")
  }
});

$("#update_password_button").click(function(event){
  var text = $(this).text()
  if (text == "Changer de mot de passe") {
    $("#infosprofil").hide();
    $("#update_infos_form").hide();
    $("#update_password_form").show();
    $(this).text('retour')
    $("#update_infos_button").text("Modifier")
  }
  else{
    $("#infosprofil").show();
    $("#update_infos_form").hide();
    $("#update_password_form").hide();
    $(this).text('Changer de mot de passe')
  }
});

$("#update_infos_form").submit(function(event) {
  event.preventDefault();
  var form = $("#update_infos_form")
  var newinfo = {
    "action" : "update_infos",
    "email" : $("#update_infos_form input[name='mail']").val(),
    "name" : $("#update_infos_form input[name='name']").val(),
    "phone": $("#update_infos_form input[name='phone']").val(),
    "number": $("#update_infos_form input[name='number']").val(),
    "street" : $("#update_infos_form input[name='rue']").val(),
    "cplt" : $("#update_infos_form input[name='cplt']").val(),
    "cp" : $("#update_infos_form input[name='code_postal']").val(),
    "city" : $("#update_infos_form input[name='ville']").val(),
    "password" : $("#update_infos_form input[name='password']").val()
  }
  update_profil(form, newinfo)
});

$("#update_password_form").submit(function(event){
  event.preventDefault();
  var newpass = $("#update_password_form input[name='newpassword']").val();
  var confirmpass = $("#update_password_form input[name='confirmpassword']").val();
  var form = $("#update_password_form");
  var pass = {
    "action" : "update_password",
    "newpassword" : newpass,
    "password" : $("#update_password_form input[name='actualpassword']").val()
  };
  if (newpass == confirmpass) {
    update_profil(form, pass)
  }
  else{
    alert("les mots de passe doivent être identique")
  }
});
