import re
from datetime import datetime
from flask import Flask, request, jsonify

from db import Database


class App:

    validation_error = None

    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.db = Database()

        self.app.route('/get_form', methods=['POST'])(self.get_form)

    def get_form(self):
        """
        Handles a POST request with parameters passed from the form.

        Returns:
            JSON: Returns a JSON response containing either the template name for passed fields or validation errors.
        """

        # Get data from request params
        data = request.args.to_dict()

        # We assign the list to a variable; if it is called again, it is reset
        self.validation_error = []

        # Looking for a suitable template
        for template in self.db.get_all_templates():

            template_fields = set(template.keys()) - {'name'}
            data_keys = set(data.keys())

            if data_keys.issuperset(template_fields):

                # Check each field for validity
                for field in template_fields:
                    if field in data:
                        self.validate(field, data, template)

                # If there are no errors, then we display the form name for the passed fields
                if not self.validation_error:
                    return jsonify({"template_name": template['name']})

                # Display errors
                return jsonify({"error": self.validation_error})

        # If there is no suitable template, we type the fields
        field_types = {field: self.infer_field_type(
            data[field]) for field in data.keys()}
        return jsonify(field_types)

    def validate(self, field: str, data: dict, template: dict) -> None:
        """
        Validates a field based on its type and adds an error message if invalid.

        Args:
            field (str): The name of the field to be validated.
            data (dict): The dictionary containing the field's value.
            template (dict): The template dictionary containing the field's expected type.

        Returns:
            None
        """

        is_valid = self.validate_field(
            value=data[field], field_type=template[field])
        if not is_valid:
            self.validation_error.append(
                f"Field '{field}' is not valid")

    def validate_field(self, value: str, field_type: str):
        """
        Validates a field based on its type.

        Args:
            value (str): The value to be validated.
            field_type (str): The type of the field to be validated.

        Returns:
            bool: True if the value passes validation for the given field type, False otherwise.
        """

        if field_type == "date":
            return self.validate_date(value)

        elif field_type == "phone":
            return self.validate_phone(value)

        elif field_type == "email":
            return self.validate_email(value)

        return True

    def infer_field_type(self, value: str):
        """
        Infers the field type based on the provided value.

        Args:
            value (str): The value to be evaluated.

        Returns:
            str: The inferred type of the value ('date', 'phone', 'email', or 'text').
        """

        match value:
            case val if isinstance(val, str) and self.validate_date(value):
                return "date"
            case val if isinstance(val, str) and self.validate_phone(value):
                return "phone"
            case val if isinstance(val, str) and self.validate_email(value):
                return "email"
            case _:
                return "text"

    def validate_date(self, date_str: str):
        """
        Checks that the date format is correct.

        Args:
            date_str (str): Date string in DD.MM.YYYY format.

        Returns:
            bool: True if the date is in the correct format, False otherwise.
        """

        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def validate_phone(self, phone_str: str):
        """
        Checks the correctness of the phone number format.

        Args:
            phone_str (str): A string representing the phone number.

        Returns:
            bool: True if the number is in the correct format, False otherwise.
        """
        if phone_str.strip():
            value = phone_str.replace(' ', '+', 1) if phone_str[0] == ' ' else phone_str
        
            if len(value) == 12:
                phone_regex = r'^\+7\d{10}$'
                return bool(re.match(phone_regex, value))
        return False

    def validate_email(self, email_str: str):
        """
        Checks the correctness of the email format.

        Args:
            email_str (str): A string representing the email address.

        Returns:
            bool: True if the email is in the correct format, False otherwise.
        """

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email_str)


if __name__ == '__main__':
    app = App()
    app.app.run(debug=True)
