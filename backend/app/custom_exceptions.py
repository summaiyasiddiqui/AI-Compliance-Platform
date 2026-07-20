class CompanyNotFoundException(Exception):
    def __init__(self, message="Company not found"):
        self.message = message
        super().__init__(self.message)


class DuplicateCompanyException(Exception):
    def __init__(self, message="Company already exists"):
        self.message = message
        super().__init__(self.message)