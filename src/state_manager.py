# TODO - import email/msg handler

class StateManager(object):
    """Class to Manage State in Memory"""

    STATE = 'Not Available'

    @classmethod
    def set_state(cls, state):
        """Set State in memory and send alerts (email, smsg, etc)"""
        if state not in ['Not Available', 'Available']:
            raise RuntimeError('State {} Not an Option'.format(state))

        if state == 'Available' and cls.STATE != 'Available':
            # TODO - send email/smsg alert
            pass
        
        cls.STATE = state
        

