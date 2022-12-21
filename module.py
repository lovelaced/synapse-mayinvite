import json

from synapse.api.errors import SynapseError
from synapse.types import UserID
from twisted.web.resource import Resource
from twisted.web.server import Request

class MayInviteResource(Resource):
    def __init__(self, config, spam_checker):
        super(MayInviteResource, self).__init__()
        self.config = config

    def render_GET(self, request: Request):
        request.setHeader(b"Content-Type", b"application/json")
        return json.dumps({"message": "This identity doesn't accept public invitations. If you need to get in touch, please use ", config.shielded_user.email, ". Kind regards."})


class MayInviteModule:
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
        return config

    async def user_may_invite(self, sender: str) -> bool:
        # Check if the user trying to invite is from a different homeserver
        if sender != self.api.hs.hostname:
            if target == shielded_user.mxid:
                return False
        return True

