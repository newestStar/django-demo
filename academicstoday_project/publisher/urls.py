from django.conf.urls import patterns, include, url
from publisher.views import catalog
from publisher.views import my_publication
from publisher.views import publication

urlpatterns = patterns('',
    # Publications(s)
    url(r'^publish$', catalog.catalog_page),
    url(r'^publication/(\d+)$', publication.publication_page),
                       
    # My Publications
    url(r'^my_publications$', my_publication.my_publications_page),
    url(r'^refresh_publications_table$', my_publication.refresh_publications_table),
    url(r'^my_publication_modal$', my_publication.my_publication_modal),
    url(r'^save_publication$', my_publication.save_publication),
    url(r'^delete_publication$', my_publication.delete_publication),
)
