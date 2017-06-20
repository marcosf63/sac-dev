# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import main
from app import db
from ..models import (
    Lotacao,
    ItemLotacao,
    Disciplina,
    Dia,
    Fluxo,
    Coordenacao,
    Usuario,
    Sala,
    UsuarioItemLotacao,
    SalaItemLotacao
)
from ..funcoes import dia_horario, lista_itens_lotacao, gera_titulo
from .forms import (
      SemestreForm,
      ProfHoraSalaForm,
      AuditoriaForm,
      LotacaoProfForm,
      CadastroUsuariosForm,
      #SelecionaEditarExcluirUsuarioForm,
      #EditarExcluirUsuarioForm,
      CadastroDisciplinaForm,
      EditarDisciplinaForm,
      CadastroFluxoForm,
      EditarFluxoForm,
      CadastroCoordenacaoForm,
      EditarCoordenacaoForm,
      CadastroSalaForm,
      EditarSalaForm,
      SolicitarProfessorForm,
      LotacaoProfForm,
      #SelecionarEditarExcluiDisicplinaForm,
      #EditarExcluirDisciplinaForm,
      #EditarExcluirDisciplinaForm,
      RelatorioLotacaoPorForm,
      ReLotacaoPorProfessorForm,
      EditarUsuariosForm,
      dias,
      periodos,
      turnos,
      LotacaoForm1,
      LotacaoForm2,
      LotacaoForm3,

)
import csv
import os

#Caso de Uso 1
@main.route('/')
def index():
    return redirect(url_for('auth.login'))

@main.route('/home')
@login_required
def home():
    lotacoes = Lotacao.query.filter_by(
        coordenacao_id=current_user.coordenacao_id,
        situacao='Em andamento'
    ).all()
    solicitacoes_pendentes = ItemLotacao.query.filter_by(
        in_solitacao = 'S',
        status_solcitacao_id = 1
    ).all()
    return render_template('index.html', lotacoes=lotacoes, solicitacoes_pendentes=solicitacoes_pendentes)

#Caso de Uso 2
@main.route('/lotacao', methods=['GET', 'POST'])
@login_required
def lotacao():
    form = SemestreForm()
    lotacoes = Lotacao.query.filter_by(coordenacao_id=current_user.coordenacao_id).all()
    if form.validate_on_submit():
        lotacao = Lotacao(
            semestre=form.semestre.data,
            coordenacao_id=current_user.coordenacao_id,
            situacao="Em andamento"
        )
        db.session.add(lotacao)
        db.session.commit()
        form.semestre.data = ""
        lotacoes = Lotacao.query.filter_by(coordenacao_id=current_user.coordenacao_id).all()
        return render_template('lotacao.html', form=form, lotacoes=lotacoes)
    return render_template('lotacao.html', form=form, lotacoes=lotacoes)



#Caso de Uso 2
@main.route('/editar_lotacao', methods=['GET', 'POST'])
@login_required
def editar_lotacao():
    id_da_lotacao = request.args.get('id_da_lotacao')
    titulo = gera_titulo(id_da_lotacao, 1)
    form = LotacaoForm1()
    disciplinas = Disciplina.query.filter(Disciplina.periodo!='').all()
    periodos = set([disciplina.periodo for disciplina in disciplinas])
    form.periodo.choices = [(periodo, periodo) for periodo in periodos]
    disciplinas_por_periodo = Disciplina.query.filter(Disciplina.periodo==1).all()
    form.disciplina.choices = [(disciplina.nome,disciplina.nome) for disciplina in disciplinas_por_periodo]

    if request.method == 'POST':
        disciplina = Disciplina.query.filter(Disciplina.nome==form.disciplina.data).all()
        item_atual  = ItemLotacao (
            lotacao_id = id_da_lotacao,
            diciplina_id = disciplina[0].id,
            turma = form.turma.data,
            vagas = form.vagas.data
        )
        db.session.add(item_atual)
        db.session.commit()
        id_item_atual = item_atual.id
        return redirect(url_for('main.editar_lotacao2', id_da_lotacao=id_da_lotacao, id_item_atual=id_item_atual))
    return render_template('editarLotacao.html', titulo=titulo.decode('utf-8'), form=form, lista_itens_lotacao=lista_itens_lotacao(id_da_lotacao))

