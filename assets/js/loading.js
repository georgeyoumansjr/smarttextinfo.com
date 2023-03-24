
$('#submit-button').on('click', function (){
    $('#loading').show();
    $( "#info-text" ).delay(3000).show("slow","swing");
});
$(document).ready(function() {
    // Check input field values on page load
    checkInputValues();
    
    // Check input field values on input change
    $('.form-control').on('input', checkInputValues);
  });
  
  function checkInputValues() {
    var allValuesEntered = $('.form-control').filter(function() {
        return this.value !== '';
      }).length === $('.form-control').length;
    $('#submit-button').prop('disabled', !allValuesEntered);
  }