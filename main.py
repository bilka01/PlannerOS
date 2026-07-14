# from app.hotkeys.listener import start_listener


# if __name__ == "__main__":
#     start_listener()'

import sys

from app.core.pipeline import PlannerPipeline
from app.hotkeys.listener import start_listener

if __name__ == "__main__":
    if "--once" in sys.argv:
        PlannerPipeline().run()
    else:
        start_listener()