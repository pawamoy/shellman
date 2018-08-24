### `{{ function.prototype }}`
{{ function.brief }}

{% if function.description %}
{{ function.description }}

{% endif %}
{% if function.arguments %}
#### Arguments
{% for argument in function.arguments %}
- **`{{ argument|first_word }}`**: {{ argument|body }}
{% endfor %}

{% endif %}
{% if function.return_codes %}
#### Return codes
{% for return_code in function.return_codes %}
- **`{{ return_code|first_word }}`**: {{ return_code|body }}
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
{% if function.stderr %}

{% endif %}
{% if function.stdin %}

{% endif %}
{% if function.stdout %}

{% endif %}
