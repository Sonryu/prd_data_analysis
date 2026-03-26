# Rocket Motor Static Test Data Analysis

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![NumPy](https://img.shields.io/badge/NumPy-Data%20Science-013243.svg?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)

An application developed for **@PotiguarRocketDesign** to analyze data from static rocket motor tests. This tool processes telemetry and sensor data to calculate critical performance parameters.

## 🚀 Features


Based on the current implementation in `formulas.py`, the app performs the following calculations:

- **Time Conversion:** Automatically converts sensor timestamps from milliseconds (ms) to seconds (s).
- **Burn Time:** Calculates the total motor burn duration.
- **Maximum Thrust:** Identifies the peak thrust (Empuxo Máximo) recorded during the test.
- **Average Thrust:** Computes the mean thrust over the burn duration.
- **Data Integration:** (In Progress) Integration with Streamlit for interactive data visualization.

## 🛠️ Technologies Used

- **Python:** Core programming language.
- **Streamlit:** Used for creating the interactive web interface.
- **NumPy:** Utilized for high-performance numerical calculations and array processing.

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd prd_data_analisys
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   *(Note: Ensure you have streamlit and numpy installed)*
   ```bash
   pip install streamlit numpy
   ```

## 🖥️ Usage

To run the application locally, use the following command:

```bash
streamlit run app.py
```

## 📄 License

This project is part of the development for @PotiguarRocketDesign. Refer to the organization for licensing details.
