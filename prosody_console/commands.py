from collections import namedtuple
from lua_ast import ast
from lua_ast import printer


class Command(object):

    def __init__(self, ast):
        self.ast = ast

    def show(self):
        return printer.ast_to_string(self.ast)


class Muc(Command):

    @classmethod
    def _call_room_method(cls, room_jid, method_name, method_args):
        """Helper constructor - use other constructors!"""
        room = ast.MethodCall(ast.Var('muc'), ast.Var('room'), [room_jid])
        return cls(ast.MethodCall(room, method_name, method_args))

    @classmethod
    def create(cls, room_jid):
        # muc:create(room)
        return cls(ast.MethodCall(ast.Var('muc'), ast.Var('create'),
                                  [ast.LiteralString(room_jid)]))

    @classmethod
    def get_affiliation(cls, room_jid, jid):
        # muc:room(room):get_affiliation(jid)
        return cls._call_room_method(ast.LiteralString(room_jid),
                                     ast.Var('get_affiliation'),
                                     [ast.Var(ast.LiteralString(jid))])

    # you can use these constants easily - for example:
    #
    #   Muc.set_affiliation("room@example.com", "user@example.com", Muc.Affiliation.member)
    #
    Affiliation = namedtuple('Affiliation', ['owner', 'admin', 'member', 'outcast'])('owner', 'admin', 'member', 'outcast')

    @classmethod
    def set_affiliation(cls, room_jid, jid, affiliation=None):
        # muc:room(room):set_affiliation(actor, jid, affiliation)
        return cls._call_room_method(ast.LiteralString(room_jid),
                                     ast.Var('set_affiliation'),
                                     [ast.Boolean(True),
                                      ast.LiteralString(jid),
                                      ast.LiteralString(affiliation) if affiliation else ast.nil])

    @classmethod
    def get_role(cls, room_jid, nick):
        # muc:room(room):get_role(nick)
        return cls._call_room_method(ast.LiteralString(room_jid),
                                     ast.Var('get_role'),
                                     [ast.LiteralString(nick)])

    @classmethod
    def destroy(cls, room_jid):
        # muc:room(room):destroy()
        return cls._call_room_method(ast.LiteralString(room_jid),
                                     ast.Var('destroy'),
                                     [])
    @classmethod
    def save(cls, room_jid, force):
        # muc:room(room):save(force)
        return cls._call_room_method(ast.LiteralString(room_jid),
                                     ast.Var('save'),
                                     [ast.Boolean(force)])

    @classmethod
    def save_function(cls, room_jid, force):
        # there was a bug in 0.10 series so save method was replaced with.. function
        room = ast.MethodCall(ast.Var('muc'), ast.Var('room'), [ast.LiteralString(room_jid)])
        return cls._call_room_method(ast.LiteralString(room_jid),
                                     ast.Var('save'),
                                     [room, ast.Boolean(force)])
