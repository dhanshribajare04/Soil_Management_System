import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import random
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# MySQL Database Connection Details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "dhanu@12345678",
    "database": "Soil_management_system"
}

# Sample data for soil properties
locations = ["Texas, USA", "Punjab, India", "Nairobi, Kenya", "Queensland, AUS", "São Paulo, Brazil", "Beijing, China", "Cairo, Egypt", "Ontario, Canada"]
soil_types = ["Sandy", "Clay", "Silt", "Peat", "Chalk", "Loam", "Loess", "Rocky"]
crop_suitability_list = ["Corn, Wheat", "Rice, Sugarcane", "Maize, Beans", "Cotton, Sorghum", "Coffee, Soybean", "Barley, Oats", "Vegetables, Fruits", "Peanuts, Sunflower"]

# Function to Connect to MySQL Database
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Function to Insert Manual Soil Data
def insert_manual_record():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        location = location_entry.get()
        pH_level = pH_entry.get()
        moisture_content = moisture_entry.get()
        soil_type = soil_type_entry.get()
        crop_suitability = crop_suitability_entry.get()

        if not location or not pH_level or not moisture_content or not soil_type or not crop_suitability:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return

        try:
            cursor.execute("""
                INSERT INTO soil_data (location, pH_level, moisture_content, soil_type, crop_suitability)
                VALUES (%s, %s, %s, %s, %s)
            """, (location, pH_level, moisture_content, soil_type, crop_suitability))
            conn.commit()
            messagebox.showinfo("Success", "Soil record inserted successfully!")
            conn.close()
            display_records()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error inserting record: {e}")

# Function to Generate Random Soil Data
def generate_data():
    location = random.choice(locations)
    pH_level = round(random.uniform(4, 9), 2)
    moisture_content = round(random.uniform(0, 100), 2)
    soil_type = random.choice(soil_types)
    crop_suitability = random.choice(crop_suitability_list)
    return (location, pH_level, moisture_content, soil_type, crop_suitability)

# Function to Insert Bulk Soil Data
def insert_bulk_records():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        batch_size = 1000
        total_records = 1000000  # 1,00,000 records

        for i in range(0, total_records, batch_size):
            data_batch = [generate_data() for _ in range(batch_size)]
            cursor.executemany("""
                INSERT INTO soil_data (location, pH_level, moisture_content, soil_type, crop_suitability)
                VALUES (%s, %s, %s, %s, %s)
            """, data_batch)
            conn.commit()
            progress_label.config(text=f"{i + batch_size} records inserted...")

        messagebox.showinfo("Success", "100,000 records inserted successfully!")
        conn.close()
        display_records()

# Function to Display Records
def display_records():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM soil_data ORDER BY soil_id DESC LIMIT 20")  # Show last 20 records
        rows = cursor.fetchall()
        conn.close()

        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert("", "end", values=row)

# GUI Setup
root = tk.Tk()
root.title("Soil Management System")
root.geometry("900x600")

# Input Fields
tk.Label(root, text="Location").grid(row=0, column=0)
location_entry = tk.Entry(root)
location_entry.grid(row=0, column=1)

tk.Label(root, text="pH Level").grid(row=1, column=0)
pH_entry = tk.Entry(root)
pH_entry.grid(row=1, column=1)

tk.Label(root, text="Moisture Content (%)").grid(row=2, column=0)
moisture_entry = tk.Entry(root)
moisture_entry.grid(row=2, column=1)

tk.Label(root, text="Soil Type").grid(row=3, column=0)
soil_type_entry = tk.Entry(root)
soil_type_entry.grid(row=3, column=1)

tk.Label(root, text="Crop Suitability").grid(row=4, column=0)
crop_suitability_entry = tk.Entry(root)
crop_suitability_entry.grid(row=4, column=1)

# Buttons
insert_button = tk.Button(root, text="Insert Soil Record", command=insert_manual_record)
insert_button.grid(row=5, column=0, columnspan=2)

bulk_insert_button = tk.Button(root, text="Insert 1000,000 Random Records", command=insert_bulk_records)
bulk_insert_button.grid(row=6, column=0, columnspan=2)

progress_label = tk.Label(root, text="")
progress_label.grid(row=7, column=0, columnspan=2)

# Table to Display Records
columns = ("ID", "Location", "pH Level", "Moisture (%)", "Soil Type", "Crop Suitability")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=8, column=0, columnspan=2)

# Load initial records
display_records()

# Run the GUI
root.mainloop()
