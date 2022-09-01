class BaseValidationRuleChecks:

    def __init__(self):
        self.__http_get_response__ = None
        self.__customer_event_request__ = None
        self.__rules__ = {}

    def with_response(self, http_response):
        self.__http_get_response__ = http_response

        return self

    def from_event(self, customer_event_request):
        self.__customer_event_request__ = customer_event_request

        return self

    def get_obj(self):  # assume csv or non json
        return self.__http_get_response__.text

    def check_response_present(self):
        pass

    def expect_success_status_code(self):
        self.check_response_present()
        rule_name = "expect_success_status_code"
        if self.__http_get_response__.status_code == 200:
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False

        return self

    def expect_csv_datatype(self):
        self.check_response_present()
        rule_name = "expect_csv_datatype"
        self.__rules__[rule_name] = self.__customer_event_request__.get('datatype', 'json') == 'csv'

        return self

    def get_status_code(self):
        return self.__http_get_response__.status_code

    def is_meaningful_response(self):
        return len(self.__http_get_response__.text) > 0 \
               and "Error Message" not in self.__http_get_response__.text \
               and self.__http_get_response__.text != "{}"\
               and "Note" not in self.__http_get_response__.text


    def expect_successful_response(self):
        self.check_response_present()
        rule_name = "expect_successful_response"
        if self.is_meaningful_response():
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False

        return self

    def passed(self):
        if len(self.__rules__) > 0:
            result = True  # optimistic
            for rule_name in self.__rules__:
                if self.__rules__.get(rule_name, False) == False:
                    result = False  # something failed
                    break
            self.clear()

            return result

        raise AttributeError("You must execute rules before checking if the rules passed")

    def failed(self):
        if len(self.__rules__) > 0:
            result = True  # optimistic
            for rule_name in self.__rules__:
                if self.__rules__.get(rule_name, True) == True:
                    result = False  # something failed
                    break
            self.clear()

            return result

        raise AttributeError("You must execute rules before checking if the rules passed")

    def clear(self):
        self.__rules__ = {}

        return self

    def expect_api_key_in_event(self):
        rule_name = "expect_api_key_in_event"
        if self.__customer_event_request__.get('apikey', None) != None and len(
                self.__customer_event_request__['apikey']) > 0:
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False

        return self

    def expect_limit_not_reached(self):
        rule_name = "has_not_reached_limit"
        response = self.__http_get_response__.text
        if " calls per minute " in response:
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False

        return self

    def get_error_message(self):
        json_response = self.__http_get_response__.json()
        if len(json_response) == 0:
            return "Symbol not found"
        return json_response.get("Error Message", "Unknown")

    def get_note_message(self):
        json_response = self.__http_get_response__.json()

        return json_response.get("Note", "Unknown")

    def get_information_message(self):
        json_response = self.__http_get_response__.json()

        return json_response.get("Information", "Unknown")

    def expect_json_datatype(self):
        self.check_response_present()
        rule_name = "expect_json_datatype"
        content_type = self.__http_get_response__.headers.get('content-type')
        datatype = self.__customer_event_request__.get('datatype', 'json')
        if datatype == 'json' and content_type == 'application/json':
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False
        return self


class JsonValidationRuleChecks(BaseValidationRuleChecks):

    def expect_limit_not_reached(self):
        rule_name = "has_not_reached_limit"
        response = self.__http_get_response__.json()
        self.__rules__[rule_name] = "Note" in response and " calls per minute " in response["Note"]

        return self

    def is_empty_global_quote(self, response_json):
        is_property_count_one = len(response_json) == 1
        has_global_quote_property = "Global Quote" in response_json
        is_global_quote_empty = len(response_json.get("Global Quote", {})) == 0
        return is_property_count_one and has_global_quote_property and is_global_quote_empty

    def expect_successful_response(self):
        self.check_response_present()
        rule_name = "expect_meaningful_json_response"
        is_meaningful = self.is_meaningful_response() and self.__http_get_response__.text != "{}"
        is_not_error_msg = "Error Message" not in self.__http_get_response__.json()
        is_not_info_msg = "Information" not in self.__http_get_response__.json()
        is_not_note_msg = "Note" not in self.__http_get_response__.json()
        is_not_empty_global_quote = not self.is_empty_global_quote(self.__http_get_response__.json())

        if is_meaningful and is_not_error_msg and is_not_info_msg and is_not_note_msg and is_not_empty_global_quote:
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False

        return self

    def get_error_message(self):
        json_response = self.__http_get_response__.json()
        if len(json_response) == 0:
            return "Symbol not found"
        elif "Error Message" in json_response:
            return json_response["Error Message"]
        else:
            return self.__http_get_response__.text  # just give them what came back from the server

    def get_obj(self):
        return self.__http_get_response__.json()


class CsvValidationRuleChecks(BaseValidationRuleChecks):

    def expect_csv_datatype(self):
        self.check_response_present()
        rule_name = "expect_csv_datatype"
        content_type = self.__http_get_response__.headers.get('content-type')
        datatype = self.__customer_event_request__.get('datatype', 'json')
        if datatype == 'csv' and 'application/x-download' in content_type:
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False
        return self

    def expect_error_message_not_present(self):
        self.check_response_present()
        rule_name = "expect_error_message_not_present"
        if "Error Message" not in self.__http_get_response__.text:
            self.__rules__[rule_name] = True
        else:
            self.__rules__[rule_name] = False

        return self


class ValidationRuleChecks:

    def __init__(self):
        self.__rule_checker = None

    def from_customer_request(self, event):
        if event is None:
            raise ValueError("Event must be defined, received None type object")
        if len(event) > 0 and event.get('datatype', 'json') == 'json':
            self.__rule_checker = JsonValidationRuleChecks()
        else:  # assume csv
            self.__rule_checker = CsvValidationRuleChecks()

        return self.__rule_checker.from_event(event)
