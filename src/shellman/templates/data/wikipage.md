{% if shellman.doc.brief %}
## {{ shellman.filename }}
{{ shellman.doc.brief[0].text|e }}

{% include "wikipage_toc.md" with context %}

{% endif %}
{% if shellman.doc.usage %}
## Usage
{% for usage in shellman.doc.usage %}
- `{{ usage.program }} {{ usage.command }}`
{% endfor %}

{% endif %}
{% if shellman.doc.desc %}
## Description
{% for desc in shellman.doc.desc %}
{{ desc.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.option %}
## Options
{% for opt_group, opt_list in shellman.doc.option|groupby('group', sort=False) %}
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
{% if shellman.doc.env %}
## Environment Variables
{% for env in shellman.doc.env %}
- *`{{ env.name }}`*:
  {{ env.description|e|indent(2) }}
{% endfor %}

{% endif %}
{% if shellman.doc.file %}
## Files
{% for file in shellman.doc.file %}
- *`{{ file.name }}`*:
  {{ file.description|e|indent(2) }}
{% endfor %}

{% endif %}
{% if shellman.doc.exit %}
## Exit Status
{% for exit in shellman.doc.exit %}
- **`{{ exit.code }}`**:
  {{ exit.description|e|indent(2) }}
{% endfor %}

{% endif %}
{% if shellman.doc.stdin %}
## Standard Input
{% for stdin in shellman.doc.stdin %}
{{ stdin.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.stdout %}
## Standard Output
{% for stdout in shellman.doc.stdout %}
{{ stdout.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.stderr %}
## Standard Error
{% for stderr in shellman.doc.stderr %}
{{ stderr.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.function %}
## Functions
{% for function in shellman.doc.function %}
{% include "wikipage_function.md" with context %}
{% if not loop.last %}
---
{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.example %}
## Examples
{% for example in shellman.doc.example %}
- **{{ example.brief|e }}**
{% if example.code %}

  ```{{ example.code_lang }}
{{ example.code }}
  ```

{% endif %}
{% if example.description %}
  {{ example.description|e|indent(2) }}
{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.error %}
## Errors
{% for error in shellman.doc.error %}
- {{ error.text|e|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.bug %}
## Bugs
{% for bug in shellman.doc.bug %}
- {{ bug.text|e|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.caveat %}
## Caveats
{% for caveat in shellman.doc.caveat %}
- {{ caveat.text|e|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.author %}
## Authors
{% for author in shellman.doc.author %}
- {{ author.text|indent(2) }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.copyright %}
## Copyright
{% for copyright in shellman.doc.copyright %}
{{ copyright.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.license %}
## License
{% for license in shellman.doc.license %}
{{ license.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.history %}
## History
{% for history in shellman.doc.history %}
{{ history.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.note %}
## Notes
{% for note in shellman.doc.note %}
{{ note.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}

{% endif %}
{% if shellman.doc.seealso %}
## See Also
{% for seealso in shellman.doc.seealso %}
{{ seealso.text|e }}
{% if not loop.last %}{{ "\n" }}{% endif %}
{% endfor %}
{% endif %}

{% if shellman.credits|default(true, true) %}
<hr><small>Wiki page generated with <a href="https://github.com/pawamoy/shellman">shellman</a></small>
{% endif %}