#Caso de Uso 2
@main.route('/editar_lotacao2', methods=['GET', 'POST'])
@login_required
def editar_lotacao2():
    id_da_lotacao = request.args.get('id_da_lotacao')
    id_item_atual = request.args.get('id_item_atual')
    titulo = gera_titulo(id_da_lotacao, 2)
    form = LotacaoForm2()
    coordenacoes = Coordenacao.query.all()
    form.coordenacao.choices = [(coordenacao.id,coordenacao.nome) for coordenacao in coordenacoes]
    professores_computacao = Usuario.query.filter(Usuario.coordenacao_id==1,Usuario.tipo=='Professor' ).all()
    form.professor.choices = [(professor.nome,professor.nome) for professor in professores_computacao]
    salas = Sala.query.all()
    campi = list(set([sala.campus for sala in salas]))
    form.campus.choices = [(campus,campus) for campus in campi]
    predios = list(set([sala.localizacao for sala in salas]))
    form.localizacao.choices = [(predio,predio) for predio in predios]
    form.sala.choices = [(sala.descricao,sala.descricao) for sala in salas]
    if request.method == 'POST':
        item_atual = ItemLotacao.query.get(id_item_atual)
        professor = Usuario.query.filter(Usuario.nome==form.professor.data).all()
        if current_user.coordenacao_id == professor[0].coordenacao_id:
            item_atual.in_solitacao = 'N'
            item_atual.status_solcitacao_id = 5
        else:
            item_atual.in_solitacao = 'S'
            item_atual.status_solcitacao_id = 1
        usuario_item_lotacao = UsuarioItemLotacao()
        usuario_item_lotacao.professor_id = professor[0].id
        usuario_item_lotacao.item_lotacao_id = item_atual.id
        #salas_itens_lotacoes.
        sala = Sala.query.filter(
            Sala.campus == form.campus.data,
            Sala.localizacao == form.localizacao.data,
            Sala.descricao == form.sala.data
        ).all()
        sala_item_lotacao = SalaItemLotacao(
            sala_id = sala[0].id,
            item_lotacao_id = item_atual.id
        )
        db.session.add_all([item_atual, usuario_item_lotacao, sala_item_lotacao])
        db.session.commit()
        return redirect(url_for('main.editar_lotacao3', id_da_lotacao=id_da_lotacao,id_item_atual=id_item_atual))
    return render_template('editarLotacao.html', titulo=titulo.decode('utf-8'), form=form, lista_itens_lotacao=lista_itens_lotacao(id_da_lotacao))

#Caso de Uso 2
@main.route('/editar_lotacao3', methods=['GET', 'POST'])
@login_required
def editar_lotacao3():
    id_da_lotacao = request.args.get('id_da_lotacao')
    id_item_atual = request.args.get('id_item_atual')
    print id_da_lotacao
    titulo = gera_titulo(id_da_lotacao, 3)
    form = LotacaoForm3()
    if request.method == 'POST':
        return redirect(url_for('main.editar_lotacao', id_da_lotacao=id_da_lotacao))
    return render_template('editarLotacao3.html', titulo=titulo.decode('utf-8'), form=form, lista_itens_lotacao=lista_itens_lotacao(id_da_lotacao), id_item_atual=id_item_atual)



# #Caso de Uso 2 (tela 2 de 2)
# @main.route('/editar_lotacao2', methods=['GET', 'POST'])
# def editar_lotacao2():
#     titulo = "Editar Lotação"
#     return render_template('editarLotacao2.html', titulo=titulo.decode('utf-8'))



@main.route('/alocar02')
def alocar02():
    form = ProfHoraSalaForm()
    if form.validate_on_submit():
        pass
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        #     login_user(user, form.remember_me.data)
        #     return redirect(request.args.get('next') or url_for('main.index'))
        # flash('Invalid username or password.')
    return render_template('alocar02v2.html', form=form)

@main.route('/alocar03')
def alocar03():
    form = AlocacaoForm()
    if form.validate_on_submit():
        pass
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        #     login_user(user, form.remember_me.data)
        #     return redirect(request.args.get('next') or url_for('main.index'))
        # flash('Invalid username or password.')
    return render_template('alocar03.html', form=form)

