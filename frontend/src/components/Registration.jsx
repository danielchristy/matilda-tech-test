import React, { useState } from 'react';

const Registration = ({ onLogin, onLogout }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8080/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include',
            });

            if (response.ok) {
                const data = await response.json();
                setMessage(`Registration successful! Welcome, ${data.username}`);
            } else {
                const errorData = await response.json();
                setMessage(`Error: ${errorData.text}`);
            }
        } catch (error) {
            setMessage('Error: Unable to connect to the server.');
        }
    };

    // placing here only for test purposes
    const handleLogin = async (e) => {
        e.preventDefault();
        await onLogin(username, password);
    };

    return (
        <div>
            <h2>Registration</h2>
            <form onSubmit={handleRegister}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Register</button>
            </form>
            <form onSubmit={handleLogin}>
                <button type="submit">Login</button>
            </form>
            <button onClick={onLogout}>Logout</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Registration;
