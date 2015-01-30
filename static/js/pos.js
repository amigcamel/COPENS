  $('#showpos').click(function() {
    $('.column').find('span').toggle();
      });
  $("#showpos").click(function () {
    $(this).text(function(i, v){
      return v === 'Show POS' ? 'Hide POS' : 'Show POS'
    });
  });


