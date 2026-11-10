import sqlite3
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict
import re
import streamlit as st

def generate_portfolio_chart(customer_id: int = 1):
    conn = sqlite3.connect("data/portfolio.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, tckn, vkn, type, investment_account_no
        FROM customers
        WHERE id = ?
    """, (customer_id,))
    customer_info = cursor.fetchone()

    if not customer_info:
        conn.close()
        return f"Müşteri ID {customer_id} bulunamadı."
    
    name, tckn, vkn, type, account_no = customer_info

    tckn = tckn if tckn else ""
    vkn = vkn if vkn else ""
    type = type.lower() if type else ""

    if type == "bireysel":
        id_label = f"tckn: {tckn}" if tckn else "TCKN bilgisi yok"
    elif type == "kurumsal":
        id_label = f"vkn: {vkn}" if vkn else "VKN bilgisi yok"
    else:
        id_label = "Kimlik bilgisi yok"

    cursor.execute("""
        SELECT stock_code, quantity
        FROM portfolio
        WHERE customer_id = ?
    """, (customer_id,))
    data = cursor.fetchall()
    conn.close()

    if not data:
        return f"{name} için portföy verisi bulunamadı."
    
    
    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]

    
    # Grafik oluştur
    fig, ax = plt.subplots(figsize=(3, 2))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    # Yazı boyutlarını küçült
    plt.setp(texts, size=7)
    plt.setp(autotexts, size=7)

    ax.set_title(f"{name} ({id_label})\nHesap No: {account_no}", fontsize=6)
    ax.axis('equal')

    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

    # Yazılı portföy özeti
    portfolio_text = f"{name} ({id_label})\nHesap No: {account_no}\nPortföy dağılımı:\n"
    for label, size in zip(labels, sizes):
        percentage = (size / sum(sizes)) * 100
        portfolio_text += f"• {label}: {size} adet (%{percentage:.1f})\n"

    return portfolio_text


def portfolio_chart(state):
    match = re.search(r"müşteri(?:\s+id(?:si)?)?\s*(?:=|:)?\s*(\d+)", state["question"].lower())
    
    if not match:
        fallback = re.search(r"\b(\d{1,3})\b", state["question"])
        if fallback:
            customer_id = int(fallback.group(1))
        else:
            return {"answer": "Geçerli bir müşteri ID'si giriniz."}
    else:
        customer_id = int(match.group(1))

    portfolio_text = generate_portfolio_chart(customer_id)
    return {"answer": portfolio_text}