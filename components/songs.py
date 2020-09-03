import subprocess
from components.hasura_controller import HasuraClient
import hashlib
import json
import uuid
import sys

sys.path.append(".")

graphQL_client = HasuraClient().graphql_client