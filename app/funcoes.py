# -*- coding: utf-8 -*-
from .models import (
    Dia,
    ItemLotacao,
    Disciplina,
    Fluxo,
    Lotacao,
    SalaItemLotacao,
    Sala,
    UsuarioItemLotacao,
    Usuario)
def dia_horario(id_item_lotacao):
    dia_horario = []
    for dia in Dia.query.filter(Dia.item_lotacao_id==id_item_lotacao).all():
        dia_horario_aux = []
        dia_horario_aux.append(dia.dia)
        for horario in dia.horarios:
            dia_horario_aux.append(horario.horario)
        dia_horario.append(dia_horario_aux)
    return dia_horario
def lista_itens_lotacao(id_da_lotacao):
    lista_itens_lotacao = []
    for item_lotacao in ItemLotacao.query.filter(ItemLotacao.lotacao_id==id_da_lotacao).all():
        id_das_salas = [
            sala.sala_id for sala in SalaItemLotacao.query.filter(SalaItemLotacao.item_lotacao_id==item_lotacao.id).all()
        ]
        descricao_salas = [
            Sala.query.get(id).descricao for id in id_das_salas
        ]
        id_dos_usuarios = [
            u.professor_id for u in UsuarioItemLotacao.query.filter(UsuarioItemLotacao.item_lotacao_id==item_lotacao.id).all()
        ]
        nome_professores = [
            Usuario.query.get(id).nome for id in id_dos_usuarios
        ]
        lista_itens_lotacao_aux = []
        lista_itens_lotacao_aux.append(Disciplina.query.get(item_lotacao.diciplina_id).periodo)
        lista_itens_lotacao_aux.append(Disciplina.query.get(item_lotacao.diciplina_id).nome)
        lista_itens_lotacao_aux.append(Fluxo.query.get(Disciplina.query.get(item_lotacao.diciplina_id).fluxo_id).descricao)
        lista_itens_lotacao_aux.append(item_lotacao.turma)
        lista_itens_lotacao_aux.append(Disciplina.query.get(item_lotacao.diciplina_id).carga_horaria)
        lista_itens_lotacao_aux.append(dia_horario(item_lotacao.id))
        lista_itens_lotacao_aux.append(item_lotacao.vagas)
        lista_itens_lotacao_aux.append(
           descricao_salas
        )
        lista_itens_lotacao_aux.append(
            nome_professores
        )
        lista_itens_lotacao.append(lista_itens_lotacao_aux)
    return lista_itens_lotacao

def gera_titulo(id_da_lotacao, tela):
    lotacao = Lotacao.query.get(id_da_lotacao)
    return "Editar Lotação de %s - tela %s de 3" % (str(lotacao.semestre), str(tela))
