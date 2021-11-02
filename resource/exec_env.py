from resource.base import BaseResource

from docstring import docstring
from document.exec_env import ExecEnvDocument, ExecEnvTypeDocument
from schema.exec_env import ExecEnvSchema, ExecEnvTypeSchema


@docstring(ext='yaml')
class ExecEnvResource(BaseResource):
    doc = ExecEnvDocument
    name = 'execution environment'
    names = 'execution environments'
    routes = '/exec-env/'
    schema = ExecEnvSchema


@docstring(ext='yaml')
class ExecEnvSelectedResource(ExecEnvResource):
    routes = '/exec-env/{id}'


@docstring(ext='yaml')
class ExecEnvTypeResource(BaseResource):
    doc = ExecEnvTypeDocument
    name = 'execution environment type'
    names = 'execution environment types'
    routes = '/type/exec-env/'
    schema = ExecEnvTypeSchema


@docstring(ext='yaml')
class ExecEnvTypeSelectedResource(ExecEnvTypeResource):
    routes = '/exec-env-type/{id}'
