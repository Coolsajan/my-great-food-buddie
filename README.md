---
title: Great Food Buddie
emoji: 🍽️
colorFrom: indigo
colorTo: pink
sdk: streamlit
sdk_version: "1.45.1"
suggested_hardware: "cpu-basic"
suggested_storage: "medium"
app_file: app.py
pinned: false
---

# 🍽️ Great Food Buddie

**Great Food Buddie** is an intelligent chatbot built using **Streamlit** that helps users explore food places and restaurants. Ask about any restaurant, and the assistant will guide you step-by-step—from identifying the place to giving detailed insights based on retrieved reviews.

---

## 🚀 Features

- 🤖 **Interactive Chatbot UI** powered by `st.chat_input` and `st.chat_message`.
- 📍 **Step-by-step flow**:
  1. Ask the food place.
  2. Ask the location.
  3. Ask the question.
- 🔎 **ChromeaDB integration** for storing and retrieving review data.
- 💬 **Natural response generation** via `retrieve_and_generate`.
- 🎨 **Custom animated UI** using Lottie and CSS enhancements.
- 📦 Easy deployment and clean layout with a responsive centered page.

---

## 🧠 Tech Stack

| Component       | Technology                                 |
| --------------- | ------------------------------------------ |
| Frontend        | Streamlit                                  |
| Chat UI         | `st.chat_input`, `st.chat_message`         |
| Animation       | [Lottie Files](https://lottiefiles.com/)   |
| Backend Logic   | Python                                     |
| Data Retrieval  | ChromeaDB (via `check_dB_data`)            |
| Response Engine | Custom retriever (`retrieve_and_generate`) |
| Styling         | Custom CSS injected via Streamlit          |

---

## 📷 Screenshots

> ![Screnshot of greatfoodbuddie UI](image.png)

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/great-food-buddie.git
cd great-food-buddie

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

---

## 📚 How It Works

1. User enters the name of a food place.
2. App asks for its location.
3. App checks if the data exists in the database (via `check_dB_data`).
4. Once confirmed, user can ask specific questions about the place.
5. Answer is generated via the `retrieve_and_generate` pipeline.
6. Everything is shown with a friendly UI and chat animation.

---

## ✨ Future Plans

- Integrate live Google Reviews scraping (with consent).
- Enhance the RAG system with sentiment analysis.
- Add multilingual support.
- Export chat history or summaries.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [LottieFiles](https://lottiefiles.com/)
- ChromeaDB for retrieval
- Your custom RAG pipeline

---

## 📬 Contact

> Created with ❤️ by Sajan Thapa  
> ✉️ Contact: tsajan001@.gmail.com  
> 🌐 [[My Linkedin](https://www.linkedin.com/in/sabu-sajanthapa/)]
