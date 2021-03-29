from resource.base import Base_Resource

from docstring import docstring
from document.exec_env import Exec_Env_Document, Exec_Env_Type_Document
from schema.exec_env import Exec_Env_Schema, Exec_Env_Type_Schema


@docstring(ext='yaml')
class Exec_Env_Resource(Base_Resource):
    doc = Exec_Env_Document
    name = 'execution environment'
    names = 'execution environments'
    routes = '/exec-env/'
    schema = Exec_Env_Schema


@docstring(ext='yaml')
class Exec_Env_Selected_Resource(Exec_Env_Resource):
    routes = '/exec-env/{id}'


@docstring(ext='yaml')
class Exec_Env_Type_Resource(Base_Resource):
    doc = Exec_Env_Type_Document
    name = 'execution environment type'
    names = 'execution environment types'
    routes = '/type/exec-env/'
    schema = Exec_Env_Type_Schema


@docstring(ext='yaml')
class Exec_Env_Type_Selected_Resource(Exec_Env_Type_Resource):
    routes = '/exec-env-type/{id}'
