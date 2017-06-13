import csv
from app.models import (
    Usuario,
    db,
    Disciplina,
    Transacao,
    TransacaoPorPerfil
)


def carrega_usuarios(arquivo_csv):
    with open(arquivo_csv) as csvfile:
        usuarios = csv.reader(csvfile)
        for linha in usuarios:
            u = Usuario()
            u.email = linha[0]
            u.nome = unicode(linha[1], "utf-8")
            u.tipo = unicode(linha[2], "utf-8")
            u.in_coordenador = linha[3]
            u.coordenacao_id = linha[4]
            u.password="senha"
            db.session.add(u)
            db.session.commit()

def carrega_disciplina(arquivo_csv):
    with open(arquivo_csv) as csvfile:
        disciplinas = csv.reader(csvfile)
        for linha in disciplinas:
            d = Disciplina()
            d.nome = unicode(linha[0],'utf-8')
            d.perirodo = linha[1]
            d.carga_horaria = linha[2]
            d.fluxo_id = linha[3]
            d.in_obrigatorio = linha[4]
            db.session.add(d)
            db.session.commit()

def transacao_por_perfil(arquivo_csv):
    with open(arquivo_csv) as csvfile:
        transacoes_por_perfil = csv.reader(csvfile)
        for linha in transacoes_por_perfil:
            tp = TransacaoPorPerfil()
            tp.perfil_id = linha[0]
            tp.transacao_id = linha[1]
            db.session.add(tp)
            db.session.commit()

def carrega_transacao(arquivo_csv):
    with open(arquivo_csv) as csvfile:
        transacoes = csv.reader(csvfile)
        for linha in transacoes:
            t = Transacao()
            t.nome = unicode(linha[0],'utf-8')
            db.session.add(t)
            db.session.commit()
