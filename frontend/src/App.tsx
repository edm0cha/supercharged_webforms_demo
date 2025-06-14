import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [formData, setFormData] = useState({
    destination: '',
    startDate: '',
    endDate: '',
    tickets: 1,
    adventurousness: 5,
  })
  const [itinerary, setItinerary] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/generate-itinerary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      const data = await response.json()
      setItinerary(data.result)
    } catch (err) {
      setItinerary('Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>AI Travel Planner</h1>
      <input name="destination" placeholder="Destination" onChange={handleChange} />
      <input name="startDate" type="date" onChange={handleChange} />
      <input name="endDate" type="date" onChange={handleChange} />
      <input name="tickets" type="number" min="1" onChange={handleChange} />
      <label>Adventurousness: {formData.adventurousness}</label>
      <input name="adventurousness" type="range" min="1" max="10" value={formData.adventurousness} onChange={handleChange}></input>
      <button onClick={handleSubmit} disabled={loading}>{loading ? 'Generating...' : 'Generate Itinerary'}</button>
      <pre>{itinerary}</pre>
    </div>
  )
}

export default App
