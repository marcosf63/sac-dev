# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Perfil(db.Model):
    __tablename__ = 'perfis'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    transacoes = db.relationship('TransacaoPorPerfil', backref='transacoes_por_perfil.transacao_id', lazy='dynamic')
    usuarios = db.relationship('Perfil_Usuario', backref='perfis_usuarios.perfil_id', lazy='dynamic')

    def __repr__(self):
        return '<Perfil %r>' % self.nome

class Transacao(db.Model):
    __tablename__ = 'transacoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    perfis = db.relationship('TransacaoPorPerfil', backref='transacoes_por_perfil.perfis_id', lazy='dynamic')

    def __repr__(self):
        return '<Perfil %r>' % self.nome

class TransacaoPorPerfil(db.Model):
    __tablename__ = 'transacoes_por_perfil'
    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.id'))
    transacao_id = db.Column(db.Integer, db.ForeignKey('transacoes.id'))


    def __repr__(self):
        return '<Perfil %r>' % self.nome

class Perfil_Usuario(db.Model):
    __tablename__ = 'perfis_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    # perfil = db.relationship('Perfil', backref='perfis_do_usuario', lazy='dynamic')
    # usuario = db.relationship('Usuario', backref='usuario_do_perfil', lazy='dynamic')

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    nome = db.Column(db.String(64), index=True)
    coordenacao_id = db.Column(db.Integer, db.ForeignKey('coordenacoes.id'))
    password_hash = db.Column(db.String(128))
    tipo = db.Column(db.String(20)) # Professor, Funcionario, Estagiario
    in_coordenador = db.Column(db.String(1)) # S ou N
    pefis = db.relationship('Perfil_Usuario', backref='perfis_usuarios.usuario_id', lazy='dynamic')
    itens_lotacao_usuarios = db.relationship('UsuarioItemLotacao', backref='usuarios_itens_lotacao.itens_lotacao_id', lazy='dynamic')

    def __repr__(self):
        return '<Usuario %r>' % self.nome

    @property
    def password(self):
        raise AttributeError(u'Senha não pode ser lida!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def eh_professor(self):
        return self.tipo == "Professor"

    def eh_funcionario(self):
        return self.tipo == "Funcionario"

    def eh_professor(self):
        return self.tipo == "Estagiario"

    def eh_coordenador(self):
        return self.in_coordenador == "S"

    def __repr__(self):
        return '<User %r>' % self.nome


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Coordenacao(db.Model):
    __tablename__ = 'coordenacoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.UnicodeText(64), unique=True)
    usuarios = db.relationship('Usuario', backref='usuarios', lazy='dynamic')
    lotacoes = db.relationship('Lotacao', backref='lotacoes', lazy='dynamic')

    def __repr__(self):
        return '<Coordenacao %r>' % self.nome

class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    periodo = db.Column(db.Integer)
    carga_horaria = db.Column(db.Integer)
    fluxo_id = db.Column(db.Integer, db.ForeignKey('fluxos.id'))
    in_obrigatorio = db.Column(db.String(1))
    itens = db.relationship('ItemLotacao', backref='itens_lotacao', lazy='dynamic')

    def __repr__(self):
        return '<Disciplina %r>' % self.nome

class Fluxo(db.Model):
    __tablename__ = 'fluxos'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(64), unique=True)
    disciplinas = db.relationship('Disciplina', backref='disciplina', lazy='dynamic')

    def __repr__(self):
        return '<Fluxo %r>' % self.descricao

class Sala(db.Model):
    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(64), unique=True)
    localizacao = db.Column(db.String(64)) # Predio, Edificio, Bloco
    campus = db.Column(db.String(64))
    salas_itens_lotacoes = db.relationship('SalaItemLotacao', backref='salas_itens_lotacao2', lazy='dynamic')

    def __repr__(self):
        return '<Sala %r>' % self.descricao

class Lotacao(db.Model):
    __tablename__ = 'lotacoes'
    id = db.Column(db.Integer, primary_key=True)
    coordenacao_id = db.Column(db.Integer, db.ForeignKey('coordenacoes.id'))
    semestre = db.Column(db.String(64), unique=True)
    situacao = db.Column(db.String(64)) # Encerrada, Em andamento.
    itens = db.relationship('ItemLotacao', backref='itens_lotacao2', lazy='dynamic')

    def __repr__(self):
        return '<Lotacao %r>' % self.semestre

class ItemLotacao(db.Model):
    __tablename__ = 'itens_lotacao'
    id = db.Column(db.Integer, primary_key=True)
    turma = db.Column(db.String(2)) # Turma 1, 2, A, B etc.
    vagas = db.Column(db.Integer)
    in_solitacao = db.Column(db.String(1)) # S = Sim ou N = Nao
    status_solcitacao_id = db.Column(db.Integer, db.ForeignKey('status_solcitacoes.id'))
    lotacao_id = db.Column(db.Integer, db.ForeignKey('lotacoes.id'))
    diciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'))
    itens_lotacao_usuarios = db.relationship('UsuarioItemLotacao', backref='usuarios_itens_lotacao.professor_id', lazy='dynamic')
    salas_itens_lotacoes = db.relationship('SalaItemLotacao', backref='salas_itens_lotacao1', lazy='dynamic')
    dias = db.relationship('Dia', backref='dias', lazy='dynamic')

    def __repr__(self):
        return '<ItemLotacao %r>' % self.turma


class UsuarioItemLotacao(db.Model):
    __tablename__ = 'usuarios_itens_lotacao'
    id = db.Column(db.Integer, primary_key=True)
    professor_id  = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    item_lotacao_id = db.Column(db.Integer, db.ForeignKey('itens_lotacao.id'))

class SalaItemLotacao(db.Model):
    __tablename__ = 'salas_itens_lotacao'
    id = db.Column(db.Integer, primary_key=True)
    sala_id  = db.Column(db.Integer, db.ForeignKey('salas.id'))
    item_lotacao_id = db.Column(db.Integer, db.ForeignKey('itens_lotacao.id'))

class Dia(db.Model):
    __tablename__ = 'dias'
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(10), unique=True) # Segunda, ..., Sabado
    item_lotacao_id = db.Column(db.Integer, db.ForeignKey('itens_lotacao.id'))
    horarios = db.relationship('Horario', backref='horarios', lazy='dynamic')

    def __repr__(self):
        return '<Dia %r>' % self.dia

class Horario(db.Model):
    __tablename__ = 'horarios'
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.String(1), unique=True) # A, ..., S
    dia_id = db.Column(db.Integer, db.ForeignKey('dias.id'))

    def __repr__(self):
        return '<Horario %r>' % self.horario


class StatusSolicitacao(db.Model):
    __tablename__ = 'status_solcitacoes'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(40), unique=True)

    def __repr__(self):
        return '<StatusSolicitacao %r>' % self.descricao

# O status da solcitacao pode ter os seguintes valores
# 1 - Aguardando aprovacao
# 2 - Totalmente aprovada
# 3 - Parcialmente aprovada
# 4 - Rejeitada
