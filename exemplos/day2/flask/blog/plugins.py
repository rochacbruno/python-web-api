from mistune import markdown


def configure(app):
    # adiciona {{ markdown('texto') }} para os templates
    app.add_template_global(markdown)

    # adiciona {{ date | format_date }}
    app.add_template_filter(lambda date: date.strftime("%d-%m-%Y"), "format_date")
