class Item:
    def __init__(self, item_id: int, sku: str, name: str, item_metadata: list):
        self.item_id = item_id
        self.sku = sku
        self.name = name
        self.item_metadata = item_metadata

    @staticmethod
    async def get_all(connection) -> list['Item']:
        res = await connection.fetch('SELECT * FROM item')
        return [Item(
            item_id=row['item_id'],
            sku=row['sku'],
            name=row['name'],
            item_metadata=row['item_metadata']
        ) for row in res]

    @staticmethod
    async def get_by_id(connection, item_id: int) -> 'Item':
        result = await connection.fetchrow('SELECT * FROM item WHERE item_id = $1', item_id)
        if result:
            return Item(
                item_id=result['item_id'],
                sku=result['sku'],
                name=result['name'],
                item_metadata=result['item_metadata']
            )
        return None
    
    @staticmethod
    async def create(connection, sku: str, name: str, item_metadata: list) -> 'Item':
        result = await connection.fetchrow(
            """
            INSERT INTO item (sku, name, item_metadata) 
            VALUES ($1, $2, $3) RETURNING *
            """,
            sku, name, item_metadata
        )
        return Item(
            item_id=result['item_id'],
            sku=result['sku'],
            name=result['name'],
            item_metadata=result['item_metadata']
        )

    @staticmethod
    async def update(connection, item_id: int, sku: str, name: str, item_metadata: list) -> 'Item':
        result = await connection.fetchrow(
            """
            UPDATE item 
            SET sku = $1, name = $2, item_metadata = $3
            WHERE item_id = $4
            RETURNING *
            """,
            sku, name, item_metadata, item_id
        )
        if result:
            return Item(
                item_id=result['item_id'],
                sku=result['sku'],
                name=result['name'],
                item_metadata=result['item_metadata']
            )
        return None

    @staticmethod
    async def delete(connection, item_id: int) -> bool:
        res = await connection.execute(
            'DELETE FROM item WHERE item_id = $1',
            item_id
        )
        return res == 'DELETE 1'