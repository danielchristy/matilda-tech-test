class ShipOrder:
    def __init__(self, ship_order_id: int, client_id: int, ship_order_state: str,
                 ship_order_date: str, expected_shipments: int, completed_shipments: int,
                 created_at: str, updated_at: str):
        self.ship_order_id = ship_order_id
        self.client_id = client_id
        self.ship_order_state = ship_order_state
        self.ship_order_date = ship_order_date
        self.expected_shipments = expected_shipments
        self.completed_shipments = completed_shipments
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    async def get_all(connection) -> list['ShipOrder']:
        res = await connection.fetch('SELECT * FROM ship_order')
        return [ShipOrder(
            ship_order_id=row['ship_order_id'],
            client_id=row['client_id'],
            ship_order_state=row['ship_order_state'],
            ship_order_date=row['ship_order_date'],
            expected_shipments=row['expected_shipments'],
            completed_shipments=row['completed_shipments'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        ) for row in res]

    @staticmethod
    async def get_by_id(connection, ship_order_id: int) -> 'ShipOrder':
        res = await connection.fetchrow('SELECT * FROM ship_order WHERE ship_order_id = $1', ship_order_id)
        if res:
            return ShipOrder(
                ship_order_id=res['ship_order_id'],
                client_id=res['client_id'],
                ship_order_state=res['ship_order_state'],
                ship_order_date=res['ship_order_date'],
                expected_shipments=res['expected_shipments'],
                completed_shipments=res['completed_shipments'],
                created_at=res['created_at'],
                updated_at=res['updated_at']
            )
        return None 
    
    @staticmethod
    async def create(connection, client_id: int, ship_order_state: str, ship_order_date: str, 
                     expected_shipments: int, completed_shipments: int) -> 'ShipOrder':
        res = await connection.fetchrow(
            """
            INSERT INTO ship_order (client_id, ship_order_state, ship_order_date, 
                                    expected_shipments, completed_shipments)
            VALUES ($1, $2, $3, $4, $5) 
            RETURNING *
            """,
            client_id, ship_order_state, ship_order_date, expected_shipments, completed_shipments
        )
        return ShipOrder(
            ship_order_id=res['ship_order_id'],
            client_id=res['client_id'],
            ship_order_state=res['ship_order_state'],
            ship_order_date=res['ship_order_date'],
            expected_shipments=res['expected_shipments'],
            completed_shipments=res['completed_shipments'],
            created_at=res['created_at'],
            updated_at=res['updated_at']
        )

    @staticmethod
    async def update(connection, ship_order_id: int, client_id: int, ship_order_state: str, 
                    ship_order_date: str, expected_shipments: int, completed_shipments: int) -> 'ShipOrder':
        res = await connection.fetchrow(
            """
            UPDATE ship_order 
            SET client_id = $1, ship_order_state = $2, ship_order_date = $3,
                expected_shipments = $4, completed_shipments = $5
            WHERE ship_order_id = $6
            RETURNING *
            """,
            client_id, ship_order_state, ship_order_date, expected_shipments, 
            completed_shipments, ship_order_id
        )
        if res:
            return ShipOrder(
                ship_order_id=res['ship_order_id'],
                client_id=res['client_id'],
                ship_order_state=res['ship_order_state'],
                ship_order_date=res['ship_order_date'],
                expected_shipments=res['expected_shipments'],
                completed_shipments=res['completed_shipments'],
                created_at=res['created_at'],
                updated_at=res['updated_at']
            )
        return None

    @staticmethod
    async def delete(connection, ship_order_id: int) -> bool:
        res = await connection.execute(
            'DELETE FROM ship_order WHERE ship_order_id = $1',
            ship_order_id
        )
        return res == 'DELETE 1'