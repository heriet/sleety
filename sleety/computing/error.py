from sleety.error import SleetyError


class SleetyComputingResponseError(SleetyError):

    def __init__(self, cp_res):
        self.status_code = cp_res.response.status_code
        self.error_code = None
        self.error_message = None

        if cp_res.dict:
            e = cp_res.dict['Errors']['Error']
            self.error_code = e['Code']
            self.error_message = e['Message']

        self.message = ""

        if self.error_message:
            self.message = "{0} ({1})".format(self.error_message, self.error_code)
        else:
            self.message = "response status: {0}".format(self.status_code)

        super(SleetyComputingResponseError, self).__init__(self.message)
