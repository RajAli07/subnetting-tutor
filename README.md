# Network Subnetting Tutor

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An advanced, interactive web architecture built with Flask that parses IPv4 addresses and teaches deep subnetting logic through step-by-step visual mapping.

![Project UI Preview - Hero](https://i.postimg.cc/XqrSCz1v/Screenshot-2026-09-04-at-12-53-30-AM.png)

![Project UI Preview - Hero](https://i.postimg.cc/8CCSGcdx/Screenshot-2026-09-04-at-1-01-02-AM.png)

![Project UI Preview - Hero](https://i.postimg.cc/7LQyZ4XB/Screenshot-2026-09-04-at-1-01-05-AM.png)

## 📌 Overview

Understanding Network Subnetting can be mathematically complex. This utility abstracts the complexity by taking any valid IPv4 address and automatically generating a complete breakdown of its network boundaries, binary conversions, and architectural class. It features a unique **Teacher's Slate** engine that explains the background math in a classroom-style format.

## 🚀 Core Features

### 1. Deep Architecture Analysis

* **Algorithmic Classification:** Automatically detects network class (A, B, C, Loopback, Multicast, or Experimental).
* **Boundary Computation:** Highly accurate calculation of Network ID, First Valid Host, Last Valid Host, and Broadcast Address based on default subnet masks.
* **IP Type Identification:** Identifies whether the input IP is Public, Private, or Localhost.

### 2. Binary & Decimal Mapping

* **Real-time Conversion:** Transforms standard decimal octets into a complete 32-bit binary string.
* **Visual Formatting:** Color-coded binary output to help visualize network bits versus host bits.

### 3. The "Teacher's Slate" Engine

* **Interactive Explanation:** Provides a step-by-step mathematical trace of how the subnet boundaries were derived.
* **Logic Breakdown:** Explains the bitwise operations (AND logic) between the IP address and the Subnet Mask in plain text.

### 4. Enterprise-Grade UI/UX

* **Glassmorphism Design:** Modern, clean interface utilizing Tailwind CSS.
* **Asynchronous Data Fetching:** Seamless API calls using Vanilla JS Fetch API for zero-reload operations.
* **Client-Side Validation:** Regex-based validation to ensure only valid IPv4 configurations reach the backend.

## 🛠️ Technical Stack

* **Backend Engine:** Python, Flask, Werkzeug
* **Frontend Interface:** HTML5, Tailwind CSS, Vanilla JavaScript
* **API Architecture:** RESTful standard with strict JSON serialization

## 📂 Project Structure

subnetting-tutor/
├── app.py                  # Main Flask application and API routes
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
└── README.md               # Project documentation

## 🔌 API Reference

The application exposes a REST API endpoint for subnet calculation.

**Endpoint:** `POST /api/calculate`

**Request Body (JSON):**

JSON

{
  "ip": "192.168.2.1"
}

**Response (JSON):**

JSON

{
  "class": "C",
  "subnet": "255.255.255.0",
  "type": "Private",
  "binary": "11000000.10101000.00000010.00000001",
  "net_id": "192.168.2.0",
  "first_host": "192.168.2.1",
  "last_host": "192.168.2.254",
  "broadcast": "192.168.2.255",
  "explanation": "<html_string>"
}

## ⚙️ Installation & Setup

1. **Clone the repository:**

    Bash

    ```
    
   git clone [https://github.com/RajAli07/subnetting-tutor.git](https://github.com/RajAli07/subnetting-tutor.git)
   cd subnetting-tutor
       
    ```

2. **Initialize Virtual Environment:**

    Bash

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    ```

3. **Install Dependencies:**

    Bash

    ```
    pip install -r requirements.txt
    
    ```

4. **Run the Application Engine:**

    Bash

    ```
    python app.py
    
    ```

    The application will boot up on `http://127.0.0.1:5000`.

5. **Live on this site :**

    Bash

    ```
   https://subnettingtutor.vercel.app/    

    ```

   

## 👨‍💻 Developer

  **raaZ© ❤️**
