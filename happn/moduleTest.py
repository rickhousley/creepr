""" Test happn module """

import happn

token = 'CAAGm0PX4ZCpsBADSUGU22PMoJXAHvntvzVFGxoMzCPYMudcy8MrQwTXW2oK5ZBykbdEJxjpBFCvpGmwbMX98pltPszek3llZBVb4TloVE9dTA1i8rvLJYUYeU0CRVVvUrHLNlp5NTfvPU9l1APHvtHMZCYKT7fSzDxCWs873vdV9lcJoFngxmv0mrQUbxn4FkcZBGEnjZBduiWB88pfezJV92Nid1FibYZD'

user = happn.User(token)
print user.getUserInfo('1346023834')