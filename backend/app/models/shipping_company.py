class ShippingCompany:
    def __init__(self, ship_company_id: int, name: str):
        self.ship_company_id = ship_company_id
        self.name = name
    
    @staticmethod
    async def get_all(connection) -> list['ShippingCompany']:
        res = await connection.fetch('SELECT * FROM shipping_company')
        return [ShippingCompany(
            ship_company_id=row['ship_company_id'],
            name=row['name']
        ) for row in res]
    
    @staticmethod
    async def get_by_id(connection, ship_company_id: int) -> 'ShippingCompany':
        res = await connection.fetchrow('SELECT * FROM shipping_company WHERE ship_company_id = $1', ship_company_id)
        if res:
            return ShippingCompany(
                ship_company_id=res['ship_company_id'],
                name=res['name']
            )
        return None
    
    @staticmethod
    async def create(connection, name: str) -> 'ShippingCompany':
        res = await connection.fetchrow(
            'INSERT INTO shipping_company (name) VALUES ($1) RETURNING *',
            name
        )
        return ShippingCompany(
            ship_company_id=res['ship_company_id'],
            name=res['name']
        )
    
    @staticmethod
    async def update(connection, ship_company_id: int, name: str) -> 'ShippingCompany':
        res = await connection.fetchrow(
            'UPDATE shipping_company SET name = $1 WHERE ship_company_id = $2 RETURNING *',
            name, ship_company_id
        )
        if res:
            return ShippingCompany(
                ship_company_id=res['ship_company_id'],
                name=res['name']
            )
        return None
    
    @staticmethod
    async def delete(connection, ship_company_id: int) -> bool:
        res = await connection.execute(
            'DELETE FROM shipping_company WHERE ship_company_id = $1',
            ship_company_id
        )
        return res == 'DELETE 1'

