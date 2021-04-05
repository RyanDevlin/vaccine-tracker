# TODO - import email/msg handler

class StateManager(object):
    """Class to Manage State in Memory"""

    State = []

    @classmethod
    def set_state(cls, newState, handler):
        """Set State in memory and send alerts (email, smsg, etc)"""

        if any([state for state in newState if state not in cls.State]):
            # TODO - send email/smsg alert
            print("Detected new state! Sending email.")
            handler()
        else:
            print("State is the same. No email to send.")
        
        cls.State = newState
        

