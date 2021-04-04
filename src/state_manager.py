# TODO - import email/msg handler

class StateManager(object):
    """Class to Manage State in Memory"""

    State = "b6ee60926c0a426addcbb7e087d4274498f35b1c" # Sha1 hash of the empty list, used as default

    @classmethod
    def set_state(cls, newState, handler):
        """Set State in memory and send alerts (email, smsg, etc)"""
        if len(newState) != 40:
            print("LENGTH: ", len(newState))
            raise RuntimeError('State {} is not a hash legnth 40'.format(newState))

        if newState != cls.State:
            # TODO - send email/smsg alert
            print("Detected new state! Sending email.")
            handler()
        else:
            print("State is the same. No email to send.")
        
        cls.State = newState
        

