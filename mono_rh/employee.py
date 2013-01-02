# coding: utf-8

import time
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from osv import fields, osv
import tools
from tools.translate import _


class hr_employee_friend_contact(osv.osv):
    _name = 'hr.employee.br.friend.contact'
    _description = "Friend Contact"
    _columns = {
        'name': fields.char('Nome', size=60),
        'contact_id': fields.integer('ID Contato'),
        'telefone': fields.integer('Telefone'),
        'celular': fields.integer('Celular'),
        'relacionamento': fields.char('Relacionamento', size=20),       
    }

hr_employee_friend_contact()


class hr_employee_sst(osv.osv):
    _inherit = 'hr.employee'
    _description = "SST"
    _columns = {
        'tipo_sanguineo': fields.many2one('hr.sst.tipo.sanguineo', 'Tipo Sanguineo'),
        'contact_id': fields.integer('ID Contato'),
        'cor_pele': fields.many2one('hr.sst.pele', 'Cor da pele'),
        'numero_calcado': fields.integer('Numero do calcado'),
        'peso': fields.float('Peso'),
        'employee_altura': fields.float('Altura'),
    }

hr_employee_sst()


class hr_sst_tipo_sanguineo(osv.osv):
    _name = 'hr.sst.tipo.sanguineo'
    _description = "Tipo Sanguineo"
    _columns = {
        'name': fields.char('Nome', size=10),
        'codigo': fields.char('Codigo', size=5),
    }
hr_sst_tipo_sanguineo()


class hr_sst_pele(osv.osv):
    _name = 'hr.sst.pele'
    _description = "SST pele"
    _columns = {
        'name': fields.char('Nome', size=20),
    }

hr_sst_pele()



class hr_employee_br_dependentes(osv.osv):
    _name = 'hr.employee.br.dependentes'
    _description = "Dependentes"
    _columns = {
        'dependente_id': fields.integer('ID'),
        'name': fields.char('Nome', size=60),
        'data_nascimento': fields.date('Data de Nascimento'),
        'idade': fields.integer('Idade'),
        'tipo': fields.selection((('1','Filho(a)'),('2','Mãe'),('3','Pai'),('4','Cônjuge'),('5','Sobrinho(a)'),('6','Tio(a)'),('7','Outros')),'Tipo de Dependente' ),
        'pensao': fields.boolean('Pensão?'),
        'percentual_pensao': fields.float('Percentual da Pensão'),
    }

hr_employee_br_dependentes()


class hr_employee_br_documentos_titulo(osv.osv):
    _name = 'hr.employee.br.documentos.titulo'
    _description = "Titulo"
    _columns = {
        'name': fields.integer('Numero do Titulo'),
        'titulo_id': fields.integer('ID Titulo'),
        'zona': fields.integer('Zona'),
        'secao': fields.integer('Secao'),
    }

hr_employee_br_documentos_titulo()



