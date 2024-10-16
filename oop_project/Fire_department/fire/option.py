"""manages menu options including reports
"""

__author__ = 'Chieh-Ching Chen'

# to help create safe filenames
import re
# for timestamps
from datetime import datetime
import os
import json
from . import vehicle as v
from . import user as u

print('dev: loading module ' + __name__)

class Option:

    def __init__(self, **kwargs):
        self._message = ""
        self._action = lambda: None
        for i in kwargs:
            setattr(self, i, kwargs[i])

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action

    def act(self):
        return self._action()
### class Option ###

class SafeOption(Option):

    def __init__(self, **kwargs):
        self._user = None
        super().__init__(**kwargs)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        self._description = description
    
    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action

    def act(self):
        time = datetime.now().replace(second=0, microsecond=0)
        message = super().act()
        with open('fire_department_log.txt', 'a') as log_file:
            log_file.write(f"{time.ctime()}, User: {self._user}, "
                           f"Option: {self._description}\n")
        return message
### class SafeOption(Option) ###


class Report(SafeOption):

    def __init__(self, **kwargs):
        self._report_type = ""
        super().__init__(**kwargs)

    @property
    def report_type(self):
        return self._report_type

    @report_type.setter
    def report_type(self, report_type):
        self._report_type = report_type

    def act(self):
        super().act()
        report = input(f"{self.user.name}, please enter your "
                       f"{self.report_type} here:")
        # removing leading and trailing white space
        report = report.strip()
        message = ""
        if len(report) > 0:
            time = datetime.now().replace(second=0, microsecond=0)
            timestamp = time.isoformat(timespec='minutes')
            name_stub = f"{self.report_type}_{timestamp}_{self.user.name}.txt"
            file_name = re.sub('[ :/\\\]', '_', name_stub)
            file = None
            try:
                file = open(file_name, 'w')
                file.write(f"{self.report_type} written by user "
                           f"{self.user.name} on {time.ctime()}\n\n")
                file.write(report)
                message = (f"{self.user.name}, your {self.report_type} has been filed as "
                           f"{file_name}")
            except:
                # TODO: handle this error. THIS IS NOT A TASK!!!!!
                #  Just normal comment.
                message = (f"ERROR, {self.user.name}, your report could not "
                           f"be filed.")
            finally:
                if file:
                    file.close()
        return message
### class Report(SafeOption) ###

class RegisteredReport(Report):

    def act(self):
        if self._user.is_registered():
            return super().act()
        else:
            return (f"{self._user.name} is not authorized to file "
                    f"{self._report_type}.")

### class RegisterdReport(Report) ###

