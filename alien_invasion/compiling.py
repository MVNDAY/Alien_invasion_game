import sys
sys.argv.append("build")
import cx_Freeze
from cx_Freeze import *

setup(
    name = "AlienInvasion",
    options = {"build_exe":{"packages":['pygame']}},
    executables=[
        Executable(
            "alien_invasion.py",
        )
    ]
)