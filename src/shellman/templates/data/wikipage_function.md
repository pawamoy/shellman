### `{{ function.prototype }}`
{{ function.brief }}

{% if function.description %}
{{ function.description }}

{% endif %}
{% if function.arguments %}
#### Arguments
{% for argument in function.arguments %}
- **`{{ argument|firstword }}`**: {{ argument|body }}
{% endfor %}

{% endif %}
{% if function.return_codes %}
#### Return codes
{% for return_code in function.return_codes %}
- **`{{ return_code|firstword }}`**: {{ return_code|body }}
{% endfor %}

{% endif %}
{% if function.preconditions %}
#### Pre-conditions
{% for precondition in function.preconditions %}
- {{ precondition }}
{% endfor %}

{% endif %}
{% if function.seealso %}
#### See also
{% for seealso in function.seealso %}
- {{ seealso }}
{% endfor %}

{% endif %}
{% if function.stdin %}
#### Standard input
{% for stdin in function.stdin %}
- {{ stdin }}
{% endfor %}

{% endif %}
{% if function.stdout %}
#### Standard output
{% for stdout in function.stdout %}
- {{ stdout }}
{% endfor %}

{% endif %}
{% if function.stderr %}
#### Standard error
{% for stderr in function.stderr %}
- {{ stderr }}
{% endfor %}

{% endif %}