#Caso de Uso 3
@main.route('/rel_lotacao_por', methods=['GET', 'POST'])
def rel_lotacao_por():
    form = RelatorioLotacaoPorForm()
    msg = ""
    msg2= ""
    exibir_form = True
    if request.method == 'POST':
        tipo = ['por Periodo', 'por Dia', 'por Turno']
        if int(form.tipo.data) is 1:
            msg2 = periodos[int(form.periodo.data) - 1][int(form.periodo.data)]
        elif int(form.tipo.data) is 2:
            msg2 = dias[int(form.diaSemana.data) - 1][int(form.diaSemana.data)]
        else:
            msg2 = turnos[int(form.turno.data) - 1][int(form.turno.data)]
        msg = tipo[int(form.tipo.data)-1]
        exibir_form = False
        return render_template('re_lotacao_por.html', form=form, msg=msg, msg2=msg2, exibir_form=exibir_form)
    return render_template('re_lotacao_por.html', form=form, msg=msg, msg2=msg2, exibir_form=exibir_form)

# Caso de Uso 4
@main.route('/rel_PROGRAD')
def rel_PROGRAD():
    return render_template('re_PROGRAD.html')


# Caso de Uso 5
@main.route('/rel_cedidos')
def rel_cedidos():
    return render_template('re_cedidos.html')

# Caso de Uso 6
@main.route('/rel_lotacao_por_professor', methods=['GET', 'POST'])
def rel_lotacao_por_professor():
    form = ReLotacaoPorProfessorForm()
    exibir_form = True
    if request.method == 'POST':
        exibir_form = False
        return render_template('re_lotacao_professor.html', form=form, exibir_form=exibir_form)
    return render_template('re_lotacao_professor.html', form=form, exibir_form=exibir_form)

@main.route('/rel_lotacao_por_professor2')
def rel_lotacao_por_professor_2():
    return render_template('re_lotacao_professor2.html')

# Caso de Uso 7
@main.route('/gerenciar_usuario', methods=['GET', 'POST'])
def gerenciar_usuario():
    tabela = 'usuario'
    form = CadastroUsuariosForm()
    titulo = "Cadastro de Usuários"
    dados = [
      { 'Email':'nome@servidor.com',
       'Nome' : 'Fulano de Tal',
       'Telefone' : '(88)99999-9999',
       'Lattes' : 'http://www.lathes.com/fulano',
      'Tipo' : 'Professor'},
       { 'Email':'nome@servidor.com',
        'Nome' : 'Fulano de Tal',
        'Telefone' : '(88)99999-9999',
        'Lattes' : 'http://www.lathes.com/fulano',
       'Tipo' : 'Professor'},
        { 'Email':'nome@servidor.com',
         'Nome' : 'Fulano de Tal',
         'Telefone' : '(88)99999-9999',
         'Lattes' : 'http://www.lathes.com/fulano',
        'Tipo' : 'Professor'},
    ]
    if request.method == 'POST':
        cargo = ['Coordenador', 'Professor', 'Servidor', 'Estagiário']
        dados.append(
          [form.email.data,
          form.nome.data,
          form.telefone.data,
          form.lattes.data,
          cargo[int(form.cargo.data)-1]]
        )
        return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)
    form.email.data = " "
    form.nome.data = " "
    form.telefone.data = " "
    form.lattes.data = " "
    return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)


@main.route('/editar_usuario', methods=['GET','POST'])
def editar_usuario():
    form = EditarUsuariosForm()
    titulo = "Editar Usuários"
    form.email.data = "nome@servidor.com"
    form.nome.data = "Fulano de Tal"
    form.telefone.data = "(88)99999-9999"
    form.lattes.data = "http://www.lathes.com/fulano"
    if request.method == 'POST':
        flash(u"Usuário editado com sucesso")
        return redirect(url_for('main.gerenciar_usuario'))
    return render_template('editar.html', form=form, titulo=titulo.decode('utf-8'))

@main.route('/excluir_usuario')
def excluir_usuario():
    flash(u"Usuário excluído com sucesso")
    return redirect(url_for('main.gerenciar_usuario'))

