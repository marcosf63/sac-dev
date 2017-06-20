$(document).ready(function(){
 //http://localhost:5000/api/get_professores
 // Busca as disciplinas para atualizar o template editar_lotacao
 var periodo = $('#periodo');
 periodo.change(function(){
   valor_periodo = $(this).val();
   $.get( "http://sac-dev.marcosf.com.br/api/get_disciplinas", {valor_periodo : valor_periodo}, function(disciplinas) {
      console.log(disciplinas);
      var $disciplina = $('#disciplina')
      $disciplina.empty()
      $.each(disciplinas, function(index) {
          $disciplina.append($("<option></option>")
             .attr("value", disciplinas[index]).text(disciplinas[index]));
       });
   });
 });

 // Busca as professores ao utualizar a coordenacao na tela 2 de 3 caso de uso 2
 var coordenacao = $('#coordenacao');
 coordenacao.change(function(){
   id_coordenacao = $(this).val();
   $.get( "http://sac-dev.marcosf.com.br/api/get_professores", {id_coordenacao : id_coordenacao}, function(professores) {
      console.log(professores);
      var $professor = $('#professor')
      $professor.empty()
      $.each(professores, function(index) {
          $professor.append($("<option></option>")
             .attr("value", professores[index]).text(professores[index]));
       });
   });
 });

 // Acrescenta horario ao item_lotacao
 var dia = $("#dia")
 var horario = $("#horario")
 var id_item_atual = $("#id_item_atual")
 var adicionar_btn = $('#adicionar');
 var horario_cel = $('#horario_cel')

 adicionar_btn.click(function(){
   $.get( "http://sac-dev.marcosf.com.br/api/set_horario",
           {
              dia : dia.val(),
              horario : horario.val(),
              id_item_atual : id_item_atual.val()
           },
           function(dados) {
            //  $.each(dados, function(index, value) {
            //     $.each(value, function(index, value) {
            //        console.log(value)
            //     });
            //   });
            location.reload();
           }
    );
});



 //console.log('teste ok');

 //faz parte da contrucao do template - vai ser retirado
  // var $tipo_relatorio = $('.form-group:eq(0) #tipo').val()
  //  $('.form-group:eq(' + $tipo_relatorio + ')').removeClass('hidden');
  //
  // $('.form-group:eq(0) #tipo').change(function(){
  //   $('.form-group:eq(' + $tipo_relatorio + ')').addClass('hidden');
  //   var $tipo_relatorio_atual = $('.form-group:eq(0) #tipo').val();
  //   $('.form-group:eq(' + $tipo_relatorio_atual + ')').removeClass('hidden');
  //   $tipo_relatorio = $tipo_relatorio_atual;
  // });
  //
  // $('#excluir').click(function(){
  //   confirm("Tem certeza que deseja excluir o {{ tabela }} Fulano de Tal?");
  // });


});
