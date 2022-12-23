import json

from synapse.api.errors import SynapseError
from synapse.types import UserID
from twisted.web.resource import Resource
from twisted.web.server import Request
from synapse.module_api import ModuleApi
from typing import List

class ShieldedUser:
    def __init__(self, mxid: str, email: str):
        self.mxid = mxid
        self.email = email

class MayInviteResource(Resource):
    def __init__(self, config):
        super(MayInviteResource, self).__init__()
        self.config = config

    def render_GET(self, request: Request):
        request.setHeader(b"Content-Type", b"application/json")
        return json.dumps({"message": "This identity doesn't accept public invitations. If you need to get in touch, please use " + self.config.shielded_user.email + ". Kind regards."})


class SynapseMayInvite:
    def __init__(self, config: dict, api: ModuleApi):
        self.config = config
        self.api = api

        self.api.register_web_resource(
            path="/_synapse/client/demo/invite",
            resource=MayInviteResource(self.config),
        )
        self.api.register_spam_checker_callbacks(
            user_may_invite=self.user_may_invite,
        )

    @staticmethod
    def parse_config(config):
        shielded_users = []
        for user in config["shielded_users"]:
            shielded_users.append(ShieldedUser(user["mxid"], user["email"]))
        config["shielded_users"] = shielded_users
        return config

    async def user_may_invite(self, sender: str, target: str, shielded_users: List[ShieldedUser]) -> bool:
        # Check if the user trying to invite is from a different homeserver
        if sender != self.api.hs.hostname:
            # Check if the target user is in the list of shielded users
            for shielded_user in shielded_users:
                if target == shielded_user.mxid:
                    return False
        return True
