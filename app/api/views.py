# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required
from ..models import Disciplina
from . import api

@api.route('/get_disciplinas')
def get_disciplinas():
    valor_periodo = request.args.get('valor_periodo')
    disciplinas = Disciplina.query.filter_by(periodo=valor_periodo).all()
    nomes_disciplinas = [disciplina.nome for disciplina in disciplinas]
    return jsonify(nomes_disciplinas)
