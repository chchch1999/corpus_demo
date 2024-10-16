import os
import importlib
from fire import manager

# importlib.reload() makes sure that you always run the latest version of your code
importlib.reload(manager)
manager.main()
