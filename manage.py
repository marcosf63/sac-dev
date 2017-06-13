#!/usr/bin/env python
import os
from app import create_app, db
from carga import (
    carrega_usuarios,
    carrega_disciplina,
    carrega_transacao,
    transacao_por_perfil
)
from app.models import (
    Usuario,
    Perfil_Usuario,
    Perfil,
    Transacao,
    Coordenacao,
    Disciplina,
    Fluxo,
    Sala,
    Lotacao,
    ItemLotacao,
    UsuarioItemLotacao,
    SalaItemLotacao,
    Dia,
    Horario,
    StatusSolicitacao,
    TransacaoPorPerfil
)
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(
        app=app,
        db=db,
        Usuario=Usuario,
        Perfil=Perfil,
        Perfil_Usuario=Perfil_Usuario,
        Transacao=Transacao,
        carrega_usuarios=carrega_usuarios,
        carrega_disciplina=carrega_disciplina,
        carrega_transacao=carrega_transacao,
        transacao_por_perfil=transacao_por_perfil,
        Coordenacao=Coordenacao,
        Disciplina=Disciplina,
        Fluxo=Fluxo,
        Sala=Sala,
        Lotacao=Lotacao,
        ItemLotacao=ItemLotacao,
        UsuarioItemLotacao=UsuarioItemLotacao,
        SalaItemLotacao=SalaItemLotacao,
        Dia=Dia,
        Horario=Horario,
        StatusSolicitacao=StatusSolicitacao,
        TransacaoPorPerfil=TransacaoPorPerfil

    )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
