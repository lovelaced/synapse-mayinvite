import json
import logging

from synapse.api.errors import SynapseError
from synapse.types import UserID
from twisted.web.resource import Resource
from twisted.web.server import Request
from synapse.module_api import ModuleApi
from typing import Dict

logger = logging.getLogger(__name__)

class MayInviteResource(Resource):
    def __init__(self, config):
        # Initialize the base Resource class
        super(MayInviteResource, self).__init__()
        # Store the configuration
        self.config = config

    def render_GET(self, request: Request):
        # Set the content type of the response to application/json
        request.setHeader(b"Content-Type", b"application/json")
        # Get the target user's Matrix ID from the request arguments
        target = request.args[b"target"][0].decode("utf-8")
        # Return a message indicating that the user doesn't accept public invitations
        return json.dumps({"message": "This identity doesn't accept public invitations. If you need to get in touch, please use " + self.config["shielded_users"][target] + ". Kind regards."})

class SynapseMayInvite:
    def __init__(self, config: dict, api: ModuleApi):
        # Store the configuration and API object
        self.config = config
        self.api = api

        # Register the user_may_invite callback function to be called for every invite request
        self.api.register_spam_checker_callbacks(
            user_may_invite=self.user_may_invite,
        )
        logger.info("Registered spam checker callbacks")

    @staticmethod
    def parse_config(config: dict) -> dict:
        # Create a new dictionary with the Matrix IDs of the shielded users as keys and their email addresses as values
        shielded_users = {}
        for user, data in config["shielded_users"].items():
            shielded_users[data[0]["mxid"]] = data[1]["email"]
        # Update the config attribute with the new dictionary
        config["shielded_users"] = shielded_users
        config["allowed_homeservers"] = config.get("allowed_homeservers", [])
        return config

    async def user_may_invite(self, sender: str, target: str, room_id: str) -> bool:
        logger.info("Shielded users:")
        logger.info(self.config["shielded_users"])
        logger.info("Allowed homeservers:")
        logger.info(self.config["allowed_homeservers"])
        shielded_mxids = list(self.config["shielded_users"].keys())
        # Check if the user trying to invite is from a different homeserver
        if self.api.is_mine(sender):
            # Allow the invite if the sender is from the same homeserver
            logger.info("Allowed invite from %s to %s to %s", sender, target)
            return True
        # Check if the homeserver of the sender is in the list of allowed homeservers
        sender_homeserver = UserID.from_string(sender).domain
        if sender_homeserver in self.config["allowed_homeservers"]:
            # Allow the invite if the sender is from an allowed homeserver
            logger.info("Allowed invite from %s to %s", sender, target)
            return True
        # Check if the target user is in the list of shielded users
        if target in shielded_mxids:
            logger.info("Blocked invite from %s to shielded user %s", sender, target)
            return False
        logger.info("Allowed invite from %s to %s", sender, target)
        return True