class hr_employee_br(osv.osv):

    def calcula_idade(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        now = datetime.now()
        for r in self.browse(cr, uid, ids, context=context):
            if r.data_nascimento:
                dob = datetime.strptime(r.data_nascimento,'%Y-%m-%d')
                delta = relativedelta(now,dob)
                result[r.id] = str(delta.years) +" anos e "+ str(delta.months) +" meses"
            else:
                result[r.id] = "Sem Data de Nascimento!"
        return result


    _inherit = 'hr.employee'
    _description = "Employee"
    _columns = {
        'nome_cracha': fields.char('Nome do cracha', size=60),
        'numero_registro': fields.integer('Numero do Registro'),
        'data_nascimento': fields.date('Data Nascimento'),
        'idade': fields.function(calcula_idade, method=True, string='Idade', type='char'),
        'nome_mae': fields.char('Nome da mae', size=60),
        'nome_pai': fields.char('Nome do pai', size=60),
        'estado_civil': fields.char('Estado Civil', size=20),
        'conjuge': fields.char('Conjuge', size=60),
        'dependentes': fields.one2many('hr.employee.br.dependentes', 'dependente_id', 'Dependentes'),
        'sexo': fields.char('Sexo', size=10),
        'friend_contact': fields.one2many('hr.employee.br.friend.contact', 'contact_id', 'Contato'),
        'titulo_eleitor': fields.many2one('hr.employee.br.documentos.titulo', 'Titulo de Eleitor'),
        
    }


    

hr_employee_br()


class hr_employee_br_documentos(osv.osv):
    _inherit = 'hr.employee'
    _description = "Documentos"
    _columns = {
        'rg': fields.char('RG', size=10),
        'orgao_exp_rg': fields.char('Orgao Expedidor', size=80),
        'rg_expedicao': fields.date('RG Data Exp.'),
        'cpf': fields.char('CPF', size=20),
        'pis': fields.char('PIS', size=30),
        'ctps': fields.many2one('hr.employee.br.documentos.ctps', 'CTPS'),
        'reservista': fields.char('Reservista', size=20),
        'passaport': fields.char('Passaport', size=15),
    }

    def _check_cpf(self, cr, uid, ids):

        for employee in self.browse(cr, uid, ids):
            if not employee.cpf:
                continue
    
            if not self._validate_cpf(employee.cpf):
                return False
        return True

    def _validate_cpf(self, cpf):  
            if not cpf.isdigit():
                cpf = re.sub('[^0-9]', '', cpf)

            if len(cpf) != 11:
                return False

            # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
            cpf = map(int, cpf)
            novo = cpf[:9]

            while len(novo) < 11:
                r = sum([(len(novo)+1-i)*v for i, v in enumerate(novo)]) % 11

                if r > 1:
                    f = 11 - r
                else:
                    f = 0
                novo.append(f)

            # Se o número gerado coincidir com o número original, é válido
            if novo == cpf:
                return True
                
            return False
    _constraints = [
                    (_check_cpf, u'CPF invalido!', ['cpf']),
    ]

    _sql_constraints = [
                    ('hr_employee_cpf_uniq', 'unique (cpf)', 
                     u'Já existe um colaborador cadastrado com este CPF!'),
                   
    ]

hr_employee_br_documentos()

class hr_employee_br_documentos_ctps(osv.osv):
    _name = 'hr.employee.br.documentos.ctps'
    _description = "CTPS"
    _columns = {
        'name': fields.integer('Codigo'),
        'atualizacoes': fields.one2many('hr.employee.br.documentos.ctps.atualizacao','atualizacao_id','Atualizacao CTPS'),
    }

hr_employee_br_documentos_ctps()

class hr_employee_br_documentos_ctps_atualizacao(osv.osv):
    _name = 'hr.employee.br.documentos.ctps.atualizacao'
    _description = "CTPS atualizacao"
    _columns = {
        'atualizacao_id': fields.integer('ID'),
        'data': fields.date('Data'),
        'empresa': fields.char('Empresa', size=60),
        'descricao': fields.text('Descricao'),
    }

hr_employee_br_documentos_ctps_atualizacao()

class hr_employee_br_country_city(osv.osv):
    _inherit = 'hr.employee'
    _description = 'Naturalidade'
    _columns = {
        'country_id3': fields.many2one('res.country', 'Nacionalidade'),
        'state_id3': fields.many2one('res.country.state', 'Estado', domain="[('country_id','=',country_id3)]"),
        'naturalidade_employee': fields.many2one('l10n_br_base.city', 'Naturalidade', domain="[('state_id', '=',state_id3)]"),
    }
hr_employee_br_country_city()

class hr_employee_br_international(osv.osv):
    _inherit = 'hr.employee'
    _columns = {
        'estrangeiro': fields.boolean('Estrageiro'),
        'rg_estrageiro': fields.char('RG Estrageiro', size=15,),
        'orgao_exp_rg_extr': fields.char('Orgao Emissao', size=40),
    }
hr_employee_br_international()
