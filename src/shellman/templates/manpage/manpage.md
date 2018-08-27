{% if doc.sections.brief %}
**NAME**  
{{ context.indent_str }}{{ doc.filename }} - {{ doc.sections.brief[0].text }}

{% endif %}
{% if doc.sections.usage %}
**SYNOPSIS**

{% for usage in doc.sections.usage %}
{{ context.indent_str }}{{ usage.program }} {{ usage.command }}
{% endfor %}

{% endif %}
{% if doc.sections.desc %}
**DESCRIPTION**  
{% for desc in doc.sections.desc %}
{{ desc.text }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.option %}
**OPTIONS**  
{% for opt_group, opt_list in doc.sections.option|groupby_unsorted('group') %}
{% if opt_group %}
*{{ opt_group }}*
{% endif %}
{% for option in opt_list %}
{% if option.short %}**`{{ option.short }}`**{% if option.long %},{% endif %} {% endif %}{% if option.long %}**`{{ option.long }}`**{% if option.positional %} {% endif %}{% endif %}{% if option.positional %}*`{{ option.positional }}`*{% endif %}  
{{ option.description|e }}

{% endfor %}
{% endfor %}

{% endif %}
{% if doc.sections.env %}
**ENVIRONMENT VARIABLES**  
{% for env in doc.sections.env %}
*`{{ env.name }}`*  
{{ env.description|e }}

{% endfor %}

{% endif %}
{% if doc.sections.file %}
**FILES**  
{% for file in doc.sections.file %}
*`{{ file.name }}`*  
{{ file.description|e }}

{% endfor %}

{% endif %}
{% if doc.sections.exit %}
**EXIT STATUS**  
{% for exit in doc.sections.exit %}
**`{{ exit.code }}`**
{{ exit.description|e }}

{% endfor %}

{% endif %}
{% if doc.sections.stdin %}

{% endif %}
{% if doc.sections.stdout %}

{% endif %}
{% if doc.sections.stderr %}

{% endif %}
{% if doc.sections.function %}
**FUNCTIONS**  
{% for function in doc.sections.function %}
{% include "function.md" with context %}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.example %}
**EXAMPLES**  
{% for example in doc.sections.example %}
**{{ example.title|e }}**  
{% if example.code %}
  ```bash
{{ example.code }}
  ```
{% endif %}
{% if example.explanation %}
{{ example.explanation|e }}
{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.error %}
**ERRORS**  
{% for error in doc.sections.error %}
{{ error.description|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.bug %}
**BUGS**  
{% for bug in doc.sections.bug %}
{{ bug.description|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.caveat %}
**CAVEATS**  
{% for caveat in doc.sections.caveat %}
{{ caveat.description|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.author %}
**AUTHORS**  
{% for author in doc.sections.author %}
{{ author.text }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.copyright %}
**COPYRIGHT**  
{% for copyright in doc.sections.copyright %}
{{ copyright.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.license %}
**LICENSE**  
{% for license in doc.sections.license %}
{{ license.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.history %}
**HISTORY**  
{% for history in doc.sections.history %}
{{ history.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.note %}
**NOTES**  
{% for note in doc.sections.note %}
{{ note.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.seealso %}
**SEE ALSO**  
{% for seealso in doc.sections.seealso %}
{{ seealso.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}
{% endif %}
