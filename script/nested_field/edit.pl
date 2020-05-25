for (def p: params.data) {{
    def updated = false;
    for (def s: ctx._source.{nested_field}) {{
        if (p.get('id') == s.id) {{
            s.putAll(p);
            updated = true;
        }}
    }}
    if (!updated) {{
        ctx._source.{nested_field}.add(p)
    }}
}}
