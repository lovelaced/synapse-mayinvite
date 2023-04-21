import json
import logging

from synapse.api.errors import SynapseError, Codes
from synapse.types import UserID
from synapse.module_api import ModuleApi, NOT_SPAM
from typing import Dict

logger = logging.getLogger(__name__)

class SynapseMayInvite:
    def __init__(self, config: dict, api: ModuleApi):
        # Store the configuration and API object
        self.config = config
        self.api = api

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

    async def user_may_invite(self, sender: str, target: str, room_id: str):
        logger.info("Shielded users:")
        logger.info(self.config["shielded_users"])
        logger.info("Allowed homeservers:")
        logger.info(self.config["allowed_homeservers"])
        shielded_mxids = list(self.config["shielded_users"].keys())
        # Check if the user trying to invite is from a different homeserver
        if self.api.is_mine(sender):
            # Allow the invite if the sender is from the same homeserver
            logger.info(f"Allowed invite from {sender} to {target}")
            return NOT_SPAM
        # Check if the homeserver of the sender is in the list of allowed homeservers
        sender_homeserver = UserID.from_string(sender).domain
        if sender_homeserver in self.config["allowed_homeservers"]:
            # Allow the invite if the sender is from an allowed homeserver
            logger.info(f"Allowed invite from {sender} to {target}")
            return NOT_SPAM
        # Check if the target user is in the list of shielded users
        if target in shielded_mxids:
            logger.info(f"Blocked invite from {sender} to shielded user {target}")
            return Codes.FORBIDDEN
        logger.info(f"Allowed invite from {sender} to {target}")
        return NOT_SPAM

