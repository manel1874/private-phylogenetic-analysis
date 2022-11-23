#!/bin/sh
/bin/sh -ec 'python3 App.py' &
/bin/sh -ec 'cd server && python3 main.py'

