from django.utils.translation import gettext as _


def test_search_dance(francoralite_context):
    francoralite_context.open_homepage(auth_username="")

    url_prefix = "/search_advanced/"

    # Go to advanced search page
    francoralite_context.open_url(url_prefix)

    # Verify the label of the page
    francoralite_context.verify_title(_('Recherche avancée'))

#     # Write first characters of the content
#     francoralite_context.scroll_to_element(
#         by_xpath="//input[@placeholder='" + _("Recherche sur danse") + " ...']").send_keys('va')

#     # There is an option named "valse"
#     francoralite_context.find_element(
#         by_xpath="//p[contains(text(), 'valse')]", visibility_timeout=5)

    #TODO ajouter des tests pour tous les critères

def click_to_list(id_block, id_link, title, context):

    # Go to advanced search page
    url_prefix = "/search_advanced/"
    context.open_url(url_prefix)

    # Link to list
    context.scroll_to_element(by_id=id_block).click()
    context.find_element(by_id=id_link).click()
    context.verify_title(title)

def test_links_to_list(francoralite_context):

    links = [
        {
            'id_block': 'details_genders',
            'id_link': 'link_domain_music',
            'title': 'Genre de musique',
        },
        {
            'id_block': 'details_genders',
            'id_link': 'link_domain_song',
            'title': 'Genre de chanson',
        },
        {
            'id_block': 'details_genders',
            'id_link': 'link_domain_tale',
            'title': 'Genre de conte',
        },
        {
            'id_block': 'details_genders',
            'id_link': 'link_domain_vocal',
            'title': 'Genre vocal',
        },
        {
            'id_block': 'details_genders',
            'id_link': 'link_thematic',
            'title': 'Thématique',
        },
        {
            'id_block': 'details_texts',
            'id_link': 'link_coupe',
            'title': 'Coupe',
        },
        {
            'id_block': 'details_what',
            'id_link': 'link_dance',
            'title': 'Genre de danse',
        },
        {
            'id_block': 'details_what',
            'id_link': 'link_media_type',
            'title': 'Type de média',
        },
        {
            'id_block': 'details_what',
            'id_link': 'link_recording_context',
            'title': 'Contexte d’enregistrement',
        },
        {
            'id_block': 'details_where',
            'id_link': 'link_location',
            'title': 'Lieux',
        },
        {
            'id_block': 'details_who',
            'id_link': 'link_authority_collector',
            'title': 'Enquêteurs',
        },
        {
            'id_block': 'details_who',
            'id_link': 'link_authority_informer',
            'title': 'Informateurs',
        },
    ]

    for link in links:
        click_to_list(
            id_block=link['id_block'],
            id_link=link['id_link'],
            title=link['title'],
            context=francoralite_context
        )