import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [input, setInput] = useState('');
  const API = 'http://localhost:5000';

  useEffect(() => {
    fetch_tasks();
  }, []);

  const fetch_tasks = async () => {
    try {
      const res = await axios.get(`${API}/api/tasks`);
      setTasks(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const add = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    try {
      const res = await axios.post(`${API}/api/tasks`, { title: input });
      setTasks([res.data, ...tasks]);
      setInput('');
    } catch (err) {
      console.log(err);
    }
  };

  const toggle = async (id, completed) => {
    try {
      const res = await axios.put(`${API}/api/tasks/${id}`, { completed: !completed });
      setTasks(tasks.map(t => t.id === id ? res.data : t));
    } catch (err) {
      console.log(err);
    }
  };

  const del = async (id) => {
    try {
      await axios.delete(`${API}/api/tasks/${id}`);
      setTasks(tasks.filter(t => t.id !== id));
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="app">
      <h1>📋 Tasks</h1>
      <form onSubmit={add}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Add task..." />
        <button>Add</button>
      </form>
      <div className="tasks">
        {tasks.map(t => (
          <div key={t.id} className={`task ${t.completed ? 'done' : ''}`}>
            <input type="checkbox" checked={t.completed} onChange={() => toggle(t.id, t.completed)} />
            <span>{t.title}</span>
            <button onClick={() => del(t.id)}>×</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;