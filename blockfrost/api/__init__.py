import os
import json
from enum import Enum

from ..config import ApiUrls, DEFAULT_API_VERSION
from ..utils import object_request_wrapper
from .health import health, clock
from ..cardano import accounts, \
    account_rewards, \
    account_history, \
    account_delegations, \
    account_registrations, \
    account_withdrawals, \
    account_mirs, \
    account_addresses, \
    account_addresses_assets

# import health
# import cardano
import requests

#
# class ApiUrls(Enum):
#     mainnet = 'https://cardano-mainnet.blockfrost.io/api'
#     testnet = 'https://cardano-testnet.blockfrost.io/api'
#     ipfs = 'https://ipfs.blockfrost.io/api'
#
#
# DEFAULT_API_VERSION = 'v0'
# DEFAULT_ORDER = 'asc'
# DEFAULT_PAGINATION_PAGE_COUNT = 1
# DEFAULT_PAGINATION_PAGE_ITEMS_COUNT = 100
#
# ADDRESS_GAP_LIMIT = 20


class Api:

    def __init__(
            self,
            project_id: str = None,
            base_url: str = None,
            api_version: str = None,
    ):
        self.project_id = project_id if project_id else os.environ.get('BLOCKFROST_PROJECT_ID')
        self.base_url = base_url if base_url else os.environ.get('BLOCKFROST_API_URL', default=ApiUrls.mainnet.value)
        self.api_version = api_version if api_version else os.environ.get('BLOCKFROST_API_VERSION',
                                                                          default=DEFAULT_API_VERSION)

    @property
    def url(self):
        return f"{self.base_url}/{self.api_version}"

    @property
    def authentication_header(self):
        return {
            'project_id': self.project_id
        }

    @staticmethod
    def query_parameters(kwargs: dict):
        """
        count
        integer <= 100
        Default: 100
        The number of results displayed on one page.

        page
        integer
        Default: 1
        The page number for listing the results.

        order
        string
        Default: "asc"
        Enum: "asc" "desc"
        The ordering of items from the point of view of the blockchain, not the page listing itself. By default, we return oldest first, newest last.
        """
        return {
            "count": kwargs.get('count', None),
            "page": kwargs.get('page', None),
            "order": kwargs.get('order', None),
        }


class BlockFrostApi(Api):
    @object_request_wrapper
    def root(self) -> json:
        """https://cardano-mainnet.blockfrost.io/api/v0/"""
        return requests.get(
            url=f"{self.url}/",
            headers=self.authentication_header
        )

    health = health
    clock = clock
    accounts = accounts
    account_rewards = account_rewards
    account_history = account_history
    account_delegations = account_delegations
    account_registrations = account_registrations
    account_withdrawals = account_withdrawals
    account_mirs = account_mirs
    account_addresses = account_addresses
    account_addresses_assets = account_addresses_assets