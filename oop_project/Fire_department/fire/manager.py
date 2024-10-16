"""resources management for the fires department
"""

__author__ = 'Chieh-Ching Chen'

# Importing necessary modules
import importlib
from . import user
from . import option
from . import vehicle_menu as vm

# Reloading modules to ensure latest changes are loaded
importlib.reload(user)
importlib.reload(option)

print('dev: loading module ' + __name__)

def main():
    # Initialize the main user and vehicle manager
    main_user = user.SecureUser()
    vehicle_manager = vm.VehicleManager()
    active = True

    def quit():
        """Quit the application."""
        print('Good bye!')
        nonlocal active
        active = False

    message = ""

    while active:

        options = []
        options.append(option.Option(description= "exit",
                                     action= quit))
        options.append(option.Option(description= "register",
                                     action= main_user.register))
        options.append(option.Report(description= "file a complaint",
                                    report_type= "Complaint",
                                    user= main_user))
        options.append(option.Report(description= "file a memo",
                                    report_type= "Memo",
                                    user= main_user))
        # Check if the user is authorized
        if main_user.is_authorized():
            options.append(option.Option(description= "logout",
                                         action= main_user.logout,
                                         user=main_user))
            options.append(option.RegisteredReport(description= "file an action report"
                                                " (registered users only)",
                                                report_type= "ActionReport",
                                                user= main_user))
            # Add the Vehicle Manager option
            options.append(option.SafeOption(description="Vehicle Manager",
                                            action=vehicle_manager.run,
                                            user= main_user))
        else:
            options.append(option.SafeOption(description="login",
                                             action=main_user.login,
                                             user=main_user))

        menu = ""
        for i in range(len(options)):
            menu += str(i) + ': ' + options[i].description + '\n'

        while True:
            choice = input(f"{message}\n\n{main_user.name}, "
                           f"please choose:\n{menu}").strip()
            if choice.isdigit():
                index = int(choice)
                if 0 <= index < len(options):
                    message = options[index].act()
                    break
            # if not, display an error message
            message = f"{choice} is not an option."
### def main() ###

