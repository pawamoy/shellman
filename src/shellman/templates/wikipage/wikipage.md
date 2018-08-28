{% if doc.sections.brief %}
## Name
**{{ doc.filename }}** - {{ doc.sections.brief[0].text|e }}

{% include "toc.md" with context %}

{% endif %}
{% if doc.sections.usage %}
## Usage
{% for usage in doc.sections.usage %}
- `{{ usage.program }} {{ usage.command }}`
{% endfor %}

{% endif %}
{% if doc.sections.desc %}
## Description
{% for desc in doc.sections.desc %}
{{ desc.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.option %}
## Options
{% for opt_group, opt_list in doc.sections.option|groupby('group', sort=False) %}
{% if opt_group %}
### {{ opt_group }}
{% endif %}
{% for option in opt_list %}
- {% if option.short %}**`{{ option.short }}`**{% if option.long %},{% endif %} {% endif %}{% if option.long %}**`{{ option.long }}`**{% if option.positional %} {% endif %}{% endif %}{% if option.positional %}*`{{ option.positional }}`*{% endif %}:
  {{ option.description|e|indent(2) }}
{% endfor %}
{% if not loop.last %}{{ '\n' }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.env %}
## Environment Variables
{% for env in doc.sections.env %}
- *`{{ env.name }}`*:
  {{ env.description|e|indent(2) }}
{% endfor %}

{% endif %}
{% if doc.sections.file %}
## Files
{% for file in doc.sections.file %}
- *`{{ file.name }}`*:
  {{ file.description|e|indent(2) }}
{% endfor %}

{% endif %}
{% if doc.sections.exit %}
## Exit Status
{% for exit in doc.sections.exit %}
- **`{{ exit.code }}`**:
  {{ exit.description|e|indent(2) }}
{% endfor %}

{% endif %}
{% if doc.sections.stdin %}
## Standard Input
{% for stdin in doc.sections.stdin %}
{{ stdin.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.stdout %}
## Standard Output
{% for stdout in doc.sections.stdout %}
{{ stdout.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.stderr %}
## Standard Error
{% for stderr in doc.sections.stderr %}
{{ stderr.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.function %}
## Functions
{% for function in doc.sections.function %}
{% include "function.md" with context %}
{% if not loop.last %}
---
{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.example %}
## Examples
{% for example in doc.sections.example %}
- **{{ example.title|e }}**
{% if example.code %}
  ```bash
{{ example.code }}
  ```
{% endif %}
{% if example.explanation %}
  {{ example.explanation|e|indent(2) }}
{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.error %}
## Errors
{% for error in doc.sections.error %}
- {{ error.text|e|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.bug %}
## Bugs
{% for bug in doc.sections.bug %}
- {{ bug.text|e|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.caveat %}
## Caveats
{% for caveat in doc.sections.caveat %}
- {{ caveat.text|e|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.author %}
## Authors
{% for author in doc.sections.author %}
- {{ author.text|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.copyright %}
## Copyright
{% for copyright in doc.sections.copyright %}
{{ copyright.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.license %}
## License
{% for license in doc.sections.license %}
{{ license.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.history %}
## History
{% for history in doc.sections.history %}
{{ history.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.note %}
## Notes
{% for note in doc.sections.note %}
{{ note.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if doc.sections.seealso %}
## See Also
{% for seealso in doc.sections.seealso %}
{{ seealso.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}
{% endif %}
