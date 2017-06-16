 # -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField, FieldList
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length, Email
from ..models import Disciplina

turnos = [
  (1, u"MANHÃ"),
  (2, u"TARDE"),
  (3, u"NOITE")
]

periodos = [
  (1, u"1º"),
  (2, u"2º"),
  (3, u"3º"),
  (4, u"4º"),
  (5, u"5º"),
  (6, u"6º"),
  (7, u"7º"),
  (8, u"8º"),
  (9, u"9º")
]

fluxos = [
  (1, '2016.1'),
  (2, '2012.1')
]

disciplinas = [
  (1, u'Cálculo 1'),
  (2, u'Inglês Instrumental'),
  (3, u'Introdução a Ciência da Computção'),
  (4, u'Lógica de Programação')
]

professores = [
  (1, u'Thales'),
  (2, u'Alex'),
  (3, u'Claudio'),
  (4, u'Lorena'),
  (5, u'Placido')
]

salas = [
  (1, u'Sala 40'),
  (2, u'Sala 39'),
  (3, u'Sala 38'),
  (4, u'Sala 37'),
  (5, u'Lab Info')
]

dias = [
   (1, u'Segunda'),
   (2, u"Terça"),
   (3, u"Quarta"),
   (4, u'Quinta'),
   (5, u"Sexta"),
   (6, u'Sabado')
]

coordenacoes = [
   (1, u'Ciências da Computação'),
   (2, u"Matemática"),
   (3, u"Física")
]

cargos = [
   (2, u"Professor"),
   (3, u"Servidor"),
   (4, u"Estagiário")
]

semestre = [
  (1, u"2016.1"),
  (2, u"2017.1"),
  (3, u"2017.1")
]

tipo_ralatorio = [
  (1, u"Por período"),
  (2, u"Por dia"),
  (3, u"Por turno")
]

class SemestreForm(FlaskForm):
    semestre = StringField(u'Informe o semestre', validators=[Required(), Length(1,6)])
    submit = SubmitField(u'Cadastrar Lotação Vazia')


class LotacaoForm1(FlaskForm):
    periodo = SelectField(u'Selecione o Período:', choices=[])
    disciplina = SelectField(u'Selecione a Desciplina:', choices=[])
    turma = StringField(u'Informe a Turma', validators=[Required(), Length(1,3)])
    vagas = StringField(u'Informe o numero de vagas', validators=[Required(), Length(1,3)])
    submit = SubmitField(u'Próximo')

class LotacaoForm2(FlaskForm):
    coordenacao = SelectField(u'Selecione a Coordenacao:',choices=coordenacoes)
    professor = SelectField(u'Selecione Professor:',choices=professores)
    sala =  StringField(u'Informe a Sala', validators=[Required(), Length(1,3)])
    submit = SubmitField(u'Próximo')

class LotacaoForm3(FlaskForm):
    dia =  StringField(u'Informe o dia (Segunda Terca etc)', validators=[Required(), Length(1,10)])
    horario = StringField(u'Informe o horario (ABCD EF etc)', validators=[Required(), Length(1,10)])
    submit = SubmitField(u'Salvar')


# a = BooleanField("A")
# b = BooleanField(u"B")
# c = BooleanField("C")
# d = BooleanField("D")
# e = BooleanField("E")
# f = BooleanField(u"F")
# g = BooleanField("G")
# h = BooleanField(u"H")
# i = BooleanField("I")
# j = BooleanField("J")
# k = BooleanField("K")
# l = BooleanField(u"L")
# m = BooleanField("M")
# n = BooleanField("N")
# o = BooleanField(u"O")
# p = BooleanField("P")
# q = BooleanField("Q")
# r = BooleanField("R")
# s = BooleanField(u"S")

