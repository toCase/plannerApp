from django.urls import path
from .views import app_index, app_welcome, app_dashboard, app_spec, app_saloon, app_clients, app_service, app_temp_sh, app_report, app_cale, app_shed, app_agent, app_product

urlpatterns = [
    path('', app_index.load, name="app_index"),
    path('welcome/<str:pk>', app_welcome.load, name="app_welcome"),
    path('dashboard', app_dashboard.load, name="app_dashboard"),
    
    
    path('service', app_service.load, name="app_service"),
    path('service_filter', app_service.filter, name="app_service_filter"),
    path('service_add', app_service.add, name="app_service_add"),
    path('service_close', app_service.filter, name="app_service_close"),
    path('service_save/<str:pk>', app_service.save, name="app_service_save"),
    path('service_edit/<str:pk>', app_service.edit, name="app_service_edit"),
    path('service_delete/<str:pk>', app_service.delete, name="app_service_delete"),
    path('service_page/<str:page>', app_service.page, name='app_service_page'),
    
    path('spec', app_spec.load, name="app_spec"),
    path('spec_filter', app_spec.filter, name="app_spec_filter"),
    path('spec_add', app_spec.add, name="app_spec_add"),
    path('spec_close', app_spec.filter, name="app_spec_close"),
    path('spec_save/<str:pk>', app_spec.save, name="app_spec_save"),
    path('spec_edit/<str:pk>', app_spec.edit, name="app_spec_edit"),
    path('spec_delete/<str:pk>', app_spec.delete, name="app_spec_delete"),
    path('spec_page/<str:page>', app_spec.page, name='app_spec_page'),
    
    path('clients', app_clients.load, name="app_clients"),
    path('clients_filter', app_clients.filter, name="app_clients_filter"),
    path('clients_add', app_clients.add, name="app_clients_add"),
    path('clients_close', app_clients.filter, name="app_clients_close"),
    path('clients_save/<str:pk>', app_clients.save, name="app_clients_save"),
    path('clients_edit/<str:pk>', app_clients.edit, name="app_clients_edit"),
    path('clients_delete/<str:pk>', app_clients.delete, name="app_clients_delete"),
    path('clients_page/<str:page>', app_clients.page, name='app_clients_page'),
    
    path('saloon', app_saloon.load, name="app_saloon"),
    path('saloon_filter', app_saloon.filter, name="app_saloon_filter"),
    path('saloon_add', app_saloon.add, name="app_saloon_add"),
    path('saloon_close', app_saloon.close, name="app_saloon_close"),
    path('saloon_save/<str:pk>', app_saloon.save, name="app_saloon_save"),
    path('saloon_edit/<str:pk>', app_saloon.edit, name="app_saloon_edit"),
    path('saloon_delete/<str:pk>', app_saloon.delete, name="app_saloon_delete"),
    path('saloon_page/<str:page>', app_saloon.page, name='app_saloon_page'),
    path('saloon_active/<str:pk>', app_saloon.active, name='app_saloon_active'),
    
    
    path('report', app_report.load, name="app_report"),
    
    path('cale', app_cale.load, name="app_cale"),
    path('cale_next_month/<str:month>/<str:year>', app_cale.next_month, name="app_cale_next_month"),
    path('cale_prev_month/<str:month>/<str:year>', app_cale.prev_month, name="app_cale_prev_month"),
    path('cale_add/<str:day>/<str:month>/<str:year>', app_cale.add, name="app_cale_add"),
    path('cale_close', app_cale.close, name="app_cale_close"),
    path('cale_edit/<str:pk>/<str:day>/<str:month>/<str:year>', app_cale.edit, name='app_cale_edit'),
    path('cale_delete/<str:pk>/<str:day>/<str:month>/<str:year>', app_cale.delete, name='app_cale_delete'),
    path('cale_save/<str:pk>/<str:day>/<str:month>/<str:year>', app_cale.save, name="app_cale_save"),
    path('cale_date/<str:day>/<str:month>/<str:year>', app_cale.select_date, name="app_cale_date"),
    path('cale_spec/<str:day>/<str:month>/<str:year>/<str:spec_id>', app_cale.select_spec, name="app_cale_spec"),
    
    path('shed', app_shed.load, name="app_shed"),
    path('shed_next_month/<str:month>/<str:year>', app_shed.next_month, name="app_shed_next_month"),
    path('shed_prev_month/<str:month>/<str:year>', app_shed.prev_month, name="app_shed_prev_month"),
    path('shed_add/<str:day>/<str:month>/<str:year>', app_shed.add, name="app_shed_add"),
    path('shed_close/<str:day>/<str:month>/<str:year>', app_shed.close, name="app_shed_close"),
    path('shed_date/<str:day>/<str:month>/<str:year>', app_shed.select_date, name="app_shed_date"),
    path('shed_spec/<str:day>/<str:month>/<str:year>/<str:spec_id>', app_shed.select_spec, name="app_shed_spec"),    
    path('meet_add/<str:day>/<str:month>/<str:year>/<str:hour>/<str:minute>/<str:meet_id>', app_shed.meet_add, name='app_meet_add'),
    path('meet_edit/<str:day>/<str:month>/<str:year>/<str:hour>/<str:minute>/<str:meet_id>', app_shed.meet_edit, name='app_meet_edit'),    
    path('meet_save/<str:day>/<str:month>/<str:year>/<str:meet_id>', app_shed.meet_save, name='app_meet_save'),
    path('meet_del/<str:day>/<str:month>/<str:year>/<str:meet_id>', app_shed.meet_del, name='app_meet_del'),
    
    path('meet_postpone/<str:day>/<str:month>/<str:year>/<str:meet_id>', app_shed.meet_postpone, name='app_meet_postpone'),
    
    path('postpone_close/<str:day>/<str:month>/<str:year>', app_shed.postpone_close, name='app_postpone_close'),
    path('postpone_spec', app_shed.postpone_spec, name='app_postpone_spec'),
    path('postpone_time', app_shed.postpone_time, name='app_postpone_time'),
    path('postpone_save/<str:day>/<str:month>/<str:year>/<str:meet_id>', app_shed.postpone_save, name='app_postpone_save'),
    
    path('agent', app_agent.load, name="app_agent"),
    path('agent_filter', app_agent.filter, name="app_agent_filter"),
    path('agent_add', app_agent.add, name="app_agent_add"),
    path('agent_close', app_agent.filter, name="app_agent_close"),
    path('agent_save/<str:pk>', app_agent.save, name="app_agent_save"),
    path('agent_edit/<str:pk>', app_agent.edit, name="app_agent_edit"),
    path('agent_delete/<str:pk>', app_agent.delete, name="app_agent_delete"),
    path('agent_page/<str:page>', app_agent.page, name="app_agent_page"),
    
    path('product/<str:category>', app_product.load, name="app_product"),
    path('product_filter/<str:category>', app_product.filter, name="app_product_filter"),
    path('product_add/<str:category>', app_product.add, name="app_product_add"),
    path('product_save/<str:pk>/<str:category>', app_product.save, name="app_product_save"),
    path('product_edit/<str:pk>/<str:category>', app_product.edit, name="app_product_edit"),
    path('product_close/<str:category>', app_product.filter, name="app_product_close"),
    path('product_delete/<str:pk>/<str:category>', app_product.delete, name="app_product_delete"),
    path('product_page/<str:page>/<str:category>', app_product.page, name="app_product_page"),
    
    path('sh_template', app_temp_sh.load, name='app_sh_template'),
    path('_sh_temp_add', app_temp_sh.add, name='app_sh_template_add'),
    path('_sh_temp_upd/<str:pk>', app_temp_sh.update, name='app_sh_template_upd'),
]