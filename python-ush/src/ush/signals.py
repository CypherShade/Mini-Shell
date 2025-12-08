import signal
import sys
import os

def sigint_handler(signum, frame):
    print("\nCaught SIGINT (Ctrl+C), exiting...")
    sys.exit(0)

def setup_signal_handlers():
    signal.signal(signal.SIGINT, sigint_handler)
    # Only ignore SIGTSTP on Unix-like systems (not available on Windows)
    if hasattr(signal, 'SIGTSTP'):
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)

setup_signal_handlers()