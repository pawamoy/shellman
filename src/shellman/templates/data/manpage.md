{% if shellman.doc.brief %}
**NAME**  
{{ shellman.filename }} - {{ shellman.doc.brief[0].text }}

{% endif %}
{% if shellman.doc.usage %}
**SYNOPSIS**

{% for usage in shellman.doc.usage %}
    {{ usage.program }} {{ usage.command }}
{% endfor %}

{% endif %}
{% if shellman.doc.desc %}
**DESCRIPTION**  
{% for desc in shellman.doc.desc %}
{{ desc.text }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.option %}
**OPTIONS**  
{% for opt_group, opt_list in shellman.doc.option|groupby('group', sort=False) %}
{% if opt_group %}
*{{ opt_group }}*
{% endif %}
{% for option in opt_list %}
{% if option.short %}**`{{ option.short }}`**{% if option.long %},{% endif %} {% endif %}{% if option.long %}**`{{ option.long }}`**{% if option.positional %} {% endif %}{% endif %}{% if option.positional %}*`{{ option.positional }}`*{% endif %}  
{{ option.description|e }}

{% endfor %}
{% endfor %}

{% endif %}
{% if shellman.doc.env %}
**ENVIRONMENT VARIABLES**  
{% for env in shellman.doc.env %}
*`{{ env.name }}`*  
{{ env.description|e }}

{% endfor %}

{% endif %}
{% if shellman.doc.file %}
**FILES**  
{% for file in shellman.doc.file %}
*`{{ file.name }}`*  
{{ file.description|e }}

{% endfor %}

{% endif %}
{% if shellman.doc.exit %}
**EXIT STATUS**  
{% for exit in shellman.doc.exit %}
**`{{ exit.code }}`**
{{ exit.description|e }}

{% endfor %}

{% endif %}
{% if shellman.doc.stdin %}
**STANDARD INPUT**  
{% for stdin in shellman.doc.stdin %}
{{ stdin.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.stdout %}
**STANDARD OUTPUT**  
{% for stdout in shellman.doc.stdout %}
{{ stdout.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.stderr %}
**STANDARD ERROR**  
{% for stderr in shellman.doc.stderr %}
{{ stderr.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.function %}
**FUNCTIONS**  
{% for function in shellman.doc.function %}
{% include "manpage_function.md" with context %}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.example %}
**EXAMPLES**  
{% for example in shellman.doc.example %}
**{{ example.brief|e }}**  
{% if example.code %}
  ```{{ example.code_lang }}
{{ example.code }}
  ```
{% endif %}
{% if example.description %}
{{ example.description|e }}
{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.error %}
**ERRORS**  
{% for error in shellman.doc.error %}
{{ error.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.bug %}
**BUGS**  
{% for bug in shellman.doc.bug %}
{{ bug.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.caveat %}
**CAVEATS**  
{% for caveat in shellman.doc.caveat %}
{{ caveat.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.author %}
**AUTHORS**  
{% for author in shellman.doc.author %}
{{ author.text }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.copyright %}
**COPYRIGHT**  
{% for copyright in shellman.doc.copyright %}
{{ copyright.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.license %}
**LICENSE**  
{% for license in shellman.doc.license %}
{{ license.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.history %}
**HISTORY**  
{% for history in shellman.doc.history %}
{{ history.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.note %}
**NOTES**  
{% for note in shellman.doc.note %}
{{ note.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.seealso %}
**SEE ALSO**  
{% for seealso in shellman.doc.seealso %}
{{ seealso.text|e }}  
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}
{% endif %}
