# -*- coding: utf-8 -*-

{
    'name' : 'Recursos Humanos Brasil',
    'description' : 'Módulo com funcionalidades e campos adicionais para atender o Brasil',
    'category' : 'Localisation',
    'license': 'AGPL-3',
    'author' : 'Monocon',
    'website' : 'http://www.openerpbrasil.com',
    'version' : '1.0',
    'depends' : ['base','hr','account','hr_contract','hr_holidays', 'l10n_br_base'],
    'init_xml': [],
    'update_xml' : [
        'benefits_view.xml',
        'employee_extension_view.xml',
        'employee_view.xml',
        'hr_contract_view.xml',
        'post_view.xml',
        'post_category_view.xml',
        'post_cbo_view.xml',       
        'schooling_view.xml',
        'syndicate_view.xml',
        'wage_view.xml',
        'hr.post.cbo.csv',

    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': True,
}