#Caso de Uso 8
@main.route('/gerenciar_disciplina', methods=['GET', 'POST'])
def gerenciar_disciplina():
    tabela = 'disciplina'
    form = CadastroDisciplinaForm()
    titulo = "Cadastro de Disciplina"
    dados = [
      {'Nome' : 'Engenharia de Software',
        'CH' : '80',
        'Fluxo' : '2016.1'},
       {'Nome' : u'Cálculo I',
         'CH' : '80',
         'Fluxo' : '2012.1'},
        {'Nome' : u'Laboratório de Desenvolvimento de Software',
          'CH' : '80',
          'Fluxo' : '2016.1'}
    ]
    if request.method == 'POST':
        fluxo = ['2012.1', '2016.1']
        dados.append(
          {'Nome' : form.nome.data,
          'CH' : form.cargaHoraria.data,
          'Fluxo' : fluxo[int(form.fluxo.data)-1]}
        )
        return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)
    form.nome.data = " "
    form.cargaHoraria.data = " "
    return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)


@main.route('/editar_disciplina', methods=['GET','POST'])
def editar_disciplina():
    form = EditarDisciplinaForm()
    titulo = "Editar Disciplina"
    form.nome.data = u"Cálculo I"
    form.cargaHoraria.data = "80"
    if request.method == 'POST':
        flash(u"Disciplina editada com sucesso")
        return redirect(url_for('main.gerenciar_disciplina'))
    return render_template('editar.html', form=form, titulo=titulo.decode('utf-8'))

@main.route('/excluir_disciplina')
def excluir_disciplina():
    flash(u"Disciplina excluída com sucesso")
    return redirect(url_for('main.gerenciar_disciplina'))

#Caso de Uso 9
@main.route('/gerenciar_fluxo', methods=['GET', 'POST'])
def gerenciar_fluxo():
    tabela = 'fluxo'
    form = CadastroFluxoForm()
    titulo = "Cadastro de Fluxo"
    dados = [
      {'Fluxo' : '2016.1'},
      {'Fluxo' : '2012.1'}
    ]
    if request.method == 'POST':
        dados.append(
          {'Fluxo' : form.fluxo.data}
        )
        return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)
    form.fluxo.data = " "
    return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)


@main.route('/editar_fluxo', methods=['GET','POST'])
def editar_fluxo():
    form = EditarFluxoForm()
    titulo = "Editar Fluxo"
    form.fluxo.data = u"2012.1"
    if request.method == 'POST':
        flash(u"Fluxo editado com sucesso")
        return redirect(url_for('main.gerenciar_fluxo'))
    return render_template('editar.html', form=form, titulo=titulo.decode('utf-8'))

@main.route('/excluir_fluxo')
def excluir_fluxo():
    flash(u"Fluxo excluído com sucesso")
    return redirect(url_for('main.gerenciar_fluxo'))

#Caso de Uso 10
@main.route('/gerenciar_coordenacao', methods=['GET', 'POST'])
def gerenciar_coordenacao():
    tabela = 'coordenacao'
    form = CadastroCoordenacaoForm()
    titulo = "Cadastro de Coordenação"
    dados = [
      {'Nome' : u'Matemática'},
      {'Nome' : u'Computação'}
    ]
    if request.method == 'POST':
        dados.append(
          {'Fluxo' : form.nome.data}
        )
        return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)
    form.nome.data = " "
    return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)


@main.route('/editar_coordenacao', methods=['GET','POST'])
def editar_coordenacao():
    form = EditarCoordenacaoForm()
    titulo = "Editar Coordenação"
    form.nome.data = u"Matemática"
    if request.method == 'POST':
        flash(u"Coordenação editada com sucesso")
        return redirect(url_for('main.gerenciar_coordenacao'))
    return render_template('editar.html', form=form, titulo=titulo.decode('utf-8'))

@main.route('/excluir_coordenacao')
def excluir_coordenacao():
    flash(u"Coordenação excluída com sucesso")
    return redirect(url_for('main.gerenciar_coordenacao'))