class ProfHoraSalaForm(FlaskForm):
    Professor = SelectField(u'Selecione o Professor:',choices=professores)
    Sala = SelectField(u'Selecione a Sala:',choices=salas)
    #DiaSemana = SelectField(u'Dia da Semana e horário:',choices=dias)
    seg = BooleanField('Seg')
    ter = BooleanField('Ter')
    qua = BooleanField('Qua')
    qui = BooleanField('Qui')
    sex = BooleanField('Sex')
    bab = BooleanField('Sab')
    h1 = BooleanField('A')
    h2 = BooleanField('B')
    h3 = BooleanField('C')
    h4 = BooleanField('D')
    h5 = BooleanField('E')
    h6 = BooleanField('F')
    h7 = BooleanField('G')
    h8 = BooleanField('H')
    submit = SubmitField('Salvar')


class AuditoriaForm(FlaskForm):
    data_inicio = DateField(u'Data de Inicio', validators=[Required(u'Campo Obrigatório')])
    data_fim = DateField(u'Data Fim', validators=[Required(u"Campo Obrigatório")])
    submit = SubmitField(u'Gerar Relatório de Auditoria')

class LotacaoProfForm(FlaskForm):
    Professor = SelectField(u'Selecione o Professor:',choices=professores)
    submit = SubmitField(u'Consultar')

class RelatorioLotacaoPorForm(FlaskForm):
    tipo = SelectField(u'Selecione o tipo de relatório:',choices=tipo_ralatorio)
    periodo = SelectField(u'Selecione o período:',choices=periodos)
    diaSemana = SelectField(u'Dia da Semana:',choices=dias)
    turno = SelectField(u'Turno:',choices=turnos)
    submit = SubmitField(u'Gerar Relatorio')

class ReLotacaoPorProfessorForm(FlaskForm):
    Professor = SelectField(u'Selecione o Professor:',choices=professores)
    submit = SubmitField(u'Gerar Relatório')

class IncluirCoordenacaoForm(FlaskForm):
    Nome = StringField(u'Nome da Coordenação')
    submit = SubmitField(u'Salvar')

class SelecionarCoordenacaoForm(FlaskForm):
    Disciplina = SelectField(u'Selecione a Coordenacao:',choices=coordenacoes)
    submit = SubmitField(u'Alterar')

class CadastroUsuariosForm(FlaskForm):
    email = StringField(u'Email', validators=[Required(), Length(1,64), Email()])
    nome = StringField(u'Nome', validators=[Required(), Length(1,100)])
    telefone = StringField(u'Telefone', validators=[Required(), Length(1,20)])
    lattes = StringField(u'Lattes', validators=[Required(), Length(1,100)])
    cargo = SelectField(u'Selecione o cargo de Usuário:', choices=cargos)
    e_coordenador = BooleanField(u'É Coordenador')
    perfil = SelectField(u'Selecione o perfil de Usuário:', choices=[
                           (1, u"Nível 1"),
                           (2, u"Nível 2"),
                           (3, u"Nível 3")]
                         )
    submit = SubmitField('Cadastrar')

class EditarUsuariosForm(FlaskForm):
    email = StringField(u'Email', validators=[Required(), Length(1,64), Email()])
    nome = StringField(u'Nome', validators=[Required(), Length(1,100)])
    telefone = StringField(u'Telefone', validators=[Required(), Length(1,20)])
    lattes = StringField(u'Lathes', validators=[Required(), Length(1,100)])
    cargo = SelectField(u'Selecione o tipo de Usuário:', choices=cargos)
    e_coordenador = BooleanField(u'É coordenador')
    perfil = SelectField(u'Selecione o cargo de Usuário:', choices=[
                           (1, u"Nível 1"),
                           (2, u"Nível 2"),
                           (3, u"Nível 3")]
                         )
    submit = SubmitField('Salvar')


class CadastroDisciplinaForm(FlaskForm):
    nome = StringField('Nome')
    cargaHoraria = StringField(u'Carga Horária')
    fluxo = SelectField(u'Selecione o Fluxo:',choices=fluxos)
    submit = SubmitField(u'Cadastrar')

