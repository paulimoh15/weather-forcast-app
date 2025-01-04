import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

API_KEY = "e42c3f486eb2e2e95a8de8fe198df4a8"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    try:
        # Fetch current weather
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract weather data
        weather_description = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        visibility = data["visibility"] / 1000  # Convert to kilometers
        sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')

        # Update the labels
        weather_label.config(text=f"{temperature}°C\nFeels Like {feels_like}° | {weather_description}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        pressure_label.config(text=f"Pressure: {pressure} mBar")
        description_label.config(text=f"Description: {weather_description}")
        visibility_label.config(text=f"Visibility: {visibility} km")
        sunrise_label.config(text=f"Sunrise: {sunrise}")
        sunset_label.config(text=f"Sunset: {sunset}")

        current_weather_label.config(text=f"Current Weather: {city.capitalize()}")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            messagebox.showerror("Error", f"City '{city}' not found.")
        else:
            messagebox.showerror("Error", f"HTTP error: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")

def reset():
    city_entry.delete(0, tk.END)
    current_weather_label.config(text="Current Weather:")
    weather_label.config(text="")
    humidity_label.config(text="")
    pressure_label.config(text="")
    description_label.config(text="")
    visibility_label.config(text="")
    sunrise_label.config(text="")
    sunset_label.config(text="")

# Tkinter GUI
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("400x400")
root.resizable(False, False)

# Title Label
tk.Label(root, text="Weather App", font=("Helvetica", 18, "bold")).pack(pady=10)

# City Entry
tk.Label(root, text="Enter City Name:").pack()
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

# Search Button
tk.Button(root, text="Search", command=fetch_weather).pack(pady=10)

# Weather Info Labels
current_weather_label = tk.Label(root, text="Current Weather:", font=("Helvetica", 14, "bold"))
current_weather_label.pack(pady=5)

weather_label = tk.Label(root, font=("Helvetica", 12))
weather_label.pack()

humidity_label = tk.Label(root, font=("Helvetica", 10))
humidity_label.pack()

pressure_label = tk.Label(root, font=("Helvetica", 10))
pressure_label.pack()

description_label = tk.Label(root, font=("Helvetica", 10))
description_label.pack()

visibility_label = tk.Label(root, font=("Helvetica", 10))
visibility_label.pack()

sunrise_label = tk.Label(root, font=("Helvetica", 10))
sunrise_label.pack()

sunset_label = tk.Label(root, font=("Helvetica", 10))
sunset_label.pack()

# Reset and Exit Buttons
frame = tk.Frame(root)
frame.pack(pady=20)

tk.Button(frame, text="Reset", command=reset, bg="orange", fg="white").grid(row=0, column=0, padx=10)
tk.Button(frame, text="Exit", command=root.quit, bg="red", fg="white").grid(row=0, column=1, padx=10)

root.mainloop()