#Caso de Uso 11
@main.route('/gerenciar_sala', methods=['GET', 'POST'])
def gerenciar_sala():
    tabela = 'sala'
    form = CadastroSalaForm()
    titulo = "Cadastro de Salas"
    dados = [
      {
        u'Número' : u'45',
        u'Tipo' : u'Padrão',
        u'Campus' : u'Betânia',
        u'Descrição' : u'Sala usada pelo curso de direito'
      },
      {
        u'Número' : u'1',
        u'Tipo' : u'Laboratório',
        u'Campus' : u'Cidao',
        u'Descrição' : u'Sala usada pelo curso de Computação'
      },

    ]
    if request.method == 'POST':
        dados.append(
          {
            u'Número' : form.numero.data,
            u'Tipo' : form.tipo.data,
            u'Campus' : form.campus.data,
            u'Descrição' : form.descricao.data
          }
        )
        return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)
    form.numero.data = " "
    form.descricao.data = " "
    return render_template('gerenciar.html', form=form, titulo=titulo.decode('utf-8'), dados=dados, tabela=tabela)


@main.route('/editar_sala', methods=['GET','POST'])
def editar_sala():
    form = EditarSalaForm()
    titulo = "Editar Sala"
    form.numero.data = "45"
    form.descricao.data = 'Sala usada pelo curso de direito'
    if request.method == 'POST':
        flash(u"Sala editada com sucesso")
        return redirect(url_for('main.gerenciar_sala'))
    return render_template('editar.html', form=form, titulo=titulo.decode('utf-8'))

@main.route('/excluir_sala')
def excluir_sala():
    flash(u"Sala excluída com sucesso")
    return redirect(url_for('main.gerenciar_sala'))

# Caso de uso 012
@main.route('/auditoria', methods=['GET','POST'])
def auditoria():
    form = AuditoriaForm()
    exibir_form = True
    dados = []
    if form.validate_on_submit():
        exibir_form = False
        dados = [
            {u'Data do Evento' : form.data_inicio.data ,
            'Email' : 'usuario@servidor.com',
            u'Operação' : u'Cadastrar Usuário',
            'Dado' : u'Usuário XPTO'},
            {u'Data do Evento' : form.data_inicio.data ,
            'Email' : 'usuario@servidor.com',
            u'Operação' : u'Imprimir Salas',
            'Dado' : u'Todos'},
            {u'Data do Evento' : form.data_fim.data ,
            'Email' : 'usuario@servidor.com',
            u'Operação' : u'Editar Lotação',
            'Dado' : u'2017.2'},
        ]
        return render_template('auditoria.html', form=form, dados=dados, exibir_form=exibir_form)
    return render_template('auditoria.html', form=form, dados=dados, exibir_form=exibir_form)

# Caso de uso 013
@main.route('/solicitar_professor', methods=['GET','POST'])
def solicitar_professor():
    form = SolicitarProfessorForm()
    exibir_form = True
    titulo = "Solicitar Professor"
    dados = []
    if request.method == 'POST':
        exibir_form = False
        dados = [
           [u'Adminstração', u'Computação', 'Segunda ABCD', u'João da Silva', u'17/04/2017',u'Pendente de aprovação'],
           [u'Computação', u'Letras', 'Segunda ABCD', u'Rosa',  u'17/04/2017', u'Pendente de aprovação']
        ]
        return render_template('solicita.html', form=form, titulo=titulo.decode('utf-8'), exibir_form=exibir_form, dados=dados)
    return render_template('solicita.html', form=form, titulo=titulo.decode('utf-8'), exibir_form=exibir_form, dados=dados)

# Caso de uso 014 - aprovar solicitação
@main.route('/aprovar_solcitacao')
def aprovar_solcitacao():
    form = None
    exibir_form = False
    titulo = "Aprovar Solicitação"
    dados = [
       [u'Adminstração', u'Computação', 'Segunda ABCD', u'João da Silva', u'17/04/2017',u'Pendente de aprovação'],
       [u'Computação', u'Letras', 'Segunda ABCD', u'Rosa',  u'17/04/2017', u'Pendente de aprovação']
    ]
    return render_template('solicita.html', form=form, titulo=titulo.decode('utf-8'), exibir_form=exibir_form, dados=dados)
