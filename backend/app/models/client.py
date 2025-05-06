class Client:
    def __init__(self, client_id: int, client_name: str, ship_company_id: int,  
                 client_address: str, client_contact_info: str, client_billing_info: str):
        self.client_id = client_id
        self.client_name = client_name
        self.ship_company_id = ship_company_id
        self.client_address = client_address
        self.client_contact_info = client_contact_info
        self.client_billing_info = client_billing_info

    @staticmethod
    async def get_all(connection) -> list['Client']:
        res = await connection.fetch('SELECT * FROM client')
        return [Client(
            client_id=row['client_id'],
            client_name=row['client_name'],
            ship_company_id=row['ship_company_id'],
            client_address=row['client_address'],
            client_contact_info=row['client_contact_info'],
            client_billing_info=row['client_billing_info']
        ) for row in res]

    @staticmethod
    async def get_by_id(connection, client_id: int) -> 'Client':
        res = await connection.fetchrow('SELECT * FROM client WHERE client_id = $1', client_id)
        if res:
            return Client(
                client_id=res['client_id'],
                client_name=res['client_name'],
                ship_company_id=res['ship_company_id'],
                client_address=res['client_address'],
                client_contact_info=res['client_contact_info'],
                client_billing_info=res['client_billing_info']
            )
        return None
    
    @staticmethod
    async def create(connection, client_name: str, ship_company_id: int,  
                 client_address: str, client_contact_info: str, client_billing_info: str) -> 'Client':
        res = await connection.fetchrow(
            """
                INSERT INTO client (client_name, ship_company_id, client_address,
                                    client_contact_info, client_billing_info)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
            """,
            client_name, ship_company_id, client_address, client_contact_info, client_billing_info
        )
        return Client(
            client_id=res['client_id'],
            client_name=res['client_name'],
            ship_company_id=res['ship_company_id'],
            client_address=res['client_address'],
            client_contact_info=res['client_contact_info'],
            client_billing_info=res['client_billing_info']
        )

    @staticmethod
    async def update(connection, client_id: int, client_name: str, ship_company_id: int,  
                 client_address: str, client_contact_info: str, client_billing_info: str) -> 'Client':
        res = await connection.fetchrow(
            """
                UPDATE client 
                SET client_name = $1, ship_company_id = $2, client_address = $3,
                    client_contact_info = $4, client_billing_info = $5
                WHERE client_id = $6
                RETURNING *
            """,
            client_name, ship_company_id, client_address, client_contact_info, 
            client_billing_info, client_id
        )
        if res:
            return Client(
                client_id=res['client_id'],
                client_name=res['client_name'],
                ship_company_id=res['ship_company_id'],
                client_address=res['client_address'],
                client_contact_info=res['client_contact_info'],
                client_billing_info=res['client_billing_info']
            )
        return None

    @staticmethod
    async def delete(connection, client_id: int) -> bool:
        res = await connection.execute(
            'DELETE FROM client WHERE client_id = $1',
            client_id
        )
        return res == 'DELETE 1'