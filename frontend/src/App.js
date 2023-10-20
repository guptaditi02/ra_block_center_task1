import React, { useState } from 'react';
import styles from './App.module.css';

const backendapi = 'http://127.0.0.1:5000/api/send';

function App() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    gender: '',
    dob: '',
    email: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(backendapi, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    alert(data.message);
  };

  return (
    
    <div className={styles.appContainer}>
        <div className={styles.formContainer}>
            <form onSubmit={handleSubmit}>
                <input className={styles.inputField} name="firstName" placeholder="First Name" onChange={handleChange} />
                <input className={styles.inputField} name="lastName" placeholder="Last Name" onChange={handleChange} />
                <div className={styles.radioGroup}>
                    <label className={styles.radioLabel}>
                        <input type="radio" value="Male" name="gender" onChange={handleChange} /> Male
                    </label>
                    <label className={styles.radioLabel}>
                        <input type="radio" value="Female" name="gender" onChange={handleChange} /> Female
                    </label>
                </div>
                <input className={styles.inputField} type="date" name="dob" onChange={handleChange} />
                <input className={styles.inputField} type="email" name="email" placeholder="Email" onChange={handleChange} />
                <button className={styles.submitButton} type="submit">Submit</button>
            </form>
        </div>
    </div>
);
}

export default App;