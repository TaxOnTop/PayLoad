import google.generativeai as genai
# Set Gemini API key and model
GEMINI_API_KEY = 'AIzaSyAj64KkRaUndUuy7zRuK5FgSMRiQtQvJhw'
GEMINI_MODEL = 'gemini-2.5-flash'

# Gemini AI wrapper
class GeminiAI:
    def __init__(self, api_key, model_name):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    def ask(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text

ai_model = GeminiAI(GEMINI_API_KEY, GEMINI_MODEL)
from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from physics_modules import orbital_mechanics

import sys
import logging

app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            r1 = float(request.form['r1'])
            r2 = float(request.form['r2'])
            mass = float(request.form['mass'])
            Isp = float(request.form.get('Isp', 300))
            thrust = float(request.form.get('thrust', 10000))
            # Input validation
            if r1 <= 0 or r2 <= 0 or mass <= 0 or Isp <= 0 or thrust <= 0:
                raise ValueError("All input values must be positive and nonzero.")
            delta_v, dv1, dv2 = orbital_mechanics.hohmann_delta_v(r1, r2)
            fuel_mass, mf = orbital_mechanics.tsiolkovsky_fuel_mass(mass, delta_v, Isp)
            burn = orbital_mechanics.burn_time(fuel_mass, Isp, thrust)
            # Step-by-step breakdown
            steps = [
                f"1. Calculate velocities for initial and target orbits:",
                f"   v1 = sqrt(mu / r1) = sqrt(3.986e14 / {r1}) = {round((3.986e14 / r1) ** 0.5, 2)} m/s",
                f"   v2 = sqrt(mu / r2) = sqrt(3.986e14 / {r2}) = {round((3.986e14 / r2) ** 0.5, 2)} m/s",
                f"2. Calculate transfer orbit velocities:",
                f"   a_transfer = (r1 + r2) / 2 = {(r1 + r2) / 2} m",
                f"   v_transfer1 = sqrt(mu * (2/r1 - 1/a_transfer))",
                f"   v_transfer2 = sqrt(mu * (2/r2 - 1/a_transfer))",
                f"3. Delta-v for burns:",
                f"   delta_v1 = v_transfer1 - v1",
                f"   delta_v2 = v2 - v_transfer2",
                f"   Total delta-v = |delta_v1| + |delta_v2| = {round(delta_v, 2)} m/s",
                f"4. Tsiolkovsky fuel mass:",
                f"   fuel_mass = m0 - m0 / exp(delta_v / (Isp * g0)) = {round(fuel_mass, 2)} kg",
                f"5. Burn time:",
                f"   burn_time = fuel_mass / (thrust / (Isp * g0)) = {round(burn, 2)} s"
            ]

            # Use Gemini AI to generate an explanation
            ai_prompt = f"""
            A spacecraft with mass {mass} kg is transferring from a circular orbit of radius {r1} m to {r2} m. The required delta-v for a Hohmann transfer, the fuel mass needed (Isp={Isp}s), and the total burn time (thrust={thrust}N) have been calculated. In 3-4 sentences, give a brief, clear, and friendly explanation of what these results mean for a general audience. Do not use JSON, LaTeX, or equations. Avoid technical jargon and keep it concise.
            """
            ai_explanation = ai_model.ask(ai_prompt)

            result = {
                'delta_v': delta_v,
                'fuel_mass': fuel_mass,
                'burn_time': burn,
                'r1': r1,
                'r2': r2,
                'mass': mass,
                'Isp': Isp,
                'thrust': thrust,
                'steps': steps,
                'ai': ai_explanation
            }
        except Exception as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

# Add this block to start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
