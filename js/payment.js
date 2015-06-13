$(document).ready(function() {
  $("#payment-form").submit(function(event) {
    event.preventDefault();
    // Deactivate submit button to avoid further clicks
    $('.submit-button').attr("disabled", "disabled");

    paymill.createToken({
      number: $('.card-number').val(),  // required, ohne Leerzeichen und Bindestriche
      exp_month: $('.card-expiry-month').val(),   // required
      exp_year: $('.card-expiry-year').val(),     // required, vierstellig z.B. "2016"
      cvc: $('.card-cvc').val(),                  // required
      amount_int: $('.card-amount-int').val(),    // required, integer, z.B. "15" fÃ¼r 0,15 Euro
      currency: $('.card-currency').val(),    // required, ISO 4217 z.B. "EUR" od. "GBP"
      cardholder: $('.card-holdername').val() // optional
    }, PaymillResponseHandler);                   // Info dazu weiter unten

    return false;
  });

  function PaymillResponseHandler(error, result) {
    if (error) {
      // Shows the error above the form
      $(".payment-errors").text(error.apierror);
      $(".submit-button").removeAttr("disabled");
    } else {
      var form = $("#payment-form");
      // Output token
      var token = result.token;
      // Insert token into form in order to submit to server
      form.append("");
      console.log(result);
    }
  }





});