from graphqlclient import GraphQLClient
import os


class HasuraClient:
    def __init__(self):
        self.HASURA_GRAPHQL_URL = os.environ['HASURA_GRAPHQL_URL']
        self.HASURA_GRAPHQL_ADMIN_SECRET = os.environ['HASURA_GRAPHQL_ADMIN_SECRET']

        self.graphql_client = GraphQLClient(self.HASURA_GRAPHQL_URL)
        self.graphql_client.inject_token(
            self.HASURA_GRAPHQL_ADMIN_SECRET, 'x-hasura-admin-secret'
        )