# @main.route('/selecionar_usuario')
# def selecionar_usuario():
#     form = SelecionaEditarExcluirUsuarioForm()
#     titulo = "Selecionar de Usuários"
#     if form.validate_on_submit():
#         pass
#     return render_template('cadastro.html', form=form, titulo=titulo.decode('utf-8'))

# @main.route('/editar_usuario')
# def editar_usuario():
#     form = EditarExcluirUsuarioForm()
#     titulo = "Editar Usuários"
#     if form.validate_on_submit():
#         pass
#     form.email.data = "email@.com.br"
#     form.nome.data  = "Fulano de Tal"
#     form.tipo.data = 3
#     return render_template('editarExcluir.html', form=form, titulo=titulo.decode('utf-8'))

# @main.route("/edicao_usuario_com_sucesso")
# def edicao_usuario_com_sucesso():
#     flash(u"Usuário editado com sucesso")
#     return redirect(url_for('main.profile'))

# @main.route('/excluir_usuario')
# def excluir_usuario():
#     form = EditarExcluirUsuarioForm()
#     titulo = "Exluir Usuários"
#     if form.validate_on_submit():
#         pass
#     form.email.data = "email@.com.br"
#     form.nome.data  = "Fulano de Tal"
#     form.tipo.data = 3
#     return render_template('editarExcluir.html', form=form, titulo=titulo.decode('utf-8'))

# @main.route("/exclusao_usuario_com_sucesso")
# def exclusao_usuario_com_sucesso():
#     flash(u"Usuário excluído com sucesso")
#     return redirect(url_for('main.profile'))
#
# @main.route('/rel_usuarios')
# def rel_usuarios():
#     titulo = "Relatório de Usuarios"
#     dados = [
#       {
#         'Nome' : u'José Alex Pontes Martins',
#         'Email': 'alex@email.com',
#         'Tipo': 'Coordenador'
#       },
#       {
#         'Nome' : 'Thales Damasceno de Andrade',
#         'Email': 'thales@email.com',
#         'Tipo': 'Professor'
#       },
#       {
#         'Nome' : u'João da Silva',
#         'Carga': 'joao@email.com',
#         'Tipo': 'Servidor'
#       }
#     ]
#     return render_template('relatorio.html', titulo=titulo.decode('utf-8'), dados=dados)
#
# # Caso de Uso 10
# @main.route('/cadastrar_disciplina')
# def cadastrar_disciplina():
#     form = CadastroDisicplinaForm()
#     titulo = "Cadastro de Disciplina"
#     if form.validate_on_submit():
#         pass
#     return render_template('cadastro.html', form=form, titulo=titulo.decode('utf-8'))
#
# @main.route('/selecionar_disciplina')
# def selecionar_disciplina():
#     form = SelecionarEditarExcluiDisicplinaForm()
#     titulo = "Selecionar de Disciplina"
#     if form.validate_on_submit():
#         pass
#     return render_template('cadastro.html', form=form, titulo=titulo.decode('utf-8'))
#
# @main.route('/editar_disciplina')
# def editar_disciplina():
#     form = EditarExcluirDisciplinaForm()
#     titulo = "Editar Disciplina"
#     if form.validate_on_submit():
#         pass
#     form.nome.data = "Engenharia de Software"
#     form.cargaHoraria.data  = 80
#     form.fluxo.data = 1
#     return render_template('editarExcluir.html', form=form, titulo=titulo.decode('utf-8'))
#
# @main.route("/edicao_discplina_com_sucesso")
# def edicao_disciplina_com_sucesso():
#     flash(u"Disciplina editada com sucesso")
#     return redirect(url_for('main.profile'))
#
# @main.route('/excluir_disciplina')
# def excluir_disciplina():
#     form = EditarExcluirDisciplinaForm()
#     titulo = "Exluir Disciplina"
#     if form.validate_on_submit():
#         pass
#     form.nome.data = "Engenharia de Software"
#     form.cargaHoraria.data  = 80
#     form.fluxo.data = 1
#     return render_template('editarExcluir.html', form=form, titulo=titulo.decode('utf-8'))
#
# @main.route("/exclusao_disciplina_com_sucesso")
# def exclusao_disciplina_com_sucesso():
#     flash(u"Disciplina excluída com sucesso")
#     return redirect(url_for('main.profile'))
#
# @main.route('/rel_diciplinas')
# def rel_disciplinas():
#     titulo = "Relatório de Discplinas"
#     dados = [
#       {
#         'Nome' : 'Engenharia de Software',
#         'Carga': '80',
#         'Fluxo': '2016.1'
#       },
#       {
#         'Nome' : u'Laboratório de Software',
#         'Carga': '80',
#         'Fluxo': '2016.1'
#       },
#       {
#         'Nome' : 'Bancos de Dados I',
#         'Carga': '80',
#         'Fluxo': '2016.1'
#       }
#     ]
#     return render_template('relatorio.html', titulo=titulo.decode('utf-8'), dados=dados)
#
#
# #########################################

