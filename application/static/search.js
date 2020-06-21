$(document).ready(function() {

  const example_claims = [
    'Black Tea cures COVID-19',
    'Corona virus was created in chinese lab',
    'COVID-19 is a weapon from America',
    'Corona is just a common cold',
    'Bill Gates is behind the COVID-19 pandemic'
  ]

 // Add event listener to trial button
 $('#trial-btn').on('click', () => {
    let ex_index = Math.floor(Math.random() * example_claims.length);
    $('#query').trigger('focus');
    $('#query').val(example_claims[ex_index]);
 });

});