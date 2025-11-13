from dataclasses import dataclass


@dataclass(frozen=True)
class EmailTemplate:
    subject: str
    body: str

    def render(self, **context) -> "EmailTemplate":
        subject = self._render_template(self.subject, context)
        body = self._render_template(self.body, context)
        return EmailTemplate(subject=subject, body=body)

    def _render_template(self, template: str, context: dict) -> str:
        result = template
        for key, value in context.items():
            result = result.replace(f"${key}", str(value))
        return result
