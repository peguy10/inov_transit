# -*- coding: utf-8 -*-
{
    'name': "INOV TRANSIT",

    'summary': """
        Creation  suivi et Facturation des dossiers de Transit""",

    'description': """
        Long description of module's purpose
    """,

    'author': "INOV CAMEROON",
    'website': "https://www.inov.cm",

    'category': 'Invoices',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','account',
                'snailmail_account',
                'stock',
                'mail'
                ],

    # always loaded
    'data': [
        # 'views/custom_report.xml',
        'data/ir_sequence_data.xml',
        'data/package_data.xml',
        'data/stage_data.xml',
        'data/stock_incoterms_data.xml',
        'data/transit_invoice_data.xml',
        'data/mail_activity_type_data.xml',
        'data/channel_data.xml',
        'data/service_cron_data.xml',
        'wizard/debour_wizard_views.xml',
        'wizard/message_wizard_views.xml',
        'security/transit_invoice_security.xml',
        'security/ir.model.access.csv',
        'views/transit_menu_views.xml',
        'views/prestation_views.xml',
        'views/debours_views.xml',
        'views/folder_views.xml',

        'views/cimaf_report_views.xml',
        'views/placam_report_template.xml',
        'views/sorepco_report_view.xml',
        'views/transit_invoice_report.xml',
        'views/simplify_report_templates.xml',
        'views/account_invoice_views.xml',
        'views/res_partner_views.xml',
        'views/account_config_setting_view.xml',
        'views/analyse_folder_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # "external_dependencies": {"python" : ["CurrencyConverter"]},
    'installable': True,
    'application': True,
    'auto_install': False,
}