class EditarDisciplinaForm(FlaskForm):
    nome = StringField('Nome')
    cargaHoraria = StringField(u'Carga Horária')
    fluxo = SelectField(u'Selecione o Fluxo:',choices=fluxos)
    submit = SubmitField(u'Salvar')

class CadastroFluxoForm(FlaskForm):
    fluxo = StringField('Fluxo')
    submit = SubmitField(u'Cadastrar')

class EditarFluxoForm(FlaskForm):
    fluxo = StringField('Fluxo')
    submit = SubmitField(u'Salvar')

class CadastroCoordenacaoForm(FlaskForm):
    nome = StringField(u'Nome da Coordenação')
    submit = SubmitField(u'Cadastrar')

class EditarCoordenacaoForm(FlaskForm):
    nome = StringField(u'Nome da Coordenação')
    submit = SubmitField(u'Salvar')

class CadastroSalaForm(FlaskForm):
    numero = StringField(u'Número da Sala')
    tipo = SelectField(u'Selecione o tipo de sala:',choices=[(1, u'Padrão'), (2, u'Laboratório')])
    campus = SelectField(u'Selecione o Campus:',choices=[(1, u'Betânia'), (2, u'Cidao')])
    descricao = StringField(u'Descrição da Sala')
    submit = SubmitField(u'Cadastrar')

class EditarSalaForm(FlaskForm):
    numero = StringField(u'Número da Sala')
    tipo = SelectField(u'Selecione o tipo de sala:',choices=[(1, u'Padrão'), (2, u'Laboratório')])
    campus = SelectField(u'Selecione o Campus:',choices=[(1, u'Betânia'), (2, u'Cidao')])
    descricao = StringField(u'Descrição da Sala')
    submit = SubmitField(u'Salvar')

class ManhaForm(FlaskForm):
    a = BooleanField("A")
    b = BooleanField(u"B")
    c = BooleanField("C")
    d = BooleanField("D")
    e = BooleanField("E")
    f = BooleanField(u"F")

class TardeForm(FlaskForm):
    g = BooleanField("G")
    h = BooleanField(u"H")
    i = BooleanField("I")
    j = BooleanField("J")
    k = BooleanField("K")
    l = BooleanField(u"L")
    m = BooleanField("M")

class NoiteForm(FlaskForm):
    n = BooleanField("N")
    o = BooleanField(u"O")
    p = BooleanField("P")
    q = BooleanField("Q")
    r = BooleanField("R")
    s = BooleanField(u"S")


class SolicitarProfessorForm(FlaskForm):
    coordenacao = SelectField(u'Selecione a Coordenação:',choices=[(1, u'Matemática'), (2, u'Fisica')])
    professor = SelectField(u'Selecione o Professor:',choices=[(1, u'João da Silva'), (2, u'Maria da Dores')])
    segunda_manha = FormField(ManhaForm, label=u"Manha")
    segunda_tarde = FormField(TardeForm, label=u"Tarde")
    segunda_noite = FormField(NoiteForm, label=u"Noite")
    terca_manha = FormField(ManhaForm, label=u"Manha")
    terca_tarde = FormField(TardeForm, label=u"Tarde")
    terca_noite = FormField(NoiteForm, label=u"Noite")
    quarta_manha = FormField(ManhaForm, label=u"Manha")
    quarta_tarde = FormField(TardeForm, label=u"Tarde")
    quarta_noite = FormField(NoiteForm, label=u"Noite")
    quinta_manha = FormField(ManhaForm, label=u"Manha")
    quinta_tarde = FormField(TardeForm, label=u"Tarde")
    quinta_noite = FormField(NoiteForm, label=u"Noite")
    sexta_manha = FormField(ManhaForm, label=u"Manha")
    sexta_tarde = FormField(TardeForm, label=u"Tarde")
    sexta_noite = FormField(NoiteForm, label=u"Noite")
    sabado_manha = FormField(ManhaForm, label=u"Manha")
    sabado_tarde = FormField(TardeForm, label=u"Tarde")
    sabado_noite = FormField(NoiteForm, label=u"Noite")
    submit = SubmitField(u'Solicitar')
