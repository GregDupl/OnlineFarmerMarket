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


$('#detailProduct').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var name = button.data('product') + " - " + button.data('variety') // Extract info from data-* attributes
  var prix = button.data('price') + "€ / " + button.data('unity')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text(name)
  modal.find('.price').text(prix)

  var vids = $(".videorecette");
  for (var i = 0; i < vids.length; i++) {
    vids[i].load()
  }

  var active = $(this).find(".active video");
  active[0].play()
})


$("#carouselExampleCaptions").on('slid.bs.carousel', function () {
   var vids = $(this).find(".active video");
   vids[0].currentTime = 0;
   vids[0].play()
})


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
