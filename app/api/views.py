# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required
from ..models import Disciplina, Coordenacao, Dia, Horario
from . import api
from app import db
from ..funcoes import dia_horario, lista_itens_lotacao, gera_titulo

@api.route('/get_disciplinas')
def get_disciplinas():
    valor_periodo = request.args.get('valor_periodo')
    disciplinas = Disciplina.query.filter_by(periodo=valor_periodo).all()
    nomes_disciplinas = [disciplina.nome for disciplina in disciplinas]
    return jsonify(nomes_disciplinas)

@api.route('/get_professores')
def get_professores():
    id_coordenacao = request.args.get('id_coordenacao')
    coordenacoes = Coordenacao.query.get(int(id_coordenacao))
    nomes_professores = [professor.nome for professor in coordenacoes.usuarios]
    return jsonify(nomes_professores)

@api.route('/set_horario', methods=['GET', 'POST'])
def set_horario():
    dia = request.args.get('dia')
    horario = request.args.get('horario')
    id_item_atual = request.args.get('id_item_atual')
    dia_semana = Dia(dia=dia, item_lotacao_id=id_item_atual )
    db.session.add(dia_semana)
    db.session.commit()
    horario = Horario(
        horario=horario.replace(' ', ''),
        dia_id=dia_semana.id
    )
    db.session.add(horario)
    db.session.commit()
    print dia_horario(id_item_atual)
    return jsonify(dia_horario(id_item_atual))
