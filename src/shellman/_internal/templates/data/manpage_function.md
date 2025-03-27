**`{{ function.prototype }}`**
{{ function.brief|e }}

{% if function.description %}
{{ function.description|e }}

{% endif %}
{% if function.arguments %}
*Arguments*
{% for argument in function.arguments %}
**{{ argument|firstword }}** - {{ argument|body }}  
{% endfor %}

{% endif %}
{% if function.return_codes %}
*Return codes*
{% for return_code in function.return_codes %}
**{{ return_code|firstword|e }}** - {{ return_code|body|e }}  
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
{% if function.stdin %}
*Standard input*
{% for stdin in function.stdin %}
{{ stdin|e }}
{% endfor %}

{% endif %}
{% if function.stdout %}
*Standard output*
{% for stdout in function.stdout %}
{{ stdout|e }}
{% endfor %}

{% endif %}
{% if function.stderr %}
*Standard error*
{% for stderr in function.stderr %}
{{ stderr|e }}
{% endfor %}

{% endif %}
