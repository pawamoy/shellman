**`{{ function.prototype }}`**
{{ function.brief|e }}

{% if function.description %}
{{ function.description|e }}

{% endif %}
{% if function.arguments %}
*Arguments*
{% for argument in function.arguments %}
**{{ argument|first_word }}** - {{ argument|body }}  
{% endfor %}

{% endif %}
{% if function.return_codes %}
*Return codes*
{% for return_code in function.return_codes %}
**{{ return_code|first_word|e }}** - {{ return_code|body|e }}  
{% endfor %}

{% endif %}
{% if function.preconditions %}
*Pre-conditions*
{% for precondition in function.preconditions %}
{{ precondition|e }}  
{% endfor %}

{% endif %}
{% if function.seealso %}
*See also*
{% for seealso in function.seealso %}
{{ seealso|e }}  
{% endfor %}

{% endif %}
{% if function.stderr %}

{% endif %}
{% if function.stdin %}

{% endif %}
{% if function.stdout %}

{% endif %}
