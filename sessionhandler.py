import blpapi
from blpapi import SessionOptions, Session

def start_session():
    session_options = SessionOptions()
    session_options.setServerHost("localhost")
    session_options.setServerPort(8194)

    session = Session(session_options)

    if not session.start():
        print("Failed to start session")
        return False

    if not session.openService("//blp/mktdata"):
        print("Failed to open //blp/mktdata")
        return False
    
    return session