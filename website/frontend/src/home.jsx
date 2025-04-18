import React, { useState } from 'react';
import './home.css';

const districtMapping = {
    "Buxar": 7, "Patna": 26, "Munger": 21, "Bhagalpur": 5,
    "Siwan": 33, "Saran": 31, "PashchimChamparan": 25,
    "Muzzafarpur": 22, "Motihari": 20, "Samastipur": 30,
    "Darbhanga": 8, "Sitamarhi": 32, "Supaul": 34,
    "Khagaria": 15, "Katihar": 14
};

const riverMapping = {
    "Ganga": 7, "Ghaghra": 6, "Gandak": 2,
    "Burhi Gandak": 1, "Bagmati": 0, "Kosi": 4
};

const districtRiverData = [
    { river: "Ganga", district: "Buxar" }, { river: "Ganga", district: "Patna" },
    { river: "Ganga", district: "Munger" }, { river: "Ganga", district: "Bhagalpur" },
    { river: "Ghaghra", district: "Siwan" }, { river: "Ghaghra", district: "Saran" },
    { river: "Gandak", district: "PashchimChamparan" }, { river: "Gandak", district: "Muzzafarpur" },
    { river: "Burhi Gandak", district: "Motihari" }, { river: "Burhi Gandak", district: "Samastipur" },
    { river: "Bagmati", district: "Darbhanga" }, { river: "Bagmati", district: "Sitamarhi" },
    { river: "Kosi", district: "Supaul" }, { river: "Kosi", district: "Khagaria" },
    { river: "Kosi", district: "Katihar" }
];

function Home() {
    const [district, setDistrict] = useState("");
    const [river, setRiver] = useState("");
    const [rainfall, setRainfall] = useState("");
    const [riverLevel, setRiverLevel] = useState("");
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    const districts = [...new Set(districtRiverData.map(d => d.district))];
    const filteredRivers = districtRiverData
        .filter(d => d.district === district)
        .map(d => d.river);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError("");

        try {
            const payload = {
                "District": districtMapping[district],
                "Rainfall (mm)": parseFloat(rainfall),
                "River": riverMapping[river],
                "River Level": parseFloat(riverLevel)
            };

            const response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || "Failed to get prediction");
            }

            const resultData = await response.json();
            setResult(resultData);
        } catch (err) {
            setError(err.message || "Failed to connect to the prediction service");
        } finally {
            setIsLoading(false);
        }
    };

    const getRiskLevel = (value) => {
        if (value === 0) return "Low";
        if (value === 1) return "Medium";
        if (value === 2) return "High";
        return "Unknown";
    };

    const getRiskColor = (value) => {
        if (value === 0) return "#4ade80"; // Green for Low
        if (value === 1) return "#f59e0b"; // Orange for Medium
        if (value === 2) return "#ef4444"; // Red for High
        return "#9ca3af"; // Gray for Unknown
    };

    return (
        <div className="container">
            <header>
                <h1>Bihar Flood Prediction System</h1>
                <p>Enter parameters to predict flood risk level</p>
            </header>

            <div className="form-container">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>District</label>
                        <select
                            value={district}
                            onChange={(e) => {
                                setDistrict(e.target.value);
                                setRiver("");
                            }}
                            required
                        >
                            <option value="">Select District</option>
                            {districts.map((d, i) => (
                                <option key={i} value={d}>{d}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>River</label>
                        <select
                            value={river}
                            onChange={(e) => setRiver(e.target.value)}
                            required
                            disabled={!district}
                        >
                            <option value="">Select River</option>
                            {filteredRivers.map((r, i) => (
                                <option key={i} value={r}>{r}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Rainfall (mm)</label>
                            <input
                                type="number"
                                value={rainfall}
                                onChange={(e) => setRainfall(e.target.value)}
                                min="0"
                                step="0.1"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>River Level (m)</label>
                            <input
                                type="number"
                                value={riverLevel}
                                onChange={(e) => setRiverLevel(e.target.value)}
                                min="0"
                                step="0.1"
                                required
                            />
                        </div>
                    </div>

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? "Predicting..." : "Predict Flood Risk"}
                    </button>
                </form>
            </div>

            {error && (
                <div className="error-message">
                    <p>Error: {error}</p>
                </div>
            )}

            {result && (
                <div className="results-container">
                    <div className="risk-indicator" style={{ backgroundColor: getRiskColor(result.Flood_Risk) }}>
                        <h2>Flood Risk: {getRiskLevel(result.Flood_Risk)}</h2>
                        <p>(Code: {result.Flood_Risk})</p>
                    </div>

                    <div className="impact-stats">
                        <div className="stat-card">
                            <h3>Area Affected</h3>
                            <p>{result.Area_affected} million ha</p>
                        </div>
                        <div className="stat-card">
                            <h3>Population Affected</h3>
                            <p>{result.Population_affected} million</p>
                        </div>
                        <div className="stat-card">
                            <h3>Crop Damage</h3>
                            <p>{result.crop_damage} million ha</p>
                        </div>
                        <div className="stat-card">
                            <h3>House Damage</h3>
                            <p>{result.houses_damage} thousand</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Home;