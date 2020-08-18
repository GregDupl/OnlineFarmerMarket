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
  var name = button.data('product') // Extract info from data-* attributes
  var prix = button.data('price') + "€"
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
