# Markov Chain Weather Forecast Website

This is a local Streamlit website version of your Markov chain weather project.

## What it includes
- A clean website-style front end
- Sunny, Cloudy, and Rain icons
- A starting weather dropdown
- Forecast length and simulation controls
- A sample simulated forecast
- Daily forecast percentages
- Monte Carlo ending-day percentages
- Long-run and steady-state comparisons
- Charts for presentation

## How to run locally

1. Open Terminal and go into the project folder.
2. Create a virtual environment if you want:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
3. Install the packages:
   - `pip install -r requirements.txt`
4. Run the website:
   - `streamlit run app.py`
5. Your browser should open a local website automatically.

## Good GitHub repo structure

```text
markov_weather_app/
├── app.py
├── weather_logic.py
├── requirements.txt
├── README.md
└── assets/
    ├── sunny.svg
    ├── cloudy.svg
    └── rain.svg
```

## Suggested presentation flow
- Explain what a Markov chain is.
- Show the transition matrix.
- Choose a starting weather.
- Run a 10-day or 14-day forecast.
- Show the prediction percentages.
- Explain how the long-run behavior approaches a steady state.

## Notes
The transition matrix is currently based on the probabilities from your notebook:
- Sunny -> [0.79, 0.13, 0.08]
- Cloudy -> [0.16, 0.63, 0.21]
- Rain -> [0.08, 0.17, 0.75]

If you want, you can later connect this app directly to your original weather dataset and calculate the matrix dynamically.
