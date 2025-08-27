---

# 🎓 Student Data Querying App

This is a **Python + SQLite3-based command-line application** that allows users to query a student database (`HyperionDev.db`) using plain text commands. It supports data retrieval, filtering, and optional export to **JSON** or **XML** formats.

---

## 📁 Files

| File                  | Description                                                                       |
| --------------------- | --------------------------------------------------------------------------------- |
| `HyperionDev.db`      | SQLite database storing students, courses, reviews, and teacher information       |
| `Lookup.py`           | Main Python script to interact with the database                                  |
| `Database README.txt` | This file: overview and documentation                                             |
| `create_database.sql` | SQL file that creates the database "HyperionDev.db" when run (replaces if exists) |

---

## 💡 What This Program Does

The script connects to `HyperionDev.db` and allows a user to:

| Command                    | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `d`                        | View a demo listing all student names                             |
| `vs <student_id>`          | View all subjects taken by a student                              |
| `la <firstname> <surname>` | Look up the address of a student                                  |
| `lr <student_id>`          | List all reviews for a student                                    |
| `lc <teacher_id>`          | List all courses taught by a teacher                              |
| `lnc`                      | List students **who have not completed** their course             |
| `lf`                       | List students **who have completed** their course but scored ≤ 30 |
| `e`                        | Exit the application                                              |

---

## 🔄 Data Export Options

After any query is executed, the user is offered the option to save the results to a file.

Supported formats:

* `.json` – Export data as JSON
* `.xml` – Export data as XML

Examples of valid filenames:

* `results.json`
* `incomplete_students.xml`

---

## 📥 Example Data Output

### Console output

```
What would you like to do?

vs 101
Course A | 
Course B | 
```

### JSON

```json
[
  {
    "course_name": "Course A"
  },
  {
    "course_name": "Course B"
  }
]
```

### XML

```xml
<Lines>
  <Record>
    <course_name>Course A</course_name>
  </Record>
  <Record>
    <course_name>Course B</course_name>
  </Record>
</Lines>
```

---

## 🧱 How It Works

* The program uses parameterized queries to prevent SQL injection.
* Input validation ensures the correct number of arguments are passed for each command.
* Export functions (`store_data_as_json`, `store_data_as_xml`) format the data correctly before writing.

---

## ✅ Requirements

* Python 3.x
* A valid SQLite database file named `HyperionDev.db` - created with create_database.sql
* Standard libraries used:

  * `sqlite3`
  * `json`
  * `xml.etree.ElementTree`

---

## 🚀 How to Run

1. Place `lookup.py` in the same folder as `HyperionDev.db`
2. Run the script:

   ```bash
   python lookup.py
   ```
3. Follow the on-screen prompts to interact with the database.

---

## 📌 Notes

* The database must be named exactly `HyperionDev.db`. Otherwise, the program will exit.
* This script is designed to **read/query** from the database only. It does not modify it.
* Invalid commands or incorrect usage will result in clear, user-friendly error messages.

---

