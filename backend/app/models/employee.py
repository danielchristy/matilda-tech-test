import bcrypt

class Employee:
    def __init__(self, employee_id: int, username: str, password_hash: str):
        self.employee_id = employee_id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    async def get_all(connection) -> list['Employee']:
        res = await connection.fetch('SELECT * from employee')
        return [Employee(
            employee_id=res['employee_id'],
            username=res['username'],
            password=res['password']
        )]

    @staticmethod
    async def get_by_username(connection, username: str):
        row = await connection.fetchrow("SELECT * FROM employee WHERE username = $1", username)
        if row:
            return Employee(row['employee_id'], row['username'], row['password_hash'])
        return None

    @staticmethod
    async def create(connection, username: str, password: str):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        row = await connection.fetchrow(
            "INSERT INTO employee (username, password_hash) VALUES ($1, $2) RETURNING *",
            username, hashed
        )
        return Employee(row['employee_id'], row['username'], row['password_hash'])

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
