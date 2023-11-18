from tinydb import TinyDB, Query


class Database:

    templates: list[dict] = [
        {"name": "Order Form", "user_name": "text", "order_date": "date"},
        {"name": "Contact Form", "user_email": "email", "user_phone": "phone"},
        {"name": "Profile Form", "username": "text", "created": "date",
         "useremail": "email", "userphone": "phone"}
    ]

    def __init__(self, db_file='db.json') -> None:
        self.db = TinyDB(db_file)
        self.forms = self.db.table('forms')

        for template in self.templates:
            self.add_template(template)

    def add_template(self, template: dict) -> None:
        Template = Query()
        if not self.forms.contains(Template.name == template['name']):
            self.forms.insert(template)
            
        

    def get_all_templates(self) -> list:
        return self.forms.all()