#
# @main.route('/lotacaoprof')
# def lotacaoprof():
#     form = LotacaoProfForm()
#     if form.validate_on_submit():
#         pass
#         # user = User.query.filter_by(email=form.email.data).first()
#         # if user is not None and user.verify_password(form.password.data):
#         #     login_user(user, form.remember_me.data)
#         #     return redirect(request.args.get('next') or url_for('main.index'))
#         # flash('Invalid username or password.')
#     return render_template('re_lotacao.html', form=form)
#
#
#
#
#
#
#
#
#
#
# # Gerenciar Coordenacoes
# @main.route('/incluir_coordenacao')
# def incluir_cordencao():
#     form = IncluirCoordenacaoForm()
#     if form.validate_on_submit():
#         pass
#         # user = User.query.filter_by(email=form.email.data).first()
#         # if user is not None and user.verify_password(form.password.data):
#         #     login_user(user, form.remember_me.data)
#         #     return redirect(request.args.get('next') or url_for('main.index'))
#         # flash('Invalid username or password.')
#     return render_template('incluir_coordenacao.html', form=form)
#
# @main.route('/selecionar_coordenacao')
# def selecionar_coordenacao():
#     form = SelecionarCoordenacaoForm()
#     if form.validate_on_submit():
#         pass
#         # user = User.query.filter_by(email=form.email.data).first()
#         # if user is not None and user.verify_password(form.password.data):
#         #     login_user(user, form.remember_me.data)
#         #     return redirect(request.args.get('next') or url_for('main.index'))
#         # flash('Invalid username or password.')
#     return render_template('alterar_coordenacao.html', form=form)
#
# @main.route('/alterar_coordenacao')
# def alterar_coordenacao():
#     form = IncluirCoordenacaoForm()
#     if form.validate_on_submit():
#         pass
#         # user = User.query.filter_by(email=form.email.data).first()
#         # if user is not None and user.verify_password(form.password.data):
#         #     login_user(user, form.remember_me.data)
#         #     return redirect(request.args.get('next') or url_for('main.index'))
#         # flash('Invalid username or password.')
#     return render_template('alterar_coordenacao.html', form=form)
#
# @main.route('/excluir_coordenacao0')
# def excluir_coordenacao0():
#     form = SelecionarCoordenacaoForm()
#     if form.validate_on_submit():
#         pass
#         # user = User.query.filter_by(email=form.email.data).first()
#         # if user is not None and user.verify_password(form.password.data):
#         #     login_user(user, form.remember_me.data)
#         #     return redirect(request.args.get('next') or url_for('main.index'))
#         # flash('Invalid username or password.')
#     return render_template('excluir_coordenacao.html', form=form)
#
# @main.route('/excluir_coordenacao')
# def excluir_coordenacao():
#     form = IncluirCoordenacaoForm()
#     if form.validate_on_submit():
#         pass
#         # user = User.query.filter_by(email=form.email.data).first()
#         # if user is not None and user.verify_password(form.password.data):
#         #     login_user(user, form.remember_me.data)
#         #     return redirect(request.args.get('next') or url_for('main.index'))
#         # flash('Invalid username or password.')
#     return render_template('excluir_coordenacao.html', form=form)
#
# @main.route('/rel_coordenacoes')
# def rel_coordenacoes():
#     return render_template('re_coordenacoes.html')
