$(document).ready(function(){
 //  $('[data-submenu]').submenupicker();
  //
 //  $('#1').hover(function(){
 //     $(this).toggleClass('open');
 //  });
 //  $('#2').hover(function(){
 //     $(this).toggleClass('open');
 //  });
 //  $('#3').hover(function(){
 //     $(this).toggleClass('open');
 //  });

 // Busca as disciplinas para atualizar o template editar_lotacao
 var periodo = $('#periodo');
 periodo.change(function(){
   valor_periodo = $(this).val();
   $.get( "http://localhost:5000/api/get_disciplinas", {valor_periodo : valor_periodo}, function(disciplinas) {
      console.log(disciplinas);
      var $disciplina = $('#disciplina')
      $disciplina.empty()
      $.each(disciplinas, function(index) {
          $disciplina.append($("<option></option>")
             .attr("value", disciplinas[index]).text(disciplinas[index]));
       });
   });
 });

 //console.log('teste ok');

 //faz parte da contrucao do template - vai ser retirado
  var $tipo_relatorio = $('.form-group:eq(0) #tipo').val()
   $('.form-group:eq(' + $tipo_relatorio + ')').removeClass('hidden');

  $('.form-group:eq(0) #tipo').change(function(){
    $('.form-group:eq(' + $tipo_relatorio + ')').addClass('hidden');
    var $tipo_relatorio_atual = $('.form-group:eq(0) #tipo').val();
    $('.form-group:eq(' + $tipo_relatorio_atual + ')').removeClass('hidden');
    $tipo_relatorio = $tipo_relatorio_atual;
  });

  $('#excluir').click(function(){
    confirm("Tem certeza que deseja excluir o {{ tabela }} Fulano de Tal?");
  });


});
