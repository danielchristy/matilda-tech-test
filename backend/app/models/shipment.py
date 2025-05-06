class Shipment:
    def __init__(self, shipment_id: int, ship_order_id: int, shipment_state: str, 
                 created_at: str, updated_at: str):
        self.shipment_id = shipment_id
        self.ship_order_id = ship_order_id
        self.shipment_state = shipment_state
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    async def get_all(connection) -> list['Shipment']:
        res = await connection.fetch('SELECT * FROM shipment')
        return [Shipment(
            shipment_id=row['shipment_id'],
            ship_order_id=row['ship_order_id'],
            shipment_state=row['shipment_state'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        ) for row in res]

    @staticmethod
    async def get_by_id(connection, shipment_id: int) -> 'Shipment':
        res = await connection.fetchrow('SELECT * FROM shipment WHERE shipment_id = $1', shipment_id)
        if res:
            return Shipment(
                shipment_id=res['shipment_id'],
                ship_order_id=res['ship_order_id'],
                shipment_state=res['shipment_state'],
                created_at=res['created_at'],
                updated_at=res['updated_at']
            )
        return None

    @staticmethod
    async def create(connection, ship_order_id: int, shipment_state: str) -> 'Shipment':
        res = await connection.fetchrow(
            """
            INSERT INTO shipment (ship_order_id, shipment_state) 
            VALUES ($1, $2) RETURNING *
            """,
            ship_order_id, shipment_state
        )
        return Shipment(
            shipment_id=res['shipment_id'],
            ship_order_id=res['ship_order_id'],
            shipment_state=res['shipment_state'],
            created_at=res['created_at'],
            updated_at=res['updated_at']
        )

    @staticmethod
    async def update(connection, shipment_id: int, ship_order_id: int, shipment_state: str) -> 'Shipment':
        res = await connection.fetchrow(
            """
            UPDATE shipment 
            SET ship_order_id = $1, shipment_state = $2
            WHERE shipment_id = $3
            RETURNING *
            """,
            ship_order_id, shipment_state, shipment_id
        )
        if res:
            return Shipment(
                shipment_id=res['shipment_id'],
                ship_order_id=res['ship_order_id'],
                shipment_state=res['shipment_state'],
                created_at=res['created_at'],
                updated_at=res['updated_at']
            )
        return None

    @staticmethod
    async def delete(connection, shipment_id: int) -> bool:
        res = await connection.execute(
            'DELETE FROM shipment WHERE shipment_id = $1',
            shipment_id
        )
        return res == 'DELETE 1'